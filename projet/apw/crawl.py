from _thread import start_new_thread

import requests
import random
import json
import time
import re
import os

IMG_DIR = "img"

g_stats = {
    "issues": 0,
    "cache": 0,
    "dl": 0,
    "imgerr": 0,
    "retries": 0
}

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

def url_get_retry(url):
    for i in range(5):
        try:
            response = requests.get(url)
            if response.status_code < 500:
                break
        except requests.exceptions.RequestException as e:
            pass
        g_stats["retries"] += 1
        time.sleep(random.uniform(0.5, 1.5))
    return response

def get_image_from_ravelry(url):
    response = url_get_retry(url)
    if response.status_code != 200:
        print("Error", response.status_code, "for", url)
        g_stats["imgerr"] += 1
        return None

    html = response.text.split("\n")

    line = None

    for i in range(len(html)):
        if html[i] == '<div class="photo_gallery__section photo_gallery__section--1 section">':
            line = html[i+1]

    if line is None:
        print("No image found in", url)
        g_stats["imgerr"] += 1
        return None
        

    start = line.rfind("https://")
    end = line.find('"', start)

    if start == -1 or end == -1:
        print("No image found in", url)
        g_stats["imgerr"] += 1
        return None

    return line[start:end].split(" ")[0]

def download_image(source_url, author, name):
    if not source_url:
        return None

    img_path = process_img_name(author) + "_" + process_img_name(name) + "."

    # list all files in the directory
    files = os.listdir(IMG_DIR)

    # check if the image is already downloaded (extension can be everything)
    for file in files:
        if file.startswith(img_path):
            g_stats["cache"] += 1
            return os.path.join(IMG_DIR, file)

    if not source_url.startswith("https://www.ravelry.com/patterns/library"):
        url = source_url
    else:
        url = get_image_from_ravelry(source_url)

    if url == None:
        return None

    ext = url.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png", "webp"]:
        print("strange extension in", url)
        ext = "jpg"

    filename = os.path.join(IMG_DIR, img_path + ext)

    response = url_get_retry(url)
    if response.status_code != 200:
        print("Error", response.status_code, "for", url)
        g_stats["imgerr"] += 1
        return None

    with open(filename, 'wb') as f:
        f.write(response.content)

    g_stats["dl"] += 1
    return filename

###################################################
#                                                 #
#            Data processing functions            #
#                                                 #
###################################################

def natsort(seq):
    def natural_key(string_):
        return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]
    return sorted(seq, key=natural_key)

def get_needles(needles):
    if needles == None:
        return -1
    needles = needles.replace(",", ".")
    try:
        return float(needles)
    except ValueError:
        return -1

def parse_str_list(str):
    if str == None:
        return None
    str = str.split(",")
    for j in range(len(str)):
        tmp = []
        str[j] = str[j].strip()
        is_start = True
        for i in range(len(str[j])):
            if is_start:
                tmp.append(str[j][i].upper())
                is_start = False
            elif str[j][i] == " ":
                tmp.append("_")
                is_start = True
            else:
                tmp.append(str[j][i].lower())
        str[j] = "".join(tmp)
    return str

def process_img_name(str):
    output = []
    for c in str:
        c = c.lower()
        if c in "abcdefghijklmnopqrstuvwxyz":
            output.append(c)
        elif c in "0123456789":
            output.append(c)
        elif c == " ":
            output.append("_")
        else:
            output.append(hex(ord(c))[2:])
    return "".join(output)

def sort_wools(wools):
    one_word = []
    multi_word = []
    for w in wools:
        if "_" in w:
            multi_word.append(w)
        else:
            one_word.append(w)
    one_word = sorted(one_word)
    multi_word = sorted(multi_word)
    return one_word + multi_word

###################################################
#                                                 #
#              Main parsing function              #
#                                                 #
###################################################

def line_to_dico(line, index):
    printable_line = lambda idx, x: f"l{idx}: '" + " ".join([str(i) for i in x if i != None]) + "'"
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
        print("No name found for", printable_line(index, line))
        g_stats["issues"] += 1
        return None

    dico["needles"] = get_needles(line[11])
    dico["wool"] = parse_str_list(line[12])
    dico["collec"] = parse_str_list(line[13])
    dico["url"] = line[14]

    dico["image"] = line[15]
    if dico["image"]:
        dico["image"] = download_image(dico["image"], dico["author"], dico["name"])
    elif dico["url"]:
        if dico["url"].startswith("https://www.ravelry.com/patterns/library"):
            dico["image"] = download_image(dico["url"], dico["author"], dico["name"])
        else:
            print("other website without image for", printable_line(index, line))

    if dico["needles"] == -1:
        print("No needles found for", printable_line(index, line))
        g_stats["issues"] += 1
        return None

    return dico

global ended_threads
ended_threads = 0

def thread_line_to_dico(line, index):
    global ended_threads

    dico = line_to_dico(line, index)
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

if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

for i, line in enumerate(lines):
    while True:
        try:
            start_new_thread(thread_line_to_dico, (line, i + 3))
            break
        except Exception as e:
            print("Error:", e)
            time.sleep(1)

while ended_threads < len(lines):
    pass

# sort by author and name

truc = sorted(truc, key=lambda x: (x["author"], x["name"]))

print(".-=== End of processing ===")
print("|")
print("| Day:        ", time.strftime("%d/%m/%Y"))
print("| Time:       ", time.strftime("%H:%M:%S"))
print("|")
print("| cached:     ", g_stats["cache"])
print("| Downloaded: ", g_stats["dl"])
print("| Retries:    ", g_stats["retries"])
print("|")
print("| Issues:     ", g_stats["issues"])
print("| Web errors: ", g_stats["imgerr"])
print("|")
print("| Total:      ", len(truc))
print("|")
print("'-=========================")

types = {
    "needles": [],
    "wools": [],
    "collec": []

}

for e in truc:
    if e["wool"]:
        for w in e["wool"]:
            if w not in types["wools"]:
                types["wools"].append(w)
    if e["collec"]:
        for c in e["collec"]:
            if c not in types["collec"]:
                types["collec"].append(c)
    if e["needles"] not in types["needles"]:
        types["needles"].append(e["needles"])

types["needles"] = sorted(types["needles"])
types["wools"] = sort_wools(types["wools"])
types["collec"] = natsort(types["collec"])

with open("data.json", "w") as f:
    json.dump(truc, f, indent=4)

with open("types.json", "w") as f:
    json.dump(types, f, indent=4)
