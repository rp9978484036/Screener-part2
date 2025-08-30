#!/usr/bin/env python3
"""Stock Scanner for GitHub Actions (Plan B)

Uses yfinance for price + technicals. Attempts fundamentals from yfinance where possible.
Reads ticker universe from universe.csv (one symbol per line). Writes results to Google Sheets
and sends Telegram alerts for Trending and Retest200 screening lists.
"""

import os, sys, time, json, logging, pytz
from datetime import datetime, timezone, time as dt_time, timedelta
import pandas as pd
import numpy as np
import requests
import yfinance as yf
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# --- Config from env / secrets ---
SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
CREDENTIALS_PATH = 'credentials.json'  # written by GitHub Actions from secret

# Screening thresholds
MARKETCAP_MIN_CRORE = float(os.getenv('MARKETCAP_MIN_CRORE', '1000'))
PEG_MAX = float(os.getenv('PEG_MAX', '1.0'))
DEBT_EQUITY_MAX = float(os.getenv('DEBT_EQUITY_MAX', '0.5'))
PROMOTER_MIN_PCT = float(os.getenv('PROMOTER_MIN_PCT', '50'))
SALES_GROWTH_3Y_MIN = float(os.getenv('SALES_GROWTH_3Y_MIN', '15'))
PROFIT_GROWTH_5Y_MIN = float(os.getenv('PROFIT_GROWTH_5Y_MIN', '15'))
PLEDGED_MAX_PCT = float(os.getenv('PLEDGED_MAX_PCT', '1'))
OPM_MIN = float(os.getenv('OPM_MIN', '15'))
PRICE_TO_SALES_MAX = float(os.getenv('PRICE_TO_SALES_MAX', '10'))
EV_EBITDA_MAX = float(os.getenv('EV_EBITDA_MAX', '25'))

# --- Run control ---
IS_MANUAL = os.getenv("GITHUB_EVENT_NAME") == "workflow_dispatch"

# Market hours in IST
MARKET_OPEN = dt_time(9, 0)     # 9:00 AM
MARKET_CLOSE = dt_time(15, 30)  # 3:30 PM

def is_market_open():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist).time()
    return MARKET_OPEN <= now <= MARKET_CLOSE

def is_weekday():
    ist = pytz.timezone("Asia/Kolkata")
    today = datetime.now(ist).weekday()
    return today < 5  # Mon–Fri

# --- Guard: only restrict scheduled runs ---
if not IS_MANUAL:
    if not is_weekday():
        print("⏸ Market closed (Weekend) — scanner will not run now.")
        sys.exit(0)
    if not is_market_open():
        print("⏸ Market is closed — scanner will not run now.")
        sys.exit(0)
else:
    logging.info("Manual run detected — skipping market/weekday checks.")

# --- Bad symbol handling ---
def mark_bad_symbol(symbol, reason=""):
    today = datetime.today().strftime("%Y-%m-%d")
    with open("bad_symbols.txt","a") as f:
        f.write(f"{symbol}|{today}\n")
    logging.info("Marked %s as bad symbol (%s)", symbol, reason)

def load_universe(path='universe.csv'):
    syms = []
    if os.path.exists(path):
        with open(path,'r') as f:
            syms = [line.strip() for line in f if line.strip()]

    # Load bad symbols with dates
    bad = {}
    if os.path.exists("bad_symbols.txt"):
        with open("bad_symbols.txt","r") as b:
            for line in b:
                parts = line.strip().split("|")
                if len(parts) == 2:
                    sym, date_str = parts
                    try:
                        bad[sym] = datetime.strptime(date_str, "%Y-%m-%d")
                    except:
                        bad[sym] = datetime.today()
                else:
                    bad[parts[0]] = datetime.today()

    # Filter: allow retry if older than 7 days
    today = datetime.today()
    filtered = []
    skipped = 0
    for s in syms:
        if s in bad and (today - bad[s]).days < 7:
            skipped += 1
            continue
        filtered.append(s)

    logging.info('Loaded %d tickers (skipped %d bad symbols)', len(filtered), skipped)
    return list(dict.fromkeys(filtered)) if filtered else syms

