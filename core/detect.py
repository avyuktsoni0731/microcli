import serial.tools.list_ports
from rich.table import Table
from rich.console import Console

console = Console()

def list_ports():
    ports = serial.tools.list_ports.comports()
    if not ports:
        console.print("[red]❌ No serial ports found[/red]")
        return
    table = Table(title="🔌 Available Ports")
    table.add_column("Index")
    table.add_column("Port")
    table.add_column("Description")
    table.add_column("Manufacturer")
    for i, p in enumerate(ports):
        table.add_row(str(i), p.device, p.description or "N/A", p.manufacturer or "Unknown")
    console.print(table)
