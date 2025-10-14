import serial
from rich.console import Console

console = Console()

def connect_to_board(port):
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        console.print(f"[green]✅ Connected to {port}[/green]")
        ser.close()
    except serial.SerialException as e:
        console.print(f"[red]❌ Could not open port {port}: {e}[/red]")
