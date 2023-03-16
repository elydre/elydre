print("Test 1...")
verifie = lambda tab : tab == sorted(tab)
assert verifie([0, 5, 8, 8, 9]) == True
assert verifie([8, 12, 4]) == False
assert verifie([-1, 4]) == True
assert verifie([5]) == True
print("Test 1 passé")

print("Test 2...")
indices_maxi = lambda tab : (max(tab), [i for i in range(len(tab)) if tab[i] == max(tab)])
assert indices_maxi([1, 5, 6, 9, 1, 2, 3, 7, 9, 8]) == (9, [3, 8])
assert indices_maxi([7]) == (7, [0])
print("Test 2 passé")

print("Test 3...")
moyenne = lambda tab: sum(map(lambda a: a[0] * a[1], tab)) / sum(a[1] for a in tab) if sum(a[1] for a in tab) else None
assert moyenne([(8, 2), (12, 0), (13.5, 1), (5, 0.5)]) == 9.142857142857142
assert moyenne([(3, 0), (5, 0)]) is None
print("Test 3 passé")

print("Test 4...")
a_doublon = lambda tab : list(set(tab)) != tab
assert a_doublon([]) == False
assert a_doublon([1]) == False
assert a_doublon([1, 2, 4, 6, 6]) == True
assert a_doublon([2, 5, 7, 7, 7, 9]) == True
assert a_doublon([0, 2, 3]) == False
print("Test 4 passé")

print("Test 5...")
lancer = lambda n : [__import__("random").randint(1, 6) for _ in range(n)]
paire_6 = lambda tab : tab.count(6) >= 2
print("Test 5 passé")

print("Test 6...")
recherche = lambda tab, nb : len(tab) - 1 - tab[::-1].index(nb) if nb in tab else len(tab)
assert recherche([5, 3], 1) == 2
assert recherche([2, 4], 2) == 0
assert recherche([2, 3, 5, 2, 4], 2) == 3
print("Test 6 passé")

print("Test 7...")
fusion = lambda tab1, tab2 : sorted(tab1 + tab2)
assert fusion([3, 5], [2, 5]) == [2, 3, 5, 5]
assert fusion([-2, 4], [-3, 5, 10]) == [-3, -2, 4, 5, 10]
assert fusion([4], [2, 6]) == [2, 4, 6]
print("Test 7 passé")

print("Test 8...")
max_dico = lambda dico : [(k, v) for k, v in dico.items() if v == max(dico.values())][0]
assert max_dico({'Bob': 102, 'Ada': 201, 'Alice': 103, 'Tim': 50}) == ('Ada', 201)
assert max_dico({'Alan': 222, 'Ada': 201, 'Eve': 220, 'Tim': 50}) == ('Alan', 222)
print("Test 8 passé")

print("Test 9...")
multiplication = lambda a, b : sum(a for _ in range(b))
assert multiplication(3, 5) == 15
print("Test 9 passé")

print("Test 10...")
maxliste = lambda tab : max(tab) if tab else None
assert maxliste([98, 12, 104, 23, 131, 9]) == 131
assert maxliste([-27, 24, -3, 15]) == 24
print("Test 10 passé")

print("Test 11...")
convertir = lambda tab : int("".join(str(x) for x in tab), 2)
assert convertir([1, 0, 1, 0, 0, 1, 1]) == 83
assert convertir([1, 0, 0, 0, 0, 0, 1, 0]) == 130
print("Test 11 passé")

print("Test 13...")
recherche = lambda nb, tab: sum(x == nb for x in tab)
assert recherche(5, []) == 0
assert recherche(5, [-2, 3, 4, 8]) == 0
assert recherche(5, [-2, 3, 1, 5, 3, 7, 4]) == 1
assert recherche(5, [-2, 5, 3, 5, 4, 5]) == 3
print("Test 13 passé")

