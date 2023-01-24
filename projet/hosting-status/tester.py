from status import Status

etat = Status("http://pf4.ddns.net/api/etat_bots.json")

print(etat.get_status("fire dragon#8794"))