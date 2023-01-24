import contextlib
import itertools
import socket
from _thread import start_new_thread
from time import sleep, time


# setings
old = "10.0.0.0"        # ip de départ
maxi = 800             # nb max de threads
port = 25565
timeout = 0.1


def chek_ip(ip):
    global nb
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    with contextlib.suppress(socket.timeout):
        s.connect((ip, port))
    nb -= 1

def print_info():
    while True:
        print(f"run: {' ' * (len(str(maxi)) - len(str(nb)))}{nb}, ip/s: {round(long / (time() - debut))}")
        sleep(0.3)
    
todo, nb, long, debut = [], 0, 0, time()
old = [int(e) for e in old.split(".")]

start_new_thread(print_info, ())

for a, b, c in itertools.product(range(old[0], 255), range(4, 255), range(4, 255)):
    if a < old[0] or (a == old[0] and b < old[1]) or (a == old[0] and b == old[1] and c < old[2]):
        continue

    todo.extend(f"{a}.{b}.{c}.{d}" for d in range(4, 255))


    for e in todo:
        while nb >= maxi:
            sleep(0.05)

        nb += 1
        long += 1

        start_new_thread(chek_ip, (e,))

    todo.clear()