# --- Utilities ---
def send_telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logging.warning('Telegram not configured')
        return
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}
    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        logging.info('Telegram message sent')
    except Exception as e:
        logging.exception('Failed to send Telegram: %s', e)

def sma(series, window):
    return series.rolling(window=window, min_periods=1).mean()

def calc_rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.ewm(com=period-1, adjust=False).mean()
    ma_down = down.ewm(com=period-1, adjust=False).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calc_macd(series):
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

# --- Fundamentals ---
def fetch_fundamentals(symbol):
    res = {'symbol': symbol}
    try:
        tk = yf.Ticker(symbol)
        info = tk.info or {}
        if not info:
            mark_bad_symbol(symbol, "no fundamentals")
            return res
        res['marketCap'] = info.get('marketCap')
        res['peg'] = info.get('pegRatio') or info.get('peg')
        res['pe'] = info.get('trailingPE') or info.get('forwardPE')
        res['priceToSales'] = info.get('priceToSalesTrailing12Months')
        res['evToEbitda'] = info.get('enterpriseToEbitda')
    except Exception as e:
        mark_bad_symbol(symbol, f"fundamentals fetch failed: {e}")
    return res

# --- Technicals ---
def fetch_technical(symbol):
    out = {'symbol': symbol}
    try:
        tk = yf.Ticker(symbol)
        hist = tk.history(period='1y', interval='1d', actions=False)
        if hist is None or hist.empty:
            mark_bad_symbol(symbol, "no price data")
            return out
        close = hist['Close']
        vol = hist['Volume']
        out['latest_close'] = float(close.iloc[-1])
        out['sma50'] = float(sma(close,50).iloc[-1])
        out['sma200'] = float(sma(close,200).iloc[-1])
        rsi = calc_rsi(close,14)
        out['rsi14'] = float(rsi.iloc[-1])
        macd, macd_signal = calc_macd(close)
        out['macd'] = float(macd.iloc[-1])
        out['macd_signal'] = float(macd_signal.iloc[-1])
        out['volume'] = int(vol.iloc[-1])
        out['avgvol1w'] = int(vol.tail(5).mean())
        out['avgvol20'] = int(vol.tail(20).mean()) if len(vol)>=20 else int(vol.mean())
        out['52w_low'] = float(close.tail(252).min()) if len(close)>=252 else float(close.min())
        if len(close) >= 2:
            out['1d_close'] = float(close.iloc[-2])
            out['1d_high'] = float(hist['High'].iloc[-2])
    except Exception as e:
        mark_bad_symbol(symbol, f"technicals fetch failed: {e}")
    return out

# --- Screening functions ---
def passes_fundamental(row):
    mc = row.get('marketCap')
    if mc is None:
        return False
    mc_crore = float(mc) / 1e7
    if mc_crore < MARKETCAP_MIN_CRORE:
        return False
    if row.get('peg') is not None and row['peg'] >= PEG_MAX:
        return False
    if row.get('priceToSales') is not None and row['priceToSales'] > PRICE_TO_SALES_MAX:
        return False
    if row.get('evToEbitda') is not None and row['evToEbitda'] > EV_EBITDA_MAX:
        return False
    return True

def passes_trending(row):
    try:
        if row.get('latest_close') is None: return False
        if not (row['latest_close'] > row.get('sma50',0) and row['latest_close'] > row.get('sma200',0)): return False
        if not (row.get('sma50',0) > row.get('sma200',0)): return False
        if row.get('rsi14') is None or not (50 < row['rsi14'] < 80): return False
        if row.get('52w_low') is None or not (row['latest_close'] > row['52w_low']): return False
        if row.get('volume') is None or row.get('avgvol1w') is None: return False
        if not (row['volume'] > 1.5 * row['avgvol1w']): return False
        return True
    except Exception as e:
        logging.info("Trending check failed for %s: %s", row.get('symbol'), e)
        return False

