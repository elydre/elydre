from _thread import start_new_thread
import requests
import json
import os

DOWNLOAD_IMAGES = True
IMG_DIR = "img"

###################################################
#                                                 #
#           CSV file reading functions            #
#                                                 #
###################################################

def read_csv(file):
    def humanize(word):
        if word == "":
            return None
        while "  " in word:
            word = word.replace("  ", " ")
        return word.strip()

    def parce_csv_line(line):
        r = []
        word = ""
        in_quote = False
        for c in line:
            if c == '"':
                in_quote = not in_quote
            elif c == ',' and not in_quote:
                r.append(humanize(word))
                word = ""
            else:
                word += c
        r.append(humanize(word))
        return r

    with open(file, 'r') as f:
        lines = f.read().splitlines()
    return [parce_csv_line(line) for line in lines]

###################################################
#                                                 #
#      Image research and download functions      #
#                                                 #
###################################################

def get_image_url(url):
    if url == "":
        return None
    response = requests.get(url)
    if response.status_code != 200:
        print("Error", response.status_code)
        exit()

    html = response.text.split("\n")

    line = None

    for i in range(len(html)):
        if html[i] == '<div class="photo_gallery__section photo_gallery__section--1 section">':
            line = html[i+1]

    if line is None:
        print("No image found")
        exit()

    start = line.rfind("https://")
    end = line.find('"', start)

    if start == -1 or end == -1:
        print("No image found")
        exit()

    return line[start:end].split(" ")[0]

def download_image(source_url):
    url = get_image_url(source_url)

    if url == None:
        print("No image found")
        exit()

    ext = url.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png"]:
        print("strange extension in", url)
        ext = "jpg"

    filename = os.path.join(IMG_DIR, source_url.split("/")[-1] + "." + ext)

    if os.path.exists(filename):
        return filename

    response = requests.get(url)
    if response.status_code != 200:
        print("Error", response.status_code)
        exit()

    with open(filename, 'wb') as f:
        f.write(response.content)

    return filename

###################################################
#                                                 #
#            Data processing functions            #
#                                                 #
###################################################

def get_needles(needles):
    if needles == None:
        return -1
    needles = needles.replace(",", ".")
    try:
        return float(needles)
    except ValueError:
        return -1

def parse_wool(wools):
    if wools == None:
        return None
    wools = wools.split(",")
    for j in range(len(wools)):
        tmp = []
        wools[j] = wools[j].strip()
        for i in range(len(wools[j])):
            if i == 0:
                tmp.append(wools[j][i].upper())
            elif wools[j][i] == " ":
                tmp.append("_")
            else:
                tmp.append(wools[j][i].lower())
        wools[j] = "".join(tmp)
    return wools

###################################################
#                                                 #
#              Main parsing function              #
#                                                 #
###################################################

def line_to_dico(line):
    dico = {}

    if line[0] == None:
        return None

    dico["author"] = line[0]

    for i in range(1, 11):
        if line[i] != None:
            dico["name"] = line[i]
            dico["type"] = i
            break
    else:
        print("No name found for", line)
        exit()

    dico["needles"] = get_needles(line[11])
    dico["wool"] = parse_wool(line[12])
    dico["url"] = line[14]

    dico["image"] = None
    if dico["url"] and DOWNLOAD_IMAGES:
        if dico["url"].startswith("https://www.ravelry.com/patterns/library"):
            dico["image"] = download_image(dico["url"])
        else:
            print("other website", dico["url"])

    if dico["needles"] == -1:
        print("No needles found for", line)

    return dico

global ended_threads
ended_threads = 0

def thread_line_to_dico(line):
    global ended_threads

    dico = line_to_dico(line)
    if dico:
        truc.append(dico)

    ended_threads += 1

###################################################
#                                                 #
#                  Main program                   #
#                                                 #
###################################################

lines = read_csv("src.csv")
lines = lines[2:]

truc = []

if DOWNLOAD_IMAGES and not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

for line in lines:
    start_new_thread(thread_line_to_dico, (line,))

while ended_threads < len(lines):
    pass

# sort by author and name

truc = sorted(truc, key=lambda x: (x["author"], x["name"]))

print(len(truc))

with open("data.json", "w") as f:
    json.dump(truc, f, indent=4)