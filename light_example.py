from machine import UART, Pin
import time
from port import PORT
from lights import LIGHTS

p = PORT(1)
uart = UART(p.uart)
uart.init(baudrate=9600, timeout=1000)

lights = LIGHTS()

font_5x5 = {
    'A': ["01110", "10001", "11111", "10001", "10001"],
    'B': ["11110", "10001", "11110", "10001", "11110"],
    'C': ["01111", "10000", "10000", "10000", "01111"],
    'D': ["11110", "10001", "10001", "10001", "11110"],
    'E': ["11111", "10000", "11110", "10000", "11111"],
    'F': ["11111", "10000", "11110", "10000", "10000"],
    'G': ["01111", "10000", "10111", "10001", "01110"],
    'H': ["10001", "10001", "11111", "10001", "10001"],
    'I': ["01110", "00100", "00100", "00100", "01110"],
    'J': ["00001", "00001", "00001", "10001", "01110"],
    'K': ["10001", "10010", "11100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10011", "10001"],
    'O': ["01110", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "11110", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10011", "01111"],
    'R': ["11110", "10001", "11110", "10010", "10001"],
    'S': ["01111", "10000", "01110", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10101", "11011", "10001"],
    'X': ["10001", "01010", "00100", "01010", "10001"],
    'Y': ["10001", "01010", "00100", "00100", "00100"],
    'Z': ["11111", "00010", "00100", "01000", "11111"],
    ' ': ["00000", "00000", "00000", "00000", "00000"]
}


def build_buffer(text):
    text = text.upper()
    rows = [[] for _ in range(5)]
    for idx, ch in enumerate(text):
        glyph = font_5x5.get(ch, font_5x5[' '])
        for y in range(5):
            rows[y].extend(int(bit) for bit in glyph[y])
            if idx < len(text) - 1:
                rows[y].append(0)
    for y in range(5):
        rows[y].extend([0] * 5)
    return rows


def draw_window(buffer_rows, start_col):
    for x in range(5):
        src_col = start_col + x
        for y in range(5):
            val = 0
            if 0 <= src_col < len(buffer_rows[0]):
                val = buffer_rows[y][src_col]
            lights.matrix_led(x, y, val)
    lights.display_update()


def scroll_text(text, speed=0.04):
    buf = build_buffer(text)
    total_cols = len(buf[0])

    for offset in range(total_cols - 4):
        draw_window(buf, offset)
        time.sleep(speed)

    for y in range(5):
        for x in range(5):
            lights.matrix_led(x, y, 0)
    lights.display_update()


print("SPIKE: Scrolling ready on PORT(1)...")

while True:
    if uart.any():
        msg = uart.read(uart.any())
        if msg:
            try:
                full_msg = msg.decode().strip()
                print("Scrolling:", full_msg)
                scroll_text(full_msg)
            except Exception as e:
                print("Decode error:", e)
    time.sleep(0.1)
