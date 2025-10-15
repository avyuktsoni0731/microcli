#include <Arduino.h>

String incoming = "";

void setup()
{
    Serial.begin(115200);
    while (!Serial)
    {
    }
    pinMode(LED_BUILTIN, OUTPUT);
    Serial.println("🔌 MicroCLI Runtime Ready!");
}

void loop()
{
    while (Serial.available())
    {
        char c = Serial.read();
        if (c == '\n' || c == '\r')
        {
            processCommand(incoming);
            incoming = "";
        }
        else
        {
            incoming += c;
        }
    }
}

void processCommand(String cmd)
{
    cmd.trim();

    if (cmd.startsWith("EVAL "))
    {
        String code = cmd.substring(5);
        Serial.println("⚙️ Executing code block:");
        Serial.println(code);
        // In a real interpreter, we'd parse & execute here.
        Serial.println("✅ Done.");
    }
    else if (cmd == "LED ON")
    {
        digitalWrite(LED_BUILTIN, HIGH);
        Serial.println("💡 LED turned ON");
    }
    else if (cmd == "LED OFF")
    {
        digitalWrite(LED_BUILTIN, LOW);
        Serial.println("🌙 LED turned OFF");
    }
    else if (cmd == "PING")
    {
        Serial.println("🏓 Pong!");
    }
    else
    {
        Serial.print("❌ Unknown command: ");
        Serial.println(cmd);
    }
}
