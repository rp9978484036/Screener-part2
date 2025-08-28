# Stock Scanner (GitHub Actions - Plan B)

This repository runs scheduled scans via GitHub Actions (no server required).
It uses `yfinance` for prices and technicals, and attempts best-effort fundamentals from yfinance too.
For production-grade fundamentals (PEG, ROE 5Y, promoter holding, pledged %), replace `fetch_fundamentals`
with a paid vendor or a reliable scraping routine and add its credentials as GitHub secrets.

## How it works
- Loads ticker universe from `universe.csv` (one symbol per line). If not present, uses a small default list.
- Fetches historical prices via `yfinance`.
- Computes SMA50, SMA200, RSI14, MACD, volume averages.
- Applies your fundamental and technical filters.
- Writes results to Google Sheets (service account JSON provided as GitHub secret).
- Sends Telegram alerts for Trending and Retest200 results.

## Setup (GitHub)
1. Create a new GitHub repo and push this project.
2. In repo Settings → Secrets → Actions add:
   - `TELEGRAM_TOKEN` - your Telegram bot token
   - `TELEGRAM_CHAT_ID` - your chat id
   - `GOOGLE_SHEET_ID` - your sheet id
   - `GOOGLE_CREDENTIALS_JSON` - the full service account JSON **content** (not file) as a secret
3. (Optional) Upload `universe.csv` with tickers (one per line). If not present, sample tickers used.
4. GitHub Actions will run on schedule (see `.github/workflows/scanner.yml`).

## Notes
- This is a fully functional starter. However, for large universes or production you MUST replace the fundamentals source with a paid API.
- The runner is ephemeral; the service account JSON is created at runtime from the secret.
