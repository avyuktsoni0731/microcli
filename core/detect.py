# microcli/core/detect.py
import serial.tools.list_ports
from rich.table import Table
from rich.console import Console

console = Console()

def list_ports():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        console.print("[red]❌ No serial ports found[/red]")
        return []
    table = Table(title="🔌 Available Ports")
    table.add_column("Index", style="dim", width=6)
    table.add_column("Port")
    table.add_column("Description")
    table.add_column("Manufacturer")
    table.add_column("VID:PID", style="magenta")
    for i, p in enumerate(ports):
        vid_pid = f"{hex(p.vid) if p.vid else 'N/A'}:{hex(p.pid) if p.pid else 'N/A'}"
        table.add_row(str(i), p.device, p.description or "N/A", p.manufacturer or "Microsoft (default)", vid_pid)
    console.print(table)
    return ports

def auto_detect_port():
    """Return first likely microcontroller port or None."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        return None
    # Heuristics: prefer USB Serial devices not named 'Bluetooth' etc.
    for p in ports:
        lname = (p.description or "").lower()
        if "usb" in lname or "serial" in lname or p.vid:
            return p.device
    return ports[0].device
