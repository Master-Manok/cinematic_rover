import subprocess
import time
import smbus  # For I2C communication
import lcd_class as lc

# I2C address of the LCD (usually 0x27, but check with your module)
LCD_ADDRESS = 0x27
# I2C bus (usually 1 on a Raspberry Pi)
pi_REV = 2

# Initialize I2C bus
try:
    lcd= lc.LCD(pi_REV,LCD_ADDRESS,True)
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
        result = subprocess.run(['hostname','-I'], capture_output=True, text=True, timeout=10)
        ip_address = result.stdout.strip().split()[0]
        if result.returncode == 0 and ip_address:
            return ip_address
        else:
            return "No Internet"
    except subprocess.TimeoutExpired:
        return "No Internet"
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return "No Internet"

def main():
    """
    Main function to display IP address on the LCD.
    """

    while True:
        ip_address = get_ip()
        lcd.clear()
        lcd.message("LOCAL IP:",1)
        lcd.message(ip_address,2)
        time.sleep(5)  # Update every 5 seconds

if __name__ == "__main__":
    main()

