import serial
import logging
from time import sleep
from serial.serialutil import SerialException

logging.basicConfig(filename="logs/plantcare.log", level=logging.DEBUG, filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

def connect_serial():
    """Attempt to connect to the serial device."""
    while True:
        try:
            serialCom = serial.Serial(SERIAL_PORT, BAUD_RATE)
            serialCom.setDTR(False)
            sleep(1)
            serialCom.flushInput()
            serialCom.setDTR(True)
            logger.info(f"Serial communication established on {SERIAL_PORT} at {BAUD_RATE} baud rate")
            return serialCom
        except SerialException as e:
            logger.warning(f"Serial connection failed: {e}. Retrying in 5 seconds...")
            sleep(5)

serialCom = connect_serial()
logger.info("Plantcare script started")

while True:
    try:
        if serialCom.is_open:
            s_bytes = serialCom.readline()
            decoded_bytes = s_bytes.decode("utf-8").strip('\r\n').split(',')
            logger.info(f"Received data: Humidity: {decoded_bytes[1]}%, Raw Value: {decoded_bytes[0]}, Dry-Wet Range: 505 - 220")
        else:
            raise SerialException("Serial port closed unexpectedly.")
    except (SerialException, OSError) as e:
        logger.error(f"Serial communication error: {e}. Attempting to reconnect...")
        try:
            serialCom.close()
        except Exception:
            pass
        serialCom = connect_serial()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    sleep(1)
