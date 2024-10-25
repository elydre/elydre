import datetime

def to_french_date(string):
    traduction = {
        'Monday':    '   Lundi',
        'Tuesday':   '   Mardi',
        'Wednesday': 'Mercredi',
        'Thursday':  '   Jeudi',
        'Friday':    'Vendredi',
        'Saturday':  '  Samedi',
        'Sunday':    'Dimanche'
    }
    for key, value in traduction.items():
        string = string.replace(key, value)
    return string

def liste_days(date_debut, date_fin):
    date_debut = datetime.datetime.strptime(date_debut, '%Y-%m-%d')
    date_fin = datetime.datetime.strptime(date_fin, '%Y-%m-%d')
    liste = []
    while date_debut <= date_fin:
        # day name, day number/month number
        liste.append(to_french_date(date_debut.strftime('%A %d/%m')))
        date_debut += datetime.timedelta(days=1)
    return liste

# decopper omogeneiquement la liste pour repartir les espaces entre les elements
def decoupe_liste(liste, count):
    if count == 0:
        return []
    if count > len(liste):
        return liste
    
    new_list = [liste.pop(0)]
    liste_len = len(liste)
    count -= 1

    if count == 0 or liste_len == 0:
        return new_list

    div = liste_len / count

    somme = div
    for i in range(liste_len):
        if i + 1.5 >= somme:
            somme += div
            new_list.append(liste[i])

    return new_list


liste = liste_days('2024-10-11', '2024-12-25')

for i, e in enumerate(decoupe_liste(liste, 24), 2):
    print(f"{'0' if i < 10 else ''}{i}  {e}")
