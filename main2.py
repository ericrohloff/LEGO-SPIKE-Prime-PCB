import network
import socket
from machine import UART, Pin
import time
import gc

# Setup UART
uart = UART(1, baudrate=9600, tx=Pin(21), rx=Pin(20))

# Setup Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="SPIKE-UART", password="12345678")
print("Starting AP...")
while not ap.active():
    pass
print("AP active at:", ap.ifconfig()[0])

# HTML form
html = """<!DOCTYPE html>
<html>
<head><title>SPIKE LED Sender</title></head>
<body>
  <h2>Send a Message to SPIKE</h2>
  <form method="POST">
    <input name="message" type="text" placeholder="HELLO" maxlength="32" />
    <input type="submit" value="Send" />
  </form>
</body>
</html>
"""

# Web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)


def send_message(text):
    print("Sending message:", text)
    for c in text:
        uart.write(c + "\n")  # newline-separated characters
        time.sleep(2.1)       # allow SPIKE to display + clear


while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    req = cl.recv(1024).decode()

    if "POST" in req:
        try:
            content = req.split("\r\n\r\n", 1)[1]
            if "message=" in content:
                msg = content.split("message=")[1]
                msg = msg.replace("+", " ").strip()
                send_message(msg)
        except Exception as e:
            print("Error parsing POST:", e)

    cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
    cl.send(html)
    cl.close()
    gc.collect()
