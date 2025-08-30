HashMob
hashmob_219_65792
Online

Amit Viradiya — 9:58 AM
TELEGRAM_TOKEN
7548150134:AAEIIqD7TbtHDxP9_8pco1VCFb1JpvMjw88

TELEGRAM_CHAT_ID
544581129

GOOGLE_SHEET_ID
1WD4ZvggAYzXSoTpPEjWP3lTflbif-vzWdVTkCwUYaNA
GOOGLE_CREDENTIALS_JSON
{
  "type": "service_account",
  "project_id": "dulcet-airline-470109-m3",
  "private_key_id": "d8ed5687b75745724a92abbe4625f289e4ad9744",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCvCO8rmLD2QgGe\n2rnPPTxurmxOU5c1dinttfFzoX7voyxtS8lhTuBRKCc/M9NEafOWsHfEyPMRx/fP\nh2BEAcolaYYUZqAmrJwCGE6T9wfeF0vV7QnWqKBs2YOipj22Og0q8ad18U9XnMZ6\nAXyjHxO+LJPv9KmRC1LJEWk1zR3ZQbEo/bRvxayAHH82sNSh6V5t3B2uq/fHWU7o\nROVbOfAGD1WIMpszL5j7DM4MSsCIC9CoifU4IMHxHrFBJrj2bnJUPpyAQyrR+z3o\nji+J9CRwOlbzTY0MJM6kk+aoyO4nJItZRsvKuqNSCNeBjYvrAuQDExVKsyH76gXy\nNO9FudKTAgMBAAECggEAQ1isrZmSfS3ocba2x4ZIOk3iXkDLbUaJ22yl+leo/4tJ\nDMScN1Sh+pf4gdju8OPTVaeQbabj33ORZcgwwfnuTXbMoAzckgTYAfZYRZZG8K0G\nAMmzf2RiVX9bprlQBU1Qw7U3OaofXRZ1R3xK+Hh8oC+GvEzm8Wfp8nNAh/LkCTMZ\n9D2JoAWLRw9j7vNwRKs1/zI9N6B5RXNAfsXYZHdjexFJuC2NWcoKJG60IM/v84GD\n/+DOMMbnu9AnvGDMJ4PaK7BGEwHzNGXxhQw3IliS4s2aEospAGBNu5DSwDtNqTA5\n5Kj9G77EebZWBgOXRIliKJ4nx5h7JSeBZCzDnz5EAQKBgQDm6ReaWzD4xLQ8KMsT\nuYfzKd7z6pbPuYEDgHgkHTj8oRQk54EIFr79oTg7l9YUCaL/SLQ0IRXXH1+DG2tZ\naVG0pxvCPZza/t4N+SYmNkfutl4jIgflJxIc2WGq9P33uVk2Og10FnsJ+UBVF1rD\nS5oyx60mfW5PTipTwevh+l+uzQKBgQDCDaFAHYX309Ou7dKYDcluu8iR8zZyY88j\nQ1mDvItEGbmEWU9oJz+C1qd9gWjO5TeF/VmCiS8N4MX3cQQO5fcJ3Rx/6Y2O8rI+\ncWDtkJbgp/y4sGgjOr676B/lHOi1u8kG8Lzl81DQps4yiHn1X2b//lGfzJ3PdDgo\nUucvm+bG3wKBgEwZ4CSID2C9e2UkUKGEkPCsCQW8d82oJoPf8Dh+xQxFjh0Hizf+\nPx3Z522EghKChoy6CmHv0YHfnhvYio2iL0JpnLVsluh5/Pb/+Pm5BAYBZo8PpSh5\nsvd9ETpFmfntxSAhC9QJoK1Nz0z78HbS0NQRiNhZmGRcr4iBLduBJ821AoGBAIed\nkOjG+T5GmrSw3jGHyROLRtPBHnb5C+UAB4oKdWWleMJmzBjk/PzKWQlcLEwTYydP\n9INGrkzLnm6cXBKxYmFRVr6KEXUqZalAAVZlaxwcKoFEP7MHNg8KXWf4OSXw07/2\n9Hzb+8mmGYq1WE5EWy5ipNbB4DQAa9K6hXj/QlwPAoGBANuf9brKCxpx3CbcWaJK\nQciwrWhKttZTmWpgH+nTwn45GYgg+FSlf96vfCN065jEsG3ReC9U9zXWuJwk0Tzl\n1EQ4PNk1KMC7PXGeAB/5B2gLHj/LcLEMv53a5UP7sPWIiJM7C1uGwCLWVhGuT3Ec\nUJmSzLU2+aTAVih+2YwalJKv\n-----END PRIVATE KEY-----\n",
  "client_email": "screener@dulcet-airline-470109-m3.iam.gserviceaccount.com",
Expand
message.txt
3 KB
#!/usr/bin/env python3
"""Stock Scanner for GitHub Actions (Plan B)

Uses yfinance for price + technicals. Attempts fundamentals from yfinance where possible.
Reads ticker universe from universe.csv (one symbol per line). Writes results to Google Sheets
and sends Telegram alerts for Trending and Retest200 screening lists.
Expand
scanner.py
12 KB
name: Stock Scanner Full

on:
  schedule:
    - cron: '15 3 * * 1-5'   # 08:45 IST full fundamentals run (03:15 UTC)
    - cron: '0 * * * 1-5'    # hourly run (UTC) on weekdays
Expand
scanner.yml
2 KB
﻿
Amit Viradiya
amitviradiya
#!/usr/bin/env python3
"""Stock Scanner for GitHub Actions (Plan B)

Uses yfinance for price + technicals. Attempts fundamentals from yfinance where possible.
Reads ticker universe from universe.csv (one symbol per line). Writes results to Google Sheets
and sends Telegram alerts for Trending and Retest200 screening lists.
"""
import os, sys, time, json, logging, pytz
from datetime import datetime, timezone
import pandas as pd
import numpy as np
import requests
import yfinance as yf
from bs4 import BeautifulSoup
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Config from env / secrets
SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
CREDENTIALS_PATH = 'credentials.json'  # written by GitHub Actions from secret

# Screening thresholds (your specs)
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

# Market hours in IST
MARKET_OPEN = datetime.time(9, 0)     # 9:00 AM
MARKET_CLOSE = datetime.time(15, 30)  # 3:30 PM

def is_market_open():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(ist).time()
    return MARKET_OPEN <= now <= MARKET_CLOSE

# Check before running scanner
if not is_market_open():
    print("⏸ Market is closed — scanner will not run now.")
    sys.exit(0)

# Utilities
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

# Read universe
def load_universe(path='universe.csv'):
    if os.path.exists(path):
        with open(path,'r') as f:
            syms = [line.strip() for line in f if line.strip()]
            logging.info('Loaded %d tickers from %s', len(syms), path)
            return list(dict.fromkeys(syms))
    # fallback sample
    sample = ['INFY.NS','TCS.NS','RELIANCE.NS']
    logging.warning('universe.csv missing - falling back to sample (%s)', ','.join(sample))
    return sample

# Fetch fundamentals (best-effort using yfinance). Replace for production.
def fetch_fundamentals(symbol):
    # returns a dict of metrics; many may be None if vendor lacks them
    res = {'symbol': symbol}
    try:
        tk = yf.Ticker(symbol)
        info = tk.info or {}
        res['marketCap'] = info.get('marketCap')
        res['peg'] = info.get('pegRatio') or info.get('peg')
        res['pe'] = info.get('trailingPE') or info.get('forwardPE')
        res['priceToSales'] = info.get('priceToSalesTrailing12Months')
        res['evToEbitda'] = info.get('enterpriseToEbitda')
        # Some items like promoter holding, pledged % not in yfinance -> left None
    except Exception as e:
        logging.exception('Error fetching fundamentals for %s: %s', symbol, e)
    return res

# Fetch price history and compute technicals
def fetch_technical(symbol):
    out = {'symbol': symbol}
    try:
        tk = yf.Ticker(symbol)
        hist = tk.history(period='1y', interval='1d', actions=False)
        if hist is None or hist.empty:
            logging.warning('No history for %s', symbol)
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
        logging.exception('Error fetching technicals for %s: %s', symbol, e)
    return out

# Screening functions
def passes_fundamental(row):
    # check essentials, convert marketCap to crores if present (marketCap in INR)
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
        logging.exception('Error in trending check: %s', e)
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
        logging.exception('Error in retest200: %s', e)
        return False

# Google Sheets helpers
def sheets_client():
    if not os.path.exists(CREDENTIALS_PATH):
        logging.error('Google credentials file not found: %s', CREDENTIALS_PATH)
        return None
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    service = build('sheets', 'v4', credentials=creds)
    return service

from datetime import datetime

def append_df_to_sheet(service, tab, df):
    if service is None:
        logging.warning('No sheets service; skipping append for %s', tab)
        return

    if df.empty:
        logging.info("No data to append for %s", tab)
        return

    # Add timestamp column
    df = df.copy()
    df.insert(0, "Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    values = [df.columns.tolist()] + df.fillna('').values.tolist()
    rng = f"{tab}!A1"

    try:
        # Use append instead of update
        service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=rng,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': values}
        ).execute()
        logging.info('Appended %d rows to %s', len(df), tab)
    except Exception as e:
        logging.exception('Error appending to sheet %s: %s', tab, e)

def main():
    universe = load_universe()
    all_results = []
    for sym in universe:
        f = fetch_fundamentals(sym)
        t = fetch_technical(sym)
        merged = {**f, **t}
        all_results.append(merged)
        time.sleep(0.5)  # polite

    df_all = pd.DataFrame(all_results)
    df_all_sorted = df_all.sort_values(by=['symbol'])
    # Fundamental strong
    fund = [r for r in all_results if passes_fundamental(r)]
    df_fund = pd.DataFrame(fund)
    # Trending
    trend = [r for r in fund if passes_trending(r)]
    df_trend = pd.DataFrame(trend)
    # Retest200
    ret = [r for r in fund if passes_retest200(r)]
    df_retest = pd.DataFrame(ret)

    # Write to Sheets
    svc = sheets_client()
    write_df_to_sheet(svc, 'AllStocks', df_all_sorted if not df_all_sorted.empty else pd.DataFrame())
    write_df_to_sheet(svc, 'Fundamental_Strong', df_fund if not df_fund.empty else pd.DataFrame())
    write_df_to_sheet(svc, 'Trending', df_trend if not df_trend.empty else pd.DataFrame())
    write_df_to_sheet(svc, 'Retest200', df_retest if not df_retest.empty else pd.DataFrame())

    # Alerts (simple de-dup: use a file 'state.json' in workspace)
    state = {}
    if os.path.exists('state.json'):
        try:
            with open('state.json','r') as f:
                state = json.load(f)
        except:
            state = {}
    new_trend = []
    for r in df_trend['symbol'].tolist() if not df_trend.empty else []:
        if 'trending' not in state or r not in state.get('trending',[]):
            new_trend.append(r)
    new_retest = []
    for r in df_retest['symbol'].tolist() if not df_retest.empty else []:
        if 'retest200' not in state or r not in state.get('retest200',[]):
            new_retest.append(r)
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
        # update state
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
scanner.py
12 KB