print("Test 14...")
mini = lambda tmoy, annees : (tmoy[tmoy.index(min(tmoy))], annees[tmoy.index(min(tmoy))])
assert mini([14.9, 13.3, 13.1, 12.5, 13.0, 13.6, 13.7], [2013, 2014, 2015, 2016, 2017, 2018, 2019]) == (12.5, 2016)
print("Test 14 passé")

print("Test 16...")
recherche_indices_classement = lambda elt, tab : ([i for i in range(len(tab)) if tab[i] < elt], [i for i in range(len(tab)) if tab[i] == elt], [i for i in range(len(tab)) if tab[i] > elt])
assert recherche_indices_classement(3, [1, 3, 4, 2, 4, 6, 3, 0]) == ([0, 3, 7], [1, 6], [2, 4, 5])
assert recherche_indices_classement(3, [1, 4, 2, 4, 6, 0]) == ([0, 2, 5], [], [1, 3, 4])
assert recherche_indices_classement(3, [1, 1, 1, 1]) == ([0, 1, 2, 3], [], [])
assert recherche_indices_classement(3, []) == ([], [], [])
print("Test 16 passé")

print("Test 17...")
moyenne = lambda tab: sum(map(lambda a: a[0] * a[1], tab)) / sum(a[1] for a in tab) if sum(a[1] for a in tab) else None
print("Test 17 passé")

print("Test 18...")
max_et_indice = lambda tab : (sorted(tab)[-1], tab.index(sorted(tab)[-1]))
assert max_et_indice([1, 5, 6, 9, 1, 2, 3, 7, 9, 8]) == (9, 3)
assert max_et_indice([-2]) == (-2, 0)
assert max_et_indice([-1, -1, 3, 3, 3]) == (3, 2)
assert max_et_indice([1, 1, 1, 1]) == (1, 0)
print("Test 18 passé")

print("Test 19...")
recherche = lambda tab, n : tab.index(n) if n in tab else -1
assert recherche([2, 3, 4, 5, 6], 5) == 3
assert recherche([2, 3, 4, 6, 7], 5) == -1
print("Test 19 passé")

print("Test 20...")
ajoute_dictionnaires = lambda dic1, dic2 : {k: dic1.get(k, 0) + dic2.get(k, 0) for k in set(dic1) | set(dic2)}
assert ajoute_dictionnaires({1: 5, 2: 7}, {2: 9, 3: 11}) == {1: 5, 2: 16, 3: 11}
assert ajoute_dictionnaires({}, {2: 9, 3: 11}) == {2: 9, 3: 11}
assert ajoute_dictionnaires({1: 5, 2: 7}, {}) == {1: 5, 2: 7}
print("Test 20 passé")

print("Test 21...")
delta = lambda tab : [tab[0]] + [tab[i] - tab[i - 1] for i in range(1, len(tab))]
assert delta([1000, 800, 802, 1000, 1003]) == [1000, -200, 2, 198, 3]
assert delta([42]) == [42]
print("Test 21 passé")

print("Test 22...")
liste_puissances = lambda a, b : [a ** i for i in range(1, b+1)]
liste_puissances_borne = lambda a, borne : [a ** i for i in range(1, borne**2) if a ** i < borne]
assert liste_puissances(3, 5) == [3, 9, 27, 81, 243]
assert liste_puissances(-2, 4) == [-2, 4, -8, 16]
assert liste_puissances_borne(2, 16) == [2, 4, 8]
assert liste_puissances_borne(2, 17) == [2, 4, 8, 16]
assert liste_puissances_borne(5, 5) == []
print("Test 22 passé")

