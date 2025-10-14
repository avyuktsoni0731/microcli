import serial
import threading
from rich.console import Console

console = Console()

def start_monitor(port, baud):
    try:
        ser = serial.Serial(port, baud, timeout=1)
        console.print(f"[green]🔌 Connected to {port}[/green]")
        console.print("[yellow]Type 'exit' to quit[/yellow]")

        def read_from_serial():
            while True:
                try:
                    line = ser.readline().decode(errors='ignore').strip()
                    if line:
                        console.print(f"[cyan]<< {line}[/cyan]")
                except Exception:
                    break

        thread = threading.Thread(target=read_from_serial, daemon=True)
        thread.start()

        while True:
            user_input = input(">> ")
            if user_input.lower() == "exit":
                console.print("[red]👋 Exiting monitor[/red]")
                break
            ser.write((user_input + "\n").encode())

        ser.close()
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
