# microcli/cli.py
import typer
from rich.console import Console
from .core import detect, monitor, shell, uploader

app = typer.Typer(help="microcli — Universal microcontroller CLI")
console = Console()

@app.command()
def ports():
    """List available serial ports"""
    detect.list_ports()

@app.command()
def info(port: str = typer.Option(None, help="Port to query (optional)")):
    """Show device info: if port omitted, auto-detect first"""
    if not port:
        port = detect.auto_detect_port()
        if not port:
            console.print("[red]No port found[/red]")
            raise typer.Exit()
    console.print(f"[blue]Querying {port}...[/blue]")
    # Try simple ping/ID handshake
    from .core.connect import SerialConnection
    conn = SerialConnection(port, 115200, reconnect=False)
    conn.send("INFO")
    import time; time.sleep(0.3)
    resp = conn.read_all()
    if resp:
        console.print(f"[green]Device response:[/green]\n{resp}")
    else:
        console.print("[yellow]No response to INFO command — showing port metadata instead[/yellow]")
        detect.list_ports()

@app.command()
def monitor_cmd(port: str = typer.Argument(..., help="Port"),
                baud: int = typer.Option(115200, help="Baud rate"),
                save: str = typer.Option(None, "--save", "-s", help="Save log to path (csv)"),
                autoreconnect: bool = typer.Option(True, "--autoreconnect/--no-autoreconnect")):
    """Start serial monitor (with optional logging)"""
    monitor.start_monitor(port, baud, save_path=save, auto_reconnect=autoreconnect)

@app.command()
def upload(port: str = typer.Argument(..., help="Port"),
           sketch: str = typer.Argument(..., help="Path to sketch folder or .ino"),
           fqbn: str = typer.Option(None, help="Fully qualified board name (fqbn)")):
    """Compile & upload a sketch using arduino-cli (requires arduino-cli installed)"""
    success = uploader.upload_sketch(port, sketch, fqbn)
    if not success:
        raise typer.Exit(code=1)

@app.command()
def live(port: str = typer.Argument(..., help="Port to open shell"),
         baud: int = typer.Option(115200, help="Baud rate")):
    """Open interactive live shell (REPL-like)"""
    shell.start_shell(port, baud)

if __name__ == "__main__":
    app()
