import psutil
import time
while True:
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    print(f"RAM: {ram.available/ 1024 / 1024}/{ram.total/ 1024 / 1024}")
    print(f"SWAP: {swap.free/ 1024 / 1024}/{swap.total/ 1024 / 1024}")
    time.sleep(0.5)