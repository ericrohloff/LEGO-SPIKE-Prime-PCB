from machine import UART, Pin
import time
from port import PORT

# Initialize UART on PORT(1) which is Port B on the SPIKE
p = PORT(1)
uart = UART(p.uart)
uart.init(baudrate=9600, timeout=1000)

print("UART initialized and listening...")

while True:
    if uart.any():
        msg = uart.read(uart.any())
        if msg:
            try:
                print("Received:", msg.decode().strip())
            except UnicodeDecodeError:
                print("Unreadable:", msg)
    time.sleep(0.1)
