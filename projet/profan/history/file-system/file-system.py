__DOCUMENTATION__ = """
0x8000 ==> secteur écrit
0x4000 ==> dossier ici
0x2000 ==> index de fichier ici
0x1000 ==> fichier ici
path = "/dir/.../" + "name"
"""

# NE PAS PORTER

import os
import shutil

NUMBER_OF_MO = 1
DISK_SIZE = 2048*NUMBER_OF_MO
disque = [[0]*128]*DISK_SIZE

def p_write_sectors_ATA_PIO(secteur, data):
    if secteur < 0:
        p_print_and_exit(f"CONAR TU ECRIT PAS SUR LE SECTEUR {secteur}")
    if len(data) != 128 :
        p_print_and_exit("Erreur: la taille de la donnée doit être de 128 octets")
    disque[secteur] = data
def p_read_sectors_ATA_PIO(secteur):
    return disque[secteur]

def p_print_and_exit(msg):
    print(msg)
    raise Exception()

def p_print_and_debug(debut, fin):
    for i in range(debut, fin+1):
        sect = p_read_sectors_ATA_PIO(i)
        debug_status = hex(sect[0])
        if debug_status == "0x8000": debug_status = "Unknown Type "
        if debug_status == "0x9000": debug_status = "File content "
        if debug_status == "0xa000": debug_status = "File header  "
        if debug_status == "0xc000": debug_status = "Folder       "
        print(f"secteur {i} - {debug_status}: {sect}")

def p_file_to_disk():
    global disque
    print("Dump de HDD.bin dans disque, merci d'attendre")
    with open("HDD.bin", "rb") as file:
        cnt = file.read()
    liste = [cnt[i] + cnt[i + 1] * 256 for i in range(0, len(cnt), 2)]
    new_list = [liste[i] for i in range(0, len(liste), 2)]
    disque = [new_list[i:i + 128] for i in range(0, len(new_list), 128)]
    print("Dump fini !")
    
def p_disk_to_file() :  # sourcery skip: use-itertools-product
    print("Dump de disque dans HDD.bin, merci d'attendre")
    global disque
    with open("HDD.bin", "wb") as file:
        for i in range(DISK_SIZE):
            for j in range(128):
                hex_string = "0"*(4-len(hex(disque[i][j])[2:]))+hex(disque[i][j])[2:]
                hex_string = hex_string[2]+hex_string[3]+hex_string[0]+hex_string[1]
                file.write(bytes.fromhex(hex_string))
                file.write(bytes.fromhex("0000"))
    print("Dump fini !")

def p_folder_to_disk(local_place="/"):
    # TODO : fix pouvoir transferer des fichiers de edit_folder directement (ça marche que en récursif)
    if len(local_place) > 1 and local_place[0] == local_place[1] == "/":
        local_place = local_place[1:]
    path_folder=os.getcwd()+"\\edit_folder"+local_place.replace("/", "\\")
    for file_folder in os.listdir(path_folder):
        if os.path.isfile(f"{path_folder}/{file_folder}"):
            print(f"writing file {file_folder} in {local_place}")
            make_file(local_place, file_folder)
            with open(path_folder+"\\"+file_folder, "rb") as f:
                bit_stream = f.read()
                # mettre un byte par uint32 pour éviter les soucis, ++ faire un décalage de 1
                bit_stream = [x+1 for x in list(bit_stream)] + [0]*(3-len(bit_stream)%3)
                chunks = [list(bit_stream[3 * i : 3 * (i + 1)]) for i in range(int(len(bit_stream) / 3 + 1))]

                chunks = chunks[:-1]
                if chunks[-1] == [0, 0, 0]:
                    chunks = chunks[:-1]
            string_final = []
            for chunk in chunks:
                string_final.extend([chunk[0], chunk[1], chunk[2]])
            if string_final != b"":
                write_in_file(f"{local_place}/{file_folder}", string_final, len(string_final))
        else:
            print(f"writing folder {file_folder} in {local_place}")
            make_dir(local_place, file_folder)
            p_folder_to_disk((f"/{local_place}" if local_place != "/" else "") + "/" + file_folder)

