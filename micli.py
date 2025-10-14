import serial, serial.tools.list_ports
import argparse, os, sys, time

HISTORY = []

def get_port():
    ports = [p.device for p in serial.tools.list_ports.comports()]
    if not ports:
        print("⚠️ No ports found.")
        sys.exit(1)
    print("🔌 Available ports:")
    for i, p in enumerate(ports):
        print(f" [{i}] {p}")
    choice = input("Select port index: ")
    try:
        return ports[int(choice)]
    except:
        print("Invalid choice.")
        sys.exit(1)

def connect(port, baud=115200):
    try:
        ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2)  # wait for reset
        print(f"✅ Connected to {port}")
        return ser
    except serial.SerialException as e:
        print(f"❌ {e}")
        sys.exit(1)

def send_command(ser, cmd):
    ser.write((cmd + "\n").encode())
    time.sleep(0.05)
    while ser.in_waiting:
        print(ser.readline().decode().strip())
    HISTORY.append(cmd)

def repl(ser):
    print("💬 micli REPL — type 'exit' to quit.")
    while True:
        try:
            cmd = input("micli> ").strip()
            if cmd.lower() in ["exit", "quit"]:
                break
            if cmd:
                send_command(ser, cmd)
        except KeyboardInterrupt:
            break
    print("👋 Exiting REPL.")

def run_file(ser, path):
    if not os.path.exists(path):
        print("File not found.")
        return
    with open(path) as f:
        for line in f:
            cmd = line.strip()
            if cmd:
                print(f"→ {cmd}")
                send_command(ser, cmd)

def save_history(name):
    with open(name + ".ino", "w") as f:
        f.write("void setup(){\n  Serial.begin(115200);\n}\nvoid loop(){\n")
        for cmd in HISTORY:
            f.write(f"  // {cmd}\n")
        f.write("}\n")
    print(f"💾 Saved to {name}.ino")

def main():
    parser = argparse.ArgumentParser(description="micli — Microcontroller REPL CLI")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("repl")
    evalp = sub.add_parser("eval")
    evalp.add_argument("expr")

    runp = sub.add_parser("run")
    runp.add_argument("file")

    sub.add_parser("save")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        sys.exit(0)

    port = get_port()
    ser = connect(port)

    if args.cmd == "repl":
        repl(ser)
    elif args.cmd == "eval":
        send_command(ser, args.expr)
    elif args.cmd == "run":
        run_file(ser, args.file)
    elif args.cmd == "save":
        save_history("micli_session")

if __name__ == "__main__":
    main()
