import hashlib
import hmac
import time
from urllib.parse import urlencode
import requests
from typing import Dict, Any

from .logging_config import logger

BASE_URL = "https://testnet.binancefuture.com"

class BinanceFuturesClient:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key

    def _get_timestamp(self) -> int:
        return int(time.time() * 1000)

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.secret_key.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> Dict[str, Any]:
        """Places an order on Binance Futures Testnet."""
        endpoint = "/fapi/v1/order"
        url = f"{BASE_URL}{endpoint}"

        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": self._get_timestamp(),
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good Till Cancelled

        # Create query string and compute signature
        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        params["signature"] = signature

        headers = {
            "X-MBX-APIKEY": self.api_key
        }

        logger.info(f"Sending request to {url} with params: {params}")

        try:
            response = requests.post(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Order successful: {data}")
            return data
        except requests.exceptions.HTTPError as http_err:
            error_data = response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text
            logger.error(f"HTTP error occurred: {http_err} | Response: {error_data}")
            raise Exception(f"Binance API Error: {error_data}")
        except Exception as err:
            logger.error(f"Network processing or API error occurred: {err}")
            raise Exception(f"Failed to place order: {err}")