print("Test 23...")
selection_enclos = lambda tab, nb : [x for x in tab if x["enclos"] == nb]
assert selection_enclos([ {'nom':'Medor', 'espece':'chien', 'age':5, 'enclos':2}, {'nom':'Titine', 'espece':'chat', 'age':2, 'enclos':5}, {'nom':'Tom', 'espece':'chat', 'age':7, 'enclos':4}, {'nom':'Belle', 'espece':'chien', 'age':6, 'enclos':3}, {'nom':'Mirza', 'espece':'chat', 'age':6, 'enclos':5}], 5) == [{'nom':'Titine', 'espece':'chat', 'age':2, 'enclos':5}, {'nom':'Mirza', 'espece':'chat', 'age':6, 'enclos':5}]
assert selection_enclos([ {'nom':'Medor', 'espece':'chien', 'age':5, 'enclos':2}, {'nom':'Titine', 'espece':'chat', 'age':2, 'enclos':5}, {'nom':'Tom', 'espece':'chat', 'age':7, 'enclos':4}, {'nom':'Belle', 'espece':'chien', 'age':6, 'enclos':3}, {'nom':'Mirza', 'espece':'chat', 'age':6, 'enclos':5}], 2) == [{'nom':'Medor', 'espece':'chien', 'age':5, 'enclos':2}]
assert selection_enclos([ {'nom':'Medor', 'espece':'chien', 'age':5, 'enclos':2}, {'nom':'Titine', 'espece':'chat', 'age':2, 'enclos':5}, {'nom':'Tom', 'espece':'chat', 'age':7, 'enclos':4}, {'nom':'Belle', 'espece':'chien', 'age':6, 'enclos':3}, {'nom':'Mirza', 'espece':'chat', 'age':6, 'enclos':5}], 7) == []
print("Test 23 passé")

print("Test 24...")
nbr_occurrences = lambda string : {x: string.count(x) for x in string}
print("Test 24 passé")

print("Test 25...")
enumere = lambda tab : {i:[j for j in range(len(tab)) if tab[j] == i] for i in set(tab)}
assert enumere([1, 1, 2, 3, 2, 1]) == {1: [0, 1, 5], 2: [2, 4], 3: [3]}
print("Test 25 passé")

print("Test 26...")
multiplication = lambda a, b : a / (1 / b) if b != 0 else 0
assert multiplication(3, 5) == 15
assert multiplication(-4, -8) == 32
assert multiplication(-2, 6) == -12
assert multiplication(-2, 0) == 0
print("Test 26 passé")

print("Test 27...")
recherche_min = lambda tab : tab.index(min(tab))
assert recherche_min([5]) == 0
assert recherche_min([2, 4, 1]) == 2
assert recherche_min([5, 3, 2, 2, 4]) == 2
print("Test 27 passé")

print("Test 28...")
moyenne = lambda tab : sum(tab) / len(tab)
assert moyenne([1]) == 1
assert moyenne([1, 2, 3, 4, 5, 6, 7]) == 4
assert moyenne([1, 2]) == 1.5
print("Test 28 passé")

print("Test 30...")
moyenne = lambda tab : sum(tab) / len(tab)
assert moyenne([1.0]) == 1.0
assert moyenne([1.0, 2.0, 4.0]) == 2.3333333333333335
print("Test 30 passé")

print("Test 31...")
nb_repetitions = lambda nb, tab : tab.count(nb)
assert nb_repetitions(5, [2, 5, 3, 5, 6, 9, 5]) == 3
assert nb_repetitions('A', [ 'B', 'A', 'B', 'A', 'R']) == 2
assert nb_repetitions(12, [1, '! ', 7, 21, 36, 44]) == 0
print("Test 31 passé")

print("Test 32...")
min_et_max = lambda tab : {"min" : min(tab), "max" : max(tab)}
assert min_et_max([0, 1, 4, 2, -2, 9, 3, 1, 7, 1]) == {'min': -2, 'max': 9}
assert min_et_max([0, 1, 2, 3]) == {'min': 0, 'max': 3}
assert min_et_max([3]) == {'min': 3, 'max': 3}
assert min_et_max([1, 3, 2, 1, 3]) == {'min': 1, 'max': 3}
assert min_et_max([-1, -1, -1, -1, -1]) == {'min': -1, 'max': -1}
print("Test 32 passé")

