# HOSTING-STATUT

## Démarrage rapide
### Installation
Téléchargez le repository, et déplacez *status.py* dans le dossier de votre programme.
### Importation
```py
from status import Status
```

## Interaction
### Création d'un objet
```py
etat = Status("http://pf4.ddns.net/api/etat_bots.json")
```

### url
*url* stock l'url utilisé pour la creation de l'objet

```py
etat.url
```
### brut
*brut* est le dictionaire brut qui stock les données
```py
etat.brut
```

### get_status()
*get_status("xxxx#0000")* retourne le status du bot *xxxx#0000*
```py
get_status("fire dragon#8794")
```

### get_role()
*get_role("xxxx#0000")* retourne le role du bot *xxxx#0000*
```py
get_role("fire dragon#8794")
```

### list_bots()
*list_bots()* retourne la liste de tout les bots
```py
for l in list_bots()
    print(f"{l} -> {get_status("fire dragon#8794")}")
```

### refresh()
*refresh()* met à jour les données
```py
etat.refresh()
```

*Bonne chance et amusé vous bien!*

Mon serveur discord: [ici](https://discord.gg/PFbymQ3d97)
