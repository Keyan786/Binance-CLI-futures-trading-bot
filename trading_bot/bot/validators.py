def validate_symbol(symbol: str) -> str:
    """Ensure symbol is uppercase and alphanumeric."""
    symbol = symbol.strip().upper()
    if not symbol.isalnum():
        raise ValueError("Symbol must be alphanumeric (e.g., BTCUSDT).")
    return symbol

def validate_side(side: str) -> str:
    """Must be BUY or SELL."""
    side = side.strip().upper()
    if side not in ("BUY", "SELL"):
        raise ValueError("Side must be BUY or SELL.")
    return side

def validate_order_type(order_type: str) -> str:
    """Support MARKET and LIMIT."""
    order_type = order_type.strip().upper()
    if order_type not in ("MARKET", "LIMIT"):
        raise ValueError("Order type must be MARKET or LIMIT.")
    return order_type

def validate_quantity(quantity: float) -> float:
    """Quantity must be positive."""
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return quantity

def validate_price(price: float, order_type: str) -> float:
    """Price required and positive for LIMIT orders."""
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("A positive price is required for LIMIT orders.")
    return price if price is not None else 0.0