print("Test 34...")
moyenne = lambda tab : (lambda f, tab : f(f, [tab[0] + tab[1]] + tab[2:]) if len(tab) > 1 else tab[0])((lambda f, tab : f(f, [tab[0] + tab[1]] + tab[2:]) if len(tab) > 1 else tab[0]), tab) / len(tab)
assert moyenne([5, 3, 8]) == 5.333333333333333
assert moyenne([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 5.5
print("Test 34 passé")

print("Test 35...")
ou_exclusif = lambda tab1, tab2 : [a^b for a, b in zip(tab1, tab2)]
assert ou_exclusif([1, 0, 1, 0, 1, 1, 0, 1], [0, 1, 1, 1, 0, 1, 0, 0]) == [1, 1, 0, 1, 1, 0, 0, 1]
assert ou_exclusif([1, 1, 0, 1], [0, 0, 1, 1]) == [1, 1, 1, 0]
print("Test 35 passé")

print("Test 36...")
couples_consecutifs = lambda tab : [(tab[i], tab[i+1]) for i in range(len(tab)-1) if tab[i] + 1 == tab[i+1]]
assert couples_consecutifs([1, 4, 3, 5]) == []
assert couples_consecutifs([1, 4, 5, 3]) == [(4, 5)]
assert couples_consecutifs([1, 1, 2, 4]) == [(1, 2)]
assert couples_consecutifs([7, 1, 2, 5, 3, 4]) == [(1, 2), (3, 4)]
assert couples_consecutifs ([5, 1, 2, 3, 8, -5, -4, 7]) == [(1, 2), (2, 3), (-5, -4)]
print("Test 36 passé")

print("Test 37...")
recherche = lambda nb, tab : len(tab) - 1 - tab[::-1].index(nb) if nb in tab else -1
assert recherche(1, [2, 3, 4]) == -1
assert recherche(1, [10, 12, 1, 56]) == 2
assert recherche(1, [1, 0, 42, 7]) == 0
assert recherche(1, [1, 50, 1]) == 2
assert recherche(1, [8, 1, 10, 1, 7, 1, 8]) == 5
print("Test 37 passé")

print("Test 38...")
correspond = lambda mot1, mot2 : len(mot1) == len(mot2) and all(mot1[i] == mot2[i] or mot2[i] == '*' for i in range(len(mot1)))
assert correspond('INFORMATIQUE', 'INFO*MA*IQUE') == True
assert correspond('AUTOMATIQUE', 'INFO*MA*IQUE') == False
assert correspond('STOP', 'S*') == False
assert correspond('AUTO', '*UT*') == True
print("Test 38 passé")

print("Test 39...")
fib = lambda f, n : f(f, n-1) + f(f, n-2) if n > 1 else 1
fibonacci = lambda n : fib(fib, n-1)
assert fibonacci(1) == 1
assert fibonacci(2) == 1
assert fibonacci(25) == 75025
print("Test 39 passé")

print("Test 41...")
recherche = lambda lettre, mot : mot.count(lettre)
assert recherche('e', "sciences") == 2
assert recherche('i', "mississippi") == 4
assert recherche('a', "mississippi") == 0
print("Test 41 passé")

print("Test 42...")
selection = lambda tab : sorted(tab)
assert selection([1, 52, 6, -9, 12]) == [-9, 1, 6, 12, 52]
print("Test 42 passé")

print("Test 43...")
ecriture_binaire_entier_positif = lambda n: [int(x) for x in list(bin(n)[2:])]
assert ecriture_binaire_entier_positif(0) == [0]
assert ecriture_binaire_entier_positif(2) == [1, 0]
assert ecriture_binaire_entier_positif(105) == [1, 1, 0, 1, 0, 0, 1]
print("Test 43 passé")

print("Test 44...")
renverse = lambda mot : mot[::-1]
assert renverse("informatique") == "euqitamrofni"
print("Test 44 passé")

print("Test 45...")
rangement_valeurs = lambda tab : [tab.count(i) for i in range(11)]
assert rangement_valeurs([2, 0, 5, 9, 6, 9, 10, 5, 7, 9, 9, 5, 0, 9, 6, 5, 4]) == [2, 0, 1, 0, 1, 4, 2, 1, 0, 5, 1]
print("Test 45 passé")
