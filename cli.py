import typer
from rich.console import Console
from microcli.core.detect import list_ports
from microcli.core.connect import connect_to_board
from microcli.core.monitor import start_monitor

app = typer.Typer(help="MicroCLI: Manage and interact with your microcontrollers easily ⚡")
console = Console()

@app.command()
def ports():
    """List all available serial ports."""
    list_ports()

@app.command()
def connect(port: str = typer.Argument(..., help="Serial port (e.g., COM3 or /dev/ttyUSB0)")):
    """Connect to a board on a given port."""
    connect_to_board(port)

@app.command()
def monitor(port: str = typer.Argument(..., help="Port to open REPL for"),
            baud: int = typer.Option(115200, help="Baud rate")):
    """Open an interactive serial monitor."""
    start_monitor(port, baud)

if __name__ == "__main__":
    app()
