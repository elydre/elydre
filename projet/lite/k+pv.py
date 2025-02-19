import math

pe = {
"hiver": "fr",
"loup": "fr",
"reines": "fr",
"nordique": "fr",
"winter": "al",
"schloss": "al",
"konigiennen": "al",
"nordisch": "al",
}

def nb_voyelles(mot):
    nb_voyelles = 0
    for lettre in mot:
        if lettre in "aeiouy":
            nb_voyelles += 1
    return nb_voyelles

def proche_voisins(echantillon, mot_mystere):
    def distance(mot):
        return math.sqrt((len(mot) - len(mot_mystere))**2 + (nb_voyelles(mot) - nb_voyelles(mot_mystere))**2)

    mot_tries = sorted(echantillon, key=distance)
    voisin = {}
    for i in range(4):
        mot = mot_tries[i]
        voisin[mot] = echantillon[mot]
    return voisin

def res(voisin):
    exit = {}
    for lang in voisin:
        try:
            exit[voisin[lang]] += 1
        except KeyError:
            exit[voisin[lang]] = 1
    return exit


print(proche_voisins(pe, "anoure"))
print(res(proche_voisins(pe, "anoure")))
