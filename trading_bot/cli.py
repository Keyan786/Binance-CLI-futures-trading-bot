import os
import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.orders import execute_order

# Load environment variables
load_dotenv()

app = typer.Typer(help="Binance Futures Testnet Trading Bot")
console = Console()

@app.command()
def trade(
    symbol: str = typer.Argument(..., help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="BUY or SELL"),
    order_type: str = typer.Argument(..., help="MARKET or LIMIT"),
    quantity: float = typer.Argument(..., help="Amount to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Price required if using LIMIT order"),
):
    """
    Place an order on the Binance Futures Testnet.
    """
    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    secret_key = os.getenv("BINANCE_TESTNET_SECRET_KEY")

    if not api_key or not secret_key:
        console.print("[bold red]Error:[/] API credentials not found. Please set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_SECRET_KEY in your .env file or environment.")
        raise typer.Exit(code=1)

    console.print(f"\n[bold blue]Order Summary Request:[/] {side} {quantity} {symbol} ({order_type})")
    if price:
        console.print(f"[bold blue]Target Price:[/] {price}")
    
    client = BinanceFuturesClient(api_key=api_key, secret_key=secret_key)

    with console.status("[bold cyan]Placing order on Binance Testnet...", spinner="dots"):
        try:
            response = execute_order(
                client=client,
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )
            
            # Print success response in a table
            table = Table(title="Order Confirmation", show_header=True, header_style="bold magenta")
            table.add_column("Order ID", justify="center")
            table.add_column("Symbol", justify="center")
            table.add_column("Status", justify="center")
            table.add_column("Executed Qty", justify="center")
            table.add_column("Avg Price", justify="center")

            order_id = str(response.get("orderId", "N/A"))
            res_symbol = response.get("symbol", symbol)
            status = response.get("status", "N/A")
            executed_qty = str(response.get("executedQty", "0"))
            avg_price = str(response.get("avgPrice", "0"))

            status_color = "green" if status == "NEW" or status == "FILLED" else "yellow"

            table.add_row(
                order_id,
                res_symbol,
                f"[{status_color}]{status}[/]",
                executed_qty,
                avg_price
            )

            console.print(table)
            console.print("[bold green]Success:[/] Order successfully placed and logged.\n")

        except Exception as e:
            console.print(f"[bold red]Failed:[/] {str(e)}\n")
            raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
