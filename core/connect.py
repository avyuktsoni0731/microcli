# microcli/core/connect.py
import serial
import threading
import time
from rich.console import Console

console = Console()

class SerialConnection:
    def __init__(self, port, baud=115200, reconnect=True):
        self.port = port
        self.baud = baud
        self.reconnect = reconnect
        self._ser = None
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._connect_thread = threading.Thread(target=self._ensure_connected, daemon=True)
        self._connect_thread.start()

    def _ensure_connected(self):
        while not self._stop.is_set():
            if self._ser and self._ser.is_open:
                time.sleep(0.5)
                continue
            try:
                self._ser = serial.Serial(self.port, self.baud, timeout=1)
                console.print(f"[green]✔ Connected to {self.port} @ {self.baud}[/green]")
                # give device time to reset if needed
                time.sleep(0.2)
            except Exception as e:
                console.print(f"[yellow]⚠ Could not open {self.port}: {e}[/yellow]")
                if not self.reconnect:
                    break
                time.sleep(2)

    def send(self, text: str):
        with self._lock:
            try:
                if not self._ser or not self._ser.is_open:
                    raise serial.SerialException("Port not open")
                self._ser.write((text + "\n").encode())
            except Exception as e:
                console.print(f"[red]❌ Send failed: {e}[/red]")

    def read_line(self) -> str:
        if not self._ser or not self._ser.is_open:
            return ""
        try:
            raw = self._ser.readline()
            return raw.decode(errors="ignore").rstrip("\r\n")
        except Exception:
            return ""

    def read_all(self) -> str:
        if not self._ser or not self._ser.is_open:
            return ""
        try:
            return self._ser.read_all().decode(errors="ignore")
        except Exception:
            return ""

    def close(self):
        self._stop.set()
        if self._ser and self._ser.is_open:
            try:
                self._ser.close()
            except Exception:
                pass
        console.print("[blue]🔌 Serial connection closed[/blue]")
