# Binance Futures Testnet Trading Bot

A Python CLI application for placing testnet orders on Binance Futures (USDT-M), using the official REST endpoints.

## Prerequisites
1. Python 3.8+
2. A Binance Futures Testnet account.
   - Go to [Binance Futures Testnet](https://testnet.binancefuture.com)
   - Register / Login (usually via Binance main account or Github auth).
   - Generate your Testnet API Key and Secret Key.

## Setup

1. **Clone / Extract the code**
   Navigate into the project directory:
   ```bash
   cd trading_bot
   ```

2. **Setup virtual environment** (Recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   # Or on Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Credentials**
   Create a `.env` file in the root `trading_bot` directory and add your testnet keys:
   ```env
   BINANCE_TESTNET_API_KEY="your_api_key_here"
   BINANCE_TESTNET_SECRET_KEY="your_secret_key_here"
   ```

## Usage

The application provides an interactive Command Line Interface built with Typer and Rich.

```bash
python cli.py --help
```

### Place a Market Order
```bash
python cli.py BTCUSDT BUY MARKET 0.01
```

### Place a Limit Order
LIMIT orders require the `--price` (or `-p`) parameter.
```bash
python cli.py BTCUSDT SELL LIMIT 0.01 --price 65000.0
```

## Logs

All API requests, responses, and errors are securely logged in the `trading_bot.log` file in the same directory.
