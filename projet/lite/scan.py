import contextlib
import itertools
import socket
import tkinter as tk
from _thread import start_new_thread
from time import sleep, time

# setings
old = "40.0.0.0"        # ip de départ
maxi = 90               # nb max de threads
port = 25565            # port a tester
timeout = 0.4           # timeout (s)

# tkinter gui
root = tk.Tk()
root.title("Scanner")
root.geometry("300x150")
root.resizable(False, False)
label_ip = tk.Label(root, font=("Arial", 15))
label_ip.place(x=0, y=0, width=300, height=50)
label_nb = tk.Label(root, font=("Arial", 15))
label_nb.place(x=0, y=50, width=300, height=50)
label_is = tk.Label(root, font=("Arial", 15))
label_is.place(x=0, y=100, width=300, height=50)

def refresh():
    label_ip.config(text=f"checking: {ip}")
    label_nb.config(text=f"run: {nb}")
    label_is.config(text=f"ip/s: {round(long / (time() - debut), 2)}")
    root.after(100, refresh)


def chek_ip(ip):
    global nb
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    with contextlib.suppress(socket.timeout):
        debut = time()
        s.connect((ip, port))
        print(f"{round(time() - debut, 1)}s - {ip}")
    nb -= 1
    
todo, nb, long, ip, debut = [], 0, 0, "", time()
old = [int(e) for e in old.split(".")]

def start_scan():
    global nb, long, ip
    for a, b, c in itertools.product(range(old[0], 255), range(4, 255), range(4, 255)):
        if a < old[0] or (a == old[0] and b < old[1]) or (a == old[0] and b == old[1] and c < old[2]):
            continue

        todo.extend(f"{a}.{b}.{c}.{d}" for d in range(4, 255))

        ip = f"{a}.{b}.{c}.X"

        for e in todo:
            while nb >= maxi:
                sleep(0.05)

            nb += 1
            long += 1

            start_new_thread(chek_ip, (e,))

        todo.clear()

start_new_thread(start_scan, ())
sleep(0.5)
refresh()

root.mainloop()