def disk_to_folder(id = 0, local_path = "/"):
    path_folder=os.getcwd()+"\\output_folder"
    if id == 0 and local_path == "/" : # on reset tout
        try: shutil.rmtree(path_folder)
        except FileNotFoundError: pass
    try: os.mkdir(path_folder)
    except FileExistsError: pass
    folder = p_read_sectors_ATA_PIO(id)[21:127]
    for truc in folder:
        if truc != 0:
            if p_read_sectors_ATA_PIO(truc)[0] & 0x4000:
                print("dossier", truc)
                name = "".join([chr(x) for x in p_read_sectors_ATA_PIO(truc)[1:21] if x != 0])
                try: os.mkdir(path_folder+local_path+name)
                except FileExistsError: pass
                disk_to_folder(truc,local_path+name+"/")
            if p_read_sectors_ATA_PIO(truc)[0] & 0x2000:
                print("fichier", truc)
                with open((f"{path_folder}/" + (local_path if local_path != "/" else "") + "".join([chr(x) for x in p_read_sectors_ATA_PIO(truc)[1:21] if x != 0])).replace("/", "\\"), "wb") as f:
                    to_write = []
                    current_index = p_read_sectors_ATA_PIO(truc)[127]
                    while current_index:
                        to_write += p_read_sectors_ATA_PIO(current_index)[1:127]
                        current_index = p_read_sectors_ATA_PIO(current_index)[127]
                    to_write = [x-1 for x in to_write if x != 0]
                    to_write = bytes(to_write)
                    f.write(to_write)

# INTERN FUNCTIONS

def i_next_free(rec = 0):
    x = 0
    for i in range(rec + 1):
        while p_read_sectors_ATA_PIO(x)[0] & 0x8000:
            x += 1
        if i != rec:
            x += 1
    return x

def i_creer_dossier(nom):  # sourcery skip: convert-to-enumerate
    folder_id = i_next_free()
    list_to_write = [0] * 128
    list_to_write[0] = 0xC000 # 0x8000 + 0x4000 (secteur occupé + dossier ici)

    if len(nom) > 20:
        p_print_and_exit("Erreur: le nom du dossier est trop long")
        
    # TODO : Vérifier qu'un dossier avec le même nom n'existe pas déja au même endroit

    list_index = 1
    for i in range(len(nom)):
        list_to_write[list_index] = ord(nom[i])
        list_index += 1

    p_write_sectors_ATA_PIO(folder_id, list_to_write)
    
    return folder_id # on renvoie l'id du dossier
    
def i_creer_index_de_fichier(nom):  # sourcery skip: convert-to-enumerate
    if len(nom) > 20:
        p_print_and_exit("Erreur: le nom du dossier est trop long")
    
    location = i_next_free()
    location_file = i_next_free(1)
    
    # TODO : Vérifier qu'un fichier avec le même nom n'existe pas déja au même endroit
    
    # write index
    index_to_write = [0] * 128
    index_to_write[0] = 0xA000 # 0x8000 + 0x2000 (secteur occupé + index de fichier ici)
    list_index = 1
    for i in range(len(nom)):
        index_to_write[list_index] = ord(nom[i])
        list_index += 1
    index_to_write[127] = location_file
    # print(index_to_write)
    p_write_sectors_ATA_PIO(location, index_to_write)
    
    #write file
    file_to_write = [0] * 128
    file_to_write[0] = 0x9000 # 0x8000 + 0x1000 (secteur occupé + fichier ici)
    file_to_write[127] = 0 # suite du fichier si besoin (0 = y a pas)
    p_write_sectors_ATA_PIO(location_file, file_to_write)
    
    return location # on return l'id du secteur du fichier

