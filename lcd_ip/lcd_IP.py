import subprocess
import time
import smbus  # For I2C communication

# I2C address of the LCD (usually 0x27, but check with your module)
LCD_ADDRESS = 0x27
# I2C bus (usually 1 on a Raspberry Pi)
I2C_BUS = 1

# Define LCD commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# Define flags for display control
LCD_DISPLAYON = 0x04
LCD_CURSORON = 0x02
LCD_BLINKON = 0x01

# Define flags for entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Define flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Initialize I2C bus
try:
    bus = smbus.SMBus(I2C_BUS)
except Exception as e:
    print(f"Error initializing I2C bus: {e}")
    exit()  # Exit if I2C bus initialization fails

def get_ip():
    """
    Retrieves the external IP address of the Raspberry Pi.

    Returns:
        str: The external IP address, or "No Internet" if the connection fails.
    """
    try:
        # Use a reliable external server to check connectivity.
        # Using dig and a DNS resolver is more robust than relying on a single website.
        result = subprocess.run(['dig', '+short', 'myip.opendns.com', '@resolver1.opendns.com'], capture_output=True, text=True, timeout=10)
        ip_address = result.stdout.strip()
        if result.returncode == 0 and ip_address:
            return ip_address
        else:
            return "No Internet"
    except subprocess.TimeoutExpired:
        return "No Internet"
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return "No Internet"

def lcd_init():
    """
    Initializes the 16x2 LCD display.
    """
    try:
        lcd_byte(0x33, False)  # Initialise
        lcd_byte(0x32, False)  # Initialise
        lcd_byte(0x06, False)  # Display on, cursor on
        lcd_byte(0x0C, False)  # Cursor move direction
        lcd_byte(0x28, False)  # 4-bit, 2 line, 5x8 font
        lcd_byte(LCD_CLEARDISPLAY, False)  # Clear display
        time.sleep(0.05)
    except Exception as e:
        print(f"Error initializing LCD: {e}")
        return False # Return False if initialization fails

    return True # Return True if initialization is successful

def lcd_byte(bits, data):
    """
    Sends a byte to the LCD in 4-bit mode.

    Args:
        bits (int): The data byte to send.
        data (bool): True for data, False for command.
    """
    try:
        bits_high = bits & 0xF0
        bits_low = (bits << 4) & 0xF0

        # Send the high nibble
        bus.write_byte_data(LCD_ADDRESS, 0, bits_high | (1 << 2) | (1 if data else 0))
        bus.write_byte_data(LCD_ADDRESS, 0, bits_high | (1 << 2) | (1 if data else 0) | (1 << 4))
        bus.write_byte_data(LCD_ADDRESS, 0, bits_high)

        # Send the low nibble
        bus.write_byte_data(LCD_ADDRESS, 0, bits_low | (1 << 2) | (1 if data else 0))
        bus.write_byte_data(LCD_ADDRESS, 0, bits_low | (1 << 2) | (1 if data else 0) | (1 << 4))
        bus.write_byte_data(LCD_ADDRESS, 0, bits_low)
    except Exception as e:
        print(f"Error sending byte to LCD: {e}")
        return False # Return False on error
    return True

def lcd_string(message, line):
    """
    Sends a string to the LCD.

    Args:
        message (str): The string to display (max 16 characters per line).
        line (int): The line number (1 or 2).
    """
    message = message.ljust(16, " ")  # Pad with spaces to fill the line
    try:
        lcd_byte(LCD_SETDDRAMADDR | (0x00 if line == 1 else 0x40), False)
        for i in range(16):
            lcd_byte(ord(message[i]), True)
    except Exception as e:
        print(f"Error sending string to LCD: {e}")
        return False
    return True

def main():
    """
    Main function to display IP address on the LCD.
    """
    if not lcd_init():
        print("LCD initialization failed. Please check the I2C connection and address.")
        return  # Exit if LCD initialization failed

    lcd_string("Initializing...", 1)
    lcd_string("", 2) #Clear second line

    while True:
        ip_address = get_ip()
        lcd_string("IP Address:", 1)
        lcd_string(ip_address, 2)
        time.sleep(5)  # Update every 5 seconds

if __name__ == "__main__":
    main()

