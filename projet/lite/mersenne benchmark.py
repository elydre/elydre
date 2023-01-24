from time import time
from multiprocessing import Pool
from os import cpu_count
from time import time

def fin(debut):
    return round(time()-debut,3)

def mptest(entree):   #fonction pour touvé les nombres de mersenne
    nombre_s = entree - 2
    mers_entree = ( 2 ** entree ) - 1
    s = 4
    for _ in range(nombre_s):
        s = ((s ** 2) - 2) % mers_entree
    # if s == 0:
    #     print("2^", entree, "-1 est premier")

if __name__ == '__main__':

    nbcore = cpu_count()
    liste = [x for x in range(4000)]

    print("START OF TESTS")

    debut = time()

    for l in liste:
        mptest(l)

    simple, debut = fin(debut), time()

    with Pool(nbcore) as p: 
        (p.map(mptest, liste))

    multi = fin(debut)
    factor = round(simple/multi,3)
    efficiency = round(factor/nbcore*100,3)

    print(f"1 core: {simple} s.")    
    print(f"{nbcore} core: {multi} s.")
    print(f"factor: {factor}")
    print(f"efficiency: {efficiency}%")