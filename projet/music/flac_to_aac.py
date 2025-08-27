from mutagen.mp4 import MP4, MP4Cover
from PIL import Image
import subprocess
import threading
import time
import sys
import os
import io


T_COUNT = 0
M_COUNT = 28

COMPLETED = 0
TOTAL = 0

def update_cover(path, album_cover):
    audio = MP4(path)

    img = Image.open(album_cover)
    img = img.convert("RGB")
    img = img.resize((1000, 1000), Image.LANCZOS)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_data = img_byte_arr.getvalue()

    # Ajoute la nouvelle couverture
    cover = MP4Cover(img_data, imageformat=MP4Cover.FORMAT_PNG)
    audio["covr"] = [cover]

    audio.save()


def convert_flac_to_m4a(input_file, output_file):
    for name in ["cover.jpg", "cover.png"]:
        path = os.path.join(os.path.dirname(input_file), name)
        if os.path.exists(path):
            break
    else:
        print(f"No cover file found for {input_file}!")
        os._exit(1)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    if (subprocess.run([
        "ffmpeg",
        "-loglevel", "error",
        "-y",
        "-i", input_file,
        "-map", "a",
        "-acodec", "aac",
        "-b:a", "256k",
        "-ar", "44100",
        output_file
    ])).returncode != 0:
        print(f"Error converting {input_file} to M4A!")
        os._exit(1)

    update_cover(output_file, path)


    global T_COUNT, COMPLETED
    T_COUNT -= 1
    COMPLETED += 1

    print(f"{COMPLETED/TOTAL * 100:.2f}% - {output_file}")

def read_aac_ignore(file_path):
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_allout(output_root):
    if not os.path.isdir(output_root):
        return []

    return [album for album in os.listdir(output_root) if os.path.isdir(os.path.join(output_root, album))]

def should_ignore(album, aac_ignore):
    if album in aac_ignore:
        return True
    for pattern in aac_ignore:
        if pattern.endswith('*') and album.startswith(pattern[:-1]):
            return True
    return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python flac_to_aac.py <input_dir> <output_root>")
        sys.exit(1)

    output_root = sys.argv[2]
    root = sys.argv[1]

    aac_ignore = read_aac_ignore("aac_ignore.txt")

    allout = get_allout(output_root)
    allin = []
    todo = []


    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory.")
        sys.exit(1)

    for album in os.listdir(root):
        if not os.path.isdir(os.path.join(root, album)):
            continue

        allin.append(album)

        if should_ignore(album, aac_ignore):
            print(f"IGN - {album}")
            continue

        for file in os.listdir(os.path.join(root, album)):
            filepath = os.path.join(root, album, file)

            if not (os.path.isfile(filepath) and filepath.lower().endswith(".flac")):
                continue
    
            outpt = os.path.join(output_root, album, f"{os.path.splitext(file)[0]}.m4a")

            if os.path.exists(outpt):
                print(f"OK  - {outpt}")
            else:
                todo.append((filepath, outpt))

    TOTAL = len(todo)

    for input_file, output_file in todo:
        T_COUNT += 1
        while T_COUNT >= M_COUNT:
            time.sleep(0.1)
        threading.Thread(target=convert_flac_to_m4a, args=(input_file, output_file)).start()

    while T_COUNT > 0:
        time.sleep(0.1)
        
    os.system("stty sane")

    print("All conversions completed.")

    for album in allout:
        if (album not in allin) or should_ignore(album, aac_ignore):
            dirpath = os.path.join(output_root, album)
            print(f"'{album}' found in output but not in input")
            if input("Delete it? (y/n) ").strip().lower() == 'y':
                print(f"Deleting {dirpath}")
                os.system(f"rm -rf '{dirpath}'")

    os._exit(0)
