from time import time, sleep
from random import randint
from _thread import start_new_thread
from multiprocessing import Pool
from os import cpu_count
from time import time

def mptest(entree):
    nombre_s = entree - 2
    mers_entree = ( 2 ** entree ) - 1
    s = 4
    for _ in range(nombre_s):
        s = ((s ** 2) - 2) % mers_entree

def iptest():
    iptest_sc = 0
    iptest_debut = time()
    while time() - iptest_debut < 2:
        iptest_sc += 1
    return round(iptest_sc / 500000,1)

def adtest():
    stop = 0
    y = 0
    num = 0
    debut = time()
    while stop == 0:
        for _ in range(10000):
            num += 1
        y += 1
        fin = time()
        temps = fin - debut
        if temps > 10:
            y /= 100
            stop = 1
    return(y)

def rdtest():
    fin = 0
    stop = 0
    y = 0
    debut = time()
    while stop == 0:
        for _ in range(10000): num = randint(0, 1000000000)
        y += 1
        fin = time()
        temps = fin - debut
        if temps > 10:
            y /= 100
            stop = 1
    return(y)

def bctest():
    y = 0
    debut = time()
    while y < 10**8:
        y += 1
    bcwhile = round(time() - debut,3)

    print(" while: ", bcwhile, "s. les 100G boucles")

    y = 0
    debut = time()
    for _ in range(10**8):
        y += 1
    bcfor = round(time() - debut,3)

    print(" for:   ", bcfor, "s. les 100G boucles")

def thstart():
    global thn
    thn = 10000

    def thtest(nb):
        global thn
        nb ** nb
        thn -= 1

    def thlauncher():
        for x in range(10000): start_new_thread(thtest,(x,))

    start_new_thread(thlauncher,())

    pt = 100
    while thn != 0: sleep(0.05); pt -= 1
    return(pt)

def mpstart(cores):
    debut = time()
    liste = list(range(3000))
    with Pool(cores) as p: (p.map(mptest, liste))

    return round(time()-debut,3)


if __name__ == '__main__':
    print("DEBUT DES TESTS")

    print(" ~~~~ ad test ~~~~ ")
    print(" ->", adtest(),"pts")

    print(" ~~~~ rd test ~~~~ ")
    print(" ->", rdtest(),"pts")

    print(" ~~~~ ip test ~~~~ ")
    print(" ->", iptest(),"pts")

    print(" ~~~~ th test ~~~~ ")
    print(" ->", thstart(),"pts")

    print(" ~~~~ mp test ~~~~ ")
    print( " 1 core: ", mpstart(1),"s.")
    print(f" {cpu_count()} core: ", mpstart(cpu_count()),"s.")

    print(" ~~~~ bc test ~~~~ ")
    bctest()

    input("FIN DES TESTS")