from multiprocessing import Pool
from os import cpu_count
from time import time

def mers(entree):   #fonction de Loris_redsrone pour touvé les nombres de mersenne
    nombre_s = entree - 2
    mers_entree = ( 2 ** entree ) - 1
    s = 4
    for _ in range(nombre_s):
        s = ( ( s ** 2 ) - 2 ) % mers_entree
    if s == 0:
        print("2^", entree, "-1 est premier")

if __name__ == '__main__':
    a = int(input("entrez x pour rechercher tout les nombres de 2^0 a 2^x\n-> "))

    #liste des nombre a calculé en mp
    ac = list(range(a))

    debut = time()
    with Pool(cpu_count()) as p:  # on lance sur 
        p.map(mers, ac)
    print(f"fin du calcul {round(time()-debut,2)}s")