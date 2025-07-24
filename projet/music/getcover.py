# HD Cover Downloader from Apple Music
# Usage: python getcover.py [first album name] [second album name] [...]
#
# certainly not in the apple music code of conduct -
# Use it at your own risk

import urllib.parse
import requests
import sys
import os

directories = sys.argv[1:]

if not directories:
    print("NOTE:    path used as album name, write album name as argument for fine searching")
    print("Usage:   python getcover.py [first album name] [second album name] [...]")
    print("->       python getcover.py 'Lana Del Rey - Blue Banisters'\n")

    directories = [os.path.basename(os.getcwd())]

for d in directories:
    url = "https://music.apple.com/fr/search?term=" + urllib.parse.quote(d)

    response = requests.get(url)

    try:
        r = "/".join(response.text.split("https://is1-ssl.mzstatic.com/image/thumb/")[1].split("/")[:-1])
        fmt = r.split(".")[-1]
        r = f"https://is1-ssl.mzstatic.com/image/thumb/{r}/3000x3000.{fmt}"
    except:
        print(f"{d} [Not found]")
        continue

    try:
        response = requests.get(r)

        print(f"{d} [{len(response.content) / 1024 / 1024:.2f} MB in {fmt.upper()}]")

        with open(f"{d}.{fmt}", "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(f"{d} [Error: {e}]")
        continue
