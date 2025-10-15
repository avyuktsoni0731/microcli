# microcli/core/uploader.py
import subprocess
from rich.console import Console
console = Console()

def upload_sketch(port: str, sketch_path: str, fqbn: str = None):
    """
    Upload a sketch using arduino-cli.
    If user doesn't provide fqbn, we try to hint them.
    Requires arduino-cli installed and in PATH.
    """
    if fqbn is None:
        console.print("[yellow]No --fqbn provided. You must pass board fqbn or run 'arduino-cli board list' to find it.[/yellow]")
        return False

    # Compile
    cmd_compile = ["arduino-cli", "compile", "--fqbn", fqbn, sketch_path]
    console.print("[blue]⌛ Compiling...[/blue]")
    r = subprocess.run(cmd_compile, capture_output=True, text=True)
    if r.returncode != 0:
        console.print(f"[red]Compile failed:[/red]\n{r.stderr}")
        return False
    console.print("[green]✔ Compile successful[/green]")

    # Upload
    cmd_upload = ["arduino-cli", "upload", "-p", port, "--fqbn", fqbn, sketch_path]
    console.print("[blue]⬆ Uploading...[/blue]")
    r = subprocess.run(cmd_upload, capture_output=True, text=True)
    if r.returncode != 0:
        console.print(f"[red]Upload failed:[/red]\n{r.stderr}")
        return False
    console.print("[green]🎉 Upload successful[/green]")
    return True