def passes_retest200(row):
    try:
        if any(row.get(k) is None for k in ('latest_close','sma200','1d_close','1d_high','volume')): return False
        if not (row['latest_close'] > row['sma200']): return False
        if not (abs(row['1d_close'] - row['sma200']) / max(1e-9, row['sma200']) <= 0.05): return False
        if not (abs(row['latest_close'] - row['1d_high']) / max(1e-9, row['1d_high']) <= 0.02): return False
        if not (row['volume'] > 1.2 * row.get('avgvol20', row.get('avgvol1w',0))): return False
        if row.get('rsi14') is None or row['rsi14'] <= 50: return False
        if row.get('macd') is None or row.get('macd_signal') is None or not (row['macd'] > row['macd_signal']): return False
        return True
    except Exception as e:
        logging.info("Retest200 check failed for %s: %s", row.get('symbol'), e)
        return False

# --- Google Sheets ---
def sheets_client():
    if not os.path.exists(CREDENTIALS_PATH):
        logging.error('Google credentials file not found: %s', CREDENTIALS_PATH)
        return None
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    service = build('sheets', 'v4', credentials=creds)
    return service

def write_df_to_sheet(service, tab, df):
    if service is None:
        logging.warning('No sheets service; skipping write for %s', tab)
        return
    if df.empty:
        logging.info("No data to write for %s", tab)
        return
    df = df.copy()
    df.insert(0, "Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    values = [df.columns.tolist()] + df.fillna('').values.tolist()
    rng = f"{tab}!A1"
    try:
        service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=rng,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': values}
        ).execute()
        logging.info('Wrote %d rows to %s', len(df), tab)
    except Exception as e:
        logging.exception('Error writing to sheet %s: %s', tab, e)

# --- Main ---
def main():
    universe = load_universe()
    all_results = []
    for sym in universe:
        f = fetch_fundamentals(sym)
        t = fetch_technical(sym)
        merged = {**f, **t}
        all_results.append(merged)
        time.sleep(0.5)

    df_all = pd.DataFrame(all_results)
    df_all_sorted = df_all.sort_values(by=['symbol'])
    fund = [r for r in all_results if passes_fundamental(r)]
    df_fund = pd.DataFrame(fund)
    trend = [r for r in fund if passes_trending(r)]
    df_trend = pd.DataFrame(trend)
    ret = [r for r in fund if passes_retest200(r)]
    df_retest = pd.DataFrame(ret)

    svc = sheets_client()
    write_df_to_sheet(svc, 'AllStocks', df_all_sorted)
    write_df_to_sheet(svc, 'Fundamental_Strong', df_fund)
    write_df_to_sheet(svc, 'Trending', df_trend)
    write_df_to_sheet(svc, 'Retest200', df_retest)

    state = {}
    if os.path.exists('state.json'):
        try:
            with open('state.json','r') as f:
                state = json.load(f)
        except:
            state = {}
    new_trend = [r for r in df_trend['symbol'].tolist() if r not in state.get('trending',[])] if not df_trend.empty else []
    new_retest = [r for r in df_retest['symbol'].tolist() if r not in state.get('retest200',[])] if not df_retest.empty else []
    msg = ''
    if new_trend:
        msg += f"*Trending* ({len(new_trend)}):\n" + '\n'.join(new_trend) + '\n\n'
    if new_retest:
        msg += f"*Retest200* ({len(new_retest)}):\n" + '\n'.join(new_retest) + '\n\n'
    if msg:
        if SHEET_ID:
            sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
            msg += f"Sheet: {sheet_url}"
        send_telegram(msg)
        state.setdefault('trending',[]).extend(new_trend)
        state.setdefault('retest200',[]).extend(new_retest)
        try:
            with open('state.json','w') as f:
                json.dump(state,f)
        except:
            pass
    else:
        logging.info('No new alerts')

if __name__ == '__main__':
    main()
