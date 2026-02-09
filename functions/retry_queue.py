
import threading, time
def start():
    def w():
        while True: time.sleep(5)
    threading.Thread(target=w, daemon=True).start()
