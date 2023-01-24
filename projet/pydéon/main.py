import time
from _thread import start_new_thread

import keyboard

from mod.player import Play

import mod.res1 as r1
import mod.res2 as r2

def map_touche(touche, fichier):
    start_new_thread(RUN_touche, (touche, fichier))

def RUN_touche(touche, fichier):
    while True:
        while keyboard.is_pressed(touche):
            if not fichier.runing:
                print(fichier.nom.replace(".wav", "").replace("!","#"))
                fichier.play()
            time.sleep(0.1)
        if fichier.runing:
            fichier.stop()
        time.sleep(0.1)

if input("Disposition 1/2 -> ") == "1":
    nom = r1.nom
    ordre_touches = r1.ordre_touches
else:
    nom = r2.nom
    ordre_touches = r2.ordre_touches

for i in range(len(nom)):
    map_touche(ordre_touches[i], Play(nom[i]))

while True:
    time.sleep(1)