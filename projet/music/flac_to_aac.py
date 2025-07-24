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

OUTPUT_DIR = None

def update_cover(path, album_cover):
    audio = MP4(path)

    img = Image.open(album_cover)
    img = img.convert("RGB")
    img = img.resize((1200, 1200), Image.LANCZOS)
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

def get_output_file(input_file):
    return os.path.join(OUTPUT_DIR, os.path.basename(os.path.dirname(input_file)), f"{os.path.splitext(os.path.basename(input_file))[0]}.m4a")

def read_aac_ignore(file_path):
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python truc.py <input_dir> <output_dir>")
        sys.exit(1)

    OUTPUT_DIR = sys.argv[2]

    aac_ignore = read_aac_ignore("aac_ignore.txt")
    todo = []

    for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            if not file.lower().endswith('.flac'):
                continue
            inpt = os.path.join(root, file)
            outpt = get_output_file(inpt)
            if os.path.basename(root) in aac_ignore:
                print(f"SKIP - {outpt} (ignored)")
            elif os.path.exists(outpt):
                print(f"OK   - {outpt}")
            else:
                todo.append((inpt, outpt))

    TOTAL = len(todo)

    for input_file, output_file in todo:
        T_COUNT += 1
        while T_COUNT >= M_COUNT:
            time.sleep(0.1)
        threading.Thread(target=convert_flac_to_m4a, args=(input_file, output_file)).start()

    while T_COUNT > 0:
        time.sleep(0.1)

    os.system("stty sane")
    os._exit(0)
