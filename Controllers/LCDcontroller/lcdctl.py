from rpi_lcd import LCD
from time import sleep
from gpiozero import CPUTemperature
import psutil
from datetime import datetime

interface = "eth0"
last_reset_time = None
last_rx_bytes = None
last_tx_bytes = None

lcd = LCD()

def reset_stats():

    global last_reset_time, last_rx_bytes, last_tx_bytes
    last_reset_time = datetime.now()
    last_rx_bytes = psutil.net_io_counters(pernic=True)[interface].bytes_recv
    last_tx_bytes = psutil.net_io_counters(pernic=True)[interface].bytes_sent

def get_network_stats(p):
    global last_reset_time, last_rx_bytes, last_tx_bytes
    try:
        current_time = datetime.now()
        if current_time.hour == 0 and current_time.minute == 0:
            if last_reset_time is None or last_reset_time.date() != current_time.date():
                reset_stats()  # Reset stats if the day has changed
        net_io = psutil.net_io_counters(pernic=True)

        if interface in net_io:
            current_rx_bytes = net_io[interface].bytes_recv
            current_tx_bytes = net_io[interface].bytes_sent
            if last_rx_bytes is None or last_tx_bytes is None:
                # Initialize the first run of the program with the current stats
                last_rx_bytes = current_rx_bytes
                last_tx_bytes = current_tx_bytes

            rp_kb = round((current_rx_bytes - last_rx_bytes) / 1024 / 1024)
            sp_kb = round((current_tx_bytes - last_tx_bytes) / 1024 / 1024)

            # Update the last bytes count
            last_rx_bytes = current_rx_bytes
            last_tx_bytes = current_tx_bytes

            if p == 'rx':
                return rp_kb
            elif p == 'tx':
                return sp_kb
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def is_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
def number_of_workers():
    process_name = "gunicorn"
    count = 0
    for proc in psutil.process_iter(['pid', 'name']):
        try:

            if process_name.lower() in proc.info['name'].lower():
                count += 1  # 
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):

            pass
    return int(count / 2)


def show():
    while True:
        ram = round(psutil.virtual_memory().used / 1024 / 1024)
        
        
    # RAM Display
        lcd.text(f'RAM: {ram} MB', 1)
        sleep(0.5)
    # CPU Display
        cpu = round(psutil.cpu_percent(interval=1),1)
        lcd.text(f'CPU: {cpu}%', 2)
        sleep(5)   
        lcd.clear()  
        cpu_temp = round(CPUTemperature().temperature)
    # CPU Temperature Display
        lcd.text(f'TEMP: {cpu_temp}C', 1)
        sleep(0.5)  
        

    # Network Statistics Display
        rx = get_network_stats("rx")
        tx = get_network_stats("tx")
        lcd.text(f'NET(S/R): {tx}/{rx} MB', 2)
        sleep(5)   
        lcd.clear()  

        lcd.text(f'VPN: {is_process_running("nginx")}', 1)
        sleep(0.5)   
        
    # Display NGINX status
        
        lcd.text(f'NGINX: {is_process_running("nginx")}', 2)
        sleep(5)   
        lcd.clear()  
    # Display Web workers count
        
        lcd.text(f'WEB: {number_of_workers()}W(s)', 1)
        sleep(0.5)
        

    # Display PIHOLE status
        
        lcd.text(f'PIHOLE: {is_process_running("pihole-FTL")}', 2)
        sleep(5)   
        lcd.clear()  
    # Display AV status
        
        lcd.text(f'AV: {is_process_running("clamd")}', 1)
        sleep(0.5)
        
    # Display Unbound status
        
        lcd.text(f'UB: {is_process_running("unbound")}', 2)
        sleep(5)   
        lcd.clear()  
    # Display SyncThing status
        lcd.text(f'SYNC: {is_process_running("syncthing")}', 1)
        sleep(0.5)
    # Display SHH tatus
        lcd.text(f'SSH: {is_process_running("dropbear")}', 2)
        sleep(5)  
        lcd.clear()  
        sleep(0.5)
show()