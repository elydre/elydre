import contextlib
import os

toconvert = input("text a convertire: ")

cars = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

if sum(True for t in toconvert if t not in cars) != 0:
    print("caractere invalide")
    exit()

fonts = os.listdir('fonts')

for fron in fonts:
    with contextlib.suppress(UnicodeDecodeError):
        with open(f'fonts/{fron}', 'r') as fichier:
            fichier_contenu = fichier.read()

        artcar = "&".join([l[:-1] for l in fichier_contenu.split('\n') if l.endswith('@')]).split('@')

        if len(artcar) >= len(cars):
            sortie = []
            for t in toconvert:
                for i in range(len(cars)):
                    if t == cars[i]:
                        sortie.append(artcar[i])
                        break


            for i in range(len(sortie[0])):
                entrer = False
                for j in sortie:
                    with contextlib.suppress(IndexError):
                        toprint = str(j).split('&')[i].replace('$', ' ')
                        if toprint != '':
                            entrer = True
                            print(toprint, end='')
                if entrer: print()