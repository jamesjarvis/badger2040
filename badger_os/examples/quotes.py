import badger2040
import gc
import json
import time
import random


# LETS START FROM SCRATCH

TOTAL_QUOTES = int(2042)
text_file = "quotes/quotes.txt"
try:
    open(text_file, "r")
except OSError:
    try:
        # If the specified file doesn't exist,
        # pre-populate with Quotes.
        import quoteslist
        with open(text_file, "wb") as f:
            f.write(quoteslist.data())
            f.flush()
            time.sleep(0.1)
        del quoteslist
    except ImportError:
        pass

gc.collect()

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

TEXT_PADDING = 4
TEXT_WIDTH = WIDTH - TEXT_PADDING - TEXT_PADDING
TEXT_SIZE = 0.55

FONT = "sans"
FONT_THICKNESS = 2

text_spacing = int(34 * TEXT_SIZE)
# Create a new Badger and set it to update MEDIUM.
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_MEDIUM)
display.set_font(FONT)
display.set_thickness(FONT_THICKNESS)


def display_random_quote():
    display.set_pen(15)
    display.clear()
    # Open the quotes file.
    quotes = open(text_file, "r")

    n = random.randint(0, TOTAL_QUOTES)
    for i in range(n):
        quotes.readline()

    current_quote_json = json.loads(quotes.readline())
    # Read a full line and split it into words.
    words = current_quote_json["content"].split(" ")

    lines = []
    latest_line = ""
    for word in words:
        latest_line_length = display.measure_text(latest_line + word, TEXT_SIZE)
        if latest_line_length >= TEXT_WIDTH:
            lines.append(latest_line)
            latest_line = ""
        latest_line += word
        latest_line += " "

    lines.append(latest_line)

    lines.append(current_quote_json["author"])

    row = 0
    for line in lines:
        y = int(row * text_spacing) + int(text_spacing // 2) + TEXT_PADDING
        display.set_pen(0)
        display.text(line, TEXT_PADDING, y, TEXT_WIDTH, TEXT_SIZE)
        row += 1
    display.update()


# Main program loop
changed = True
while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()

    if display.pressed(badger2040.BUTTON_A):
        changed = True

    if changed:
        display_random_quote()

        changed = False

    display.halt()
