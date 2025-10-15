# microcli/core/shell.py
import difflib
import time
from rich.console import Console
from microcli.core.connect import SerialConnection

console = Console()

COMMON_CMDS = ["LED ON", "LED OFF", "PING", "RESET", "INFO"]

def start_shell(port, baud=115200):
    conn = SerialConnection(port, baud, reconnect=True)
    console.print("[bold green]MicroCLI Shell (type 'help' or 'exit')[/bold green]")
    
    try:
        while True:
            try:
                s = input("micli> ").strip()
            except EOFError:
                break
            if not s:
                continue
            if s.lower() in ("exit", "quit"):
                break
            if s.lower() == "help":
                console.print("Common commands: " + ", ".join(COMMON_CMDS))
                continue

            # Suggest close matches if user mistypes
            if s.upper() not in COMMON_CMDS:
                close = difflib.get_close_matches(s.upper(), COMMON_CMDS, n=2, cutoff=0.6)
                if close:
                    console.print(f"[yellow]Did you mean: {', '.join(close)} ?[/yellow]")

            # Flush any old serial junk before sending
            conn.read_all()

            # Send command
            conn.send(s)
            time.sleep(0.3)  # small delay for board to respond

            # Now read fresh response
            resp = conn.read_all().strip()
            if not resp:
                console.print("[dim]⏳ No response[/dim]")
                continue

            # Smart coloring based on response content
            lower = resp.lower()
            if "on" in lower:
                console.print(f"[green]{resp}[/green]")
            elif "off" in lower:
                console.print(f"[cyan]{resp}[/cyan]")
            elif "pong" in lower:
                console.print(f"[magenta]{resp}[/magenta]")
            elif "error" in lower or "fail" in lower:
                console.print(f"[red]{resp}[/red]")
            else:
                console.print(resp)

    finally:
        conn.close()
