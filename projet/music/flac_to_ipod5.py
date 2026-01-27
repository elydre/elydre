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
    img = img.resize((500, 500), Image.LANCZOS)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG", quality=90)
    img_data = img_byte_arr.getvalue()

    # Ajoute la nouvelle couverture
    cover = MP4Cover(img_data, imageformat=MP4Cover.FORMAT_PNG)
    audio["covr"] = [cover]

    audio.save()


def convert_flac_to_alac(input_file, output_file):
    """
    input_file: path to input FLAC file
    -> 16 / 24bit lossless 44.1 / 48kHz or more

    output_file: path to output M4A file
    -> 16bit lossless 44.1 / 48kHz ONLY
    """

    for name in ["cover.jpg", "cover.png"]:
        path = os.path.join(os.path.dirname(input_file), name)
        if os.path.exists(path):
            break
    else:
        print(f"No cover file found for {input_file}!")
        os._exit(1)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # read input kbps and sample rate
    info = subprocess.run([
        "ffprobe",
        "-v", "error",
        "-show_entries", "stream=sample_rate",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_file
    ], capture_output=True, text=True)

    try:
        input_srate = int(info.stdout.strip())
    except ValueError:
        print(f"Error reading sample rate of {input_file}!")
        os._exit(1)

    if input_srate % 44100 == 0:
        output_srate = 44100
    elif input_srate % 48000 == 0:
        output_srate = 48000
    else:
        print(f"Unsupported sample rate {input_srate} Hz in {input_file}!")
        os._exit(1)

    print(f"IN: {input_srate} Hz -> OUT: {output_srate} Hz")

    if (subprocess.run([
        "ffmpeg",
        "-loglevel", "error",
        "-y",
        "-i", input_file,
        "-vn",
        "-map_metadata", "0",
        "-af", f"aresample={output_srate}:resampler=soxr:precision=28,aformat=sample_fmts=s16",
        "-c:a", "alac",
        output_file
    ]).returncode != 0):
        print(f"Error converting {input_file} to ALAC!")
        os._exit(1)

    update_cover(output_file, path)

    global T_COUNT, COMPLETED
    T_COUNT -= 1
    COMPLETED += 1

    print(f"{COMPLETED/TOTAL * 100:.2f}% - {output_file.split('/')[-1]}")

def read_album_list(file_path):
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_allout(output_root):
    if not os.path.isdir(output_root):
        return []

    return [album for album in os.listdir(output_root) if os.path.isdir(os.path.join(output_root, album))]

def should_ignore(album, album_list):
    if album in album_list:
        return False

    for pattern in album_list:
        if pattern.endswith('*') and album.startswith(pattern[:-1]):
            return False

    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python flac_to_ipod5.py <input_dir> <output_root>")
        sys.exit(1)

    output_root = sys.argv[2]
    root = sys.argv[1]

    album_list = read_album_list("ipod5_list.txt")

    allout = get_allout(output_root)
    todo = []


    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory.")
        sys.exit(1)

    for album in os.listdir(root):
        if not os.path.isdir(os.path.join(root, album)):
            continue

        if should_ignore(album, album_list):
            continue

        for file in os.listdir(os.path.join(root, album)):
            filepath = os.path.join(root, album, file)

            if not (os.path.isfile(filepath) and filepath.lower().endswith(".flac")):
                continue

            outpt = os.path.join(output_root, album, f"{os.path.splitext(file)[0]}.m4a")

            if os.path.exists(outpt):
                print(f"OK  - {outpt.split('/')[-1]}")
            else:
                todo.append((filepath, outpt))

    TOTAL = len(todo)

    for input_file, output_file in todo:
        T_COUNT += 1
        while T_COUNT >= M_COUNT:
            time.sleep(0.1)
        threading.Thread(target=convert_flac_to_alac, args=(input_file, output_file)).start()

    while T_COUNT > 0:
        time.sleep(0.1)

    os.system("stty sane")

    print("All conversions completed.")

    for album in allout:
        if should_ignore(album, album_list):
            dirpath = os.path.join(output_root, album)
            print(f"'{album}' found in output but not in input")
            if input("Delete it? (y/n) ").strip().lower() == 'y':
                print(f"Deleting {dirpath}")
                os.system(f"rm -rf '{dirpath}'")

    os._exit(0)
