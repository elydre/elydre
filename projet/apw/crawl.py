import requests
import json
import os

DOWNLOAD_IMAGES = True

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

def download_image(url, source_url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Error", response.status_code)
        exit()

    filename = os.path.join("img", source_url.split("/")[-1] + "." + url.split(".")[-1])

    with open(filename, 'wb') as f:
        f.write(response.content)

    return filename

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

lines = read_csv("src.csv")
lines = lines[2:]

truc = []

for line in lines:
    dico = {}

    if line[0] == None:
        continue

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

    if dico["url"] and DOWNLOAD_IMAGES:
        print("Downloading image for", dico["name"])
        dico["image"] = download_image(get_image_url(dico["url"]), dico["url"])
    else:
        dico["image"] = None

    if dico["needles"] == -1:
        print("No needles found for", line)
        exit()

    truc.append(dico)

print(len(truc))

with open("data.json", "w") as f:
    json.dump(truc, f, indent=4)