def i_set_data_to_file(data, data_size, file_index):
    # free
    file_index = p_read_sectors_ATA_PIO(file_index)[127]
    if not p_read_sectors_ATA_PIO(file_index)[0] & 0xa000:
        p_print_and_exit("Le secteur n'est pas un fichier !")
    suite = file_index
    while suite:
        # print(f"free {suite}")
        suite = i_free_file_and_get_next(suite)
    
    # write
    for i in range(data_size // 126 + 1):
        # print(f"{i}, write in {file_index}")
        part = [0] * 128
        ui = 1
        part[0] = 0x9000 # (secteur occupé + fichier ici)
        for j in range(126):
            if i*126 + j >= data_size:
                ui = 0
                break
            part[j + 1] = data[i * 126 + j]
        if ui:
            part[127] = i_next_free(1)
        p_write_sectors_ATA_PIO(file_index, part)
        file_index = part[127]
    
def i_free_file_and_get_next(file_part):
    file = p_read_sectors_ATA_PIO(file_part)
    suite = file[127]
    for i in range(128):
        file[i] = 0
    return suite

def i_add_item_to_dir(file_id, folder_id):
    dossier = p_read_sectors_ATA_PIO(folder_id)
    for i in range(21, 128):
        if dossier[i] == 0:
            dossier[i] = file_id
            break
    else:
        # TODO : si le dossier n'a plus de secteurs, en ajouter un
        # i_add_item_to_dir(file_id, dossier[127])
        p_print_and_exit("i_add_item_to_dir plus de place, TODO")

def i_get_dir_content(id):
    folder = p_read_sectors_ATA_PIO(id)
    if not folder[0] & 0x8000:
        p_print_and_exit("Erreur, le secteur est vide")
    if not folder[0] & 0x4000:
        p_print_and_exit("Erreur, le secteur n'est pas un dossier")
    liste_contenu = []
    # directement dans le premier secteur
    for i in range(21, 128): # 21 = juste après le nom du dossier
        pointeur = folder[i]
        if pointeur != 0:
            liste_contenu.append(pointeur)
    # TODO : ajouter la lecture dans les secteurs suivants
    liste_noms = []
    liste_id = []
    for item in liste_contenu:
        content = p_read_sectors_ATA_PIO(item)
        content = content[1:21]
        content = "".join([chr(x) for x in content]).replace("\x00", "")
        liste_noms.append(content)
        liste_id.append(item)
    return (liste_noms, liste_id)
    

def i_path_to_id(path): # path = ["/", "dossier1", "dossier2", "fichier"]
    # sourcery skip: assign-if-exp, de-morgan, reintroduce-else
    if path == "/":
        return 0
    path = i_parse_path(path)
    if path[0] == "/":
        path[0] = 0
    (liste_noms, liste_id) = i_get_dir_content(path[0])
    path = path[1:]
    if len(path) == 1:
        x = 0
        for element in liste_noms:
            if element == path[0]:
                break
            x += 1
        return liste_id[x]
    while len(path) != 1:
        x = 0
        for element in liste_noms:
            if element == path[0]:
                break
            x += 1
        contenu_path_0 = liste_id[x]
        (liste_noms, liste_id) = i_get_dir_content(contenu_path_0)
        path = path[1:]
    if not path[0] in liste_noms:
        return -1
    x = 0
    for element in liste_noms:
        if element == path[0]:
            break
        x += 1
    contenu_path_0 = liste_id[x]
    return contenu_path_0

def i_parse_path(path:str) -> list:
    path = path.split("/")
    path[0] = "/"
    return path

# FUNCTIONS TO USE

def get_used_sectors(disk_size):
    total = 0
    for i in range(disk_size):
        file = p_read_sectors_ATA_PIO(i)
        if file[0] & 0x8000:
            total += 1
    return total

def is_disk_full(size):
    return size == get_used_sectors(size)

def make_dir(path, folder_name):
    dossier = i_creer_dossier(folder_name)
    id_to_set = i_path_to_id(path)
    i_add_item_to_dir(dossier, id_to_set)
    return dossier

def make_file(path, file_name):
    fichier_test = i_creer_index_de_fichier(file_name)
    id_to_set = i_path_to_id(path)
    i_add_item_to_dir(fichier_test, id_to_set)
    return fichier_test

def write_in_file(path, data, data_size):
    id_to_set = i_path_to_id(path)
    i_set_data_to_file(data, data_size, id_to_set)

def get_file_size(path):
    id_file_index = i_path_to_id(path)
    if not p_read_sectors_ATA_PIO(id_file_index)[0] & 0xa000:
        p_print_and_exit("Le secteur n'est pas un fichier")
    sector_size = 0
    while p_read_sectors_ATA_PIO(id_file_index)[127]:
        sector_size += 1
        id_file_index = p_read_sectors_ATA_PIO(id_file_index)[127]
    return sector_size

def read_file(path):  # sourcery skip: use-named-expression
    id_file_index = p_read_sectors_ATA_PIO(i_path_to_id(path))[127]
    if not p_read_sectors_ATA_PIO(id_file_index)[0] & 0xa000:
        p_print_and_exit("Le secteur n'est pas un fichier")
    data = []
    data += p_read_sectors_ATA_PIO(id_file_index)[1:127]
    id_file_index = p_read_sectors_ATA_PIO(id_file_index)[127]
    while id_file_index:
        data += p_read_sectors_ATA_PIO(id_file_index)[1:127]
        id_file_index = p_read_sectors_ATA_PIO(id_file_index)[127]
    # TODO : virer les 0 a la fin de la lecture d'un fichier en prenant en compte sa taille
    return data

def delete_file(path):
    header_id = path if str(path)[0] != "/" else i_path_to_id(path)
    # supprimer le fichier
    file_index = p_read_sectors_ATA_PIO(header_id)[127]
    if not p_read_sectors_ATA_PIO(file_index)[0] & 0xa000:
        p_print_and_exit("Le secteur n'est pas un fichier !")
    suite = file_index
    while suite:
        suite = i_free_file_and_get_next(suite)
    p_write_sectors_ATA_PIO(header_id, [0] * 128)
    if str(path)[0] == "/": 
        # supprimer la reference dans le dossier uniquement si on delete pas dans un dossier
        path = i_parse_path(path)
        path = path[:-1][1:]
        path = "/" + "/".join(path)
        id_to_set = i_path_to_id(path)
        dossier = p_read_sectors_ATA_PIO(id_to_set)
        for i in range(21, 128):
            if dossier[i] == header_id:
                dossier[i] = 0
                break
        else:
            p_print_and_exit("Le fichier n'est pas dans le dossier !")
        p_write_sectors_ATA_PIO(id_to_set, dossier)

def does_path_exists(path):
    # without a try except
    return i_path_to_id(path) != -1

def type_sector(path):
    if str(path)[0] != "/":
        id_sector = path
    else:
        id_sector = i_path_to_id(path)
    match p_read_sectors_ATA_PIO(id_sector)[0]:
        # PORTAGE WARN : ATTENTION AUX TYPES
        case 0x8000:
            return -1 # pas sencé arriver, le secteur ne doit pas être écrit mais vide (aucun PUTAIN de sens)
        case 0x9000:
            print("WARNING 0 : SHOULD NOT BE REACHABLE")
            return 1 # fichier (pas sencé arriver, le path ne pointe pas a ça mais a l'index normalement, au cas ou je laisse...)
        case 0xa000:
            return 2 # index de fichier
        case 0xc000:
            return 3 # dossier
        case _:
            return 0 # si jamais le secteur est vide

def delete_dir(path):
    id_folder = path if str(path)[0] != "/" else i_path_to_id(path)
    if id_folder == 0:
        p_print_and_exit("On ne peut pas supprimer la racine !")
    liste_en_cours = []
    (_, liste_ids) = i_get_dir_content(id_folder)
    for contenu in liste_ids:
        if contenu in liste_en_cours:
            continue
        liste_en_cours.append(contenu)
        type_secteur = type_sector(contenu)
        if type_secteur in [0, -1]:
            p_print_and_exit("problème sur le contenu du dossier")
        if type_secteur == 2: # fichier
            delete_file(contenu)
            # supprimer fichier
        if type_secteur == 3: # dossier
            delete_dir(contenu)
            # supprimer dossier
    p_write_sectors_ATA_PIO(id_folder, [0] * 128)
    # delete la référence connue dans le path
    if str(path)[0] == "/":
        id_main_folder = i_path_to_id("".join(i_parse_path(path)[:-1]))
        main_folder = p_read_sectors_ATA_PIO(id_main_folder)
        for i in range(21, 128):
            if main_folder[i] == id_folder:
                main_folder[i] = 0
                break

# MAIN PROGRAM

# si le premier dossier n'existe pas, il est créé (cette partie est a porter)
if not p_read_sectors_ATA_PIO(0)[127] & 0x8000:
    print("pas de dossier racine, création en cours...")
    location = i_next_free()
    if location != 0:
        p_print_and_exit("Erreur: le disque n'est pas vide")
    i_creer_dossier("/")
    print("Dossier racine créé")

# code de test

p_folder_to_disk()
p_disk_to_file()

# p_file_to_disk()
# disk_to_folder()
