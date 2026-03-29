from typing import Dict, Any
from .client import BinanceFuturesClient
from .validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price
)
from .logging_config import logger

def execute_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None
) -> Dict[str, Any]:
    """Validates inputs and places an order via the client."""
    
    logger.info(f"Preparing order: {side} {quantity} {symbol} @ {order_type} (Price: {price})")

    try:
        # Validate all inputs
        v_symbol = validate_symbol(symbol)
        v_side = validate_side(side)
        v_type = validate_order_type(order_type)
        v_qty = validate_quantity(quantity)
        v_price = validate_price(price, v_type)

        # Place the order
        response = client.place_order(
            symbol=v_symbol,
            side=v_side,
            order_type=v_type,
            quantity=v_qty,
            price=v_price if v_type == "LIMIT" else None
        )
        return response

    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        raise
    except Exception as e:
        logger.error(f"Order Execution Failed: {e}")
        raise
