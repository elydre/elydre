from mutagen.flac import FLAC, Picture
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

OUTFILES = []

def tofilename(s):
    t = '’'

    for r in [["\xa0", " "], ["…", ""], ["“", ""], ["`", t], ["´", t], ["–", "-"], ["?", ""],
              ["—", "-"], ["/", "-"], [":", ""], ["\"", ""], ["'", t], [".", ""], ["\\", ""]]:
        s = s.replace(r[0], r[1])

    while "  " in s:
        s = s.replace("  ", " ")

    return s.strip()


def update_cover(path, album_cover):
    audio = FLAC(path)

    # remove all pictures
    audio.clear_pictures()

    # create a new picture from the album cover in 600x600
    img = Image.open(album_cover)
    img = img.convert("RGB")
    img = img.resize((500, 500), Image.LANCZOS)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG", quality=95)
    img_byte_arr.seek(0)

    # add the new picture to the audio file
    picture = Picture()
    picture.data = img_byte_arr.read()
    picture.type = 3 # front cover
    picture.mime = "image/jpeg"
    picture.desc = ""
    picture.width  = 500
    picture.height = 500
    audio.add_picture(picture)

    audio.save()

def make_tiny_cover(input_cover, output_cover):
    img = Image.open(input_cover)
    img = img.convert("RGB")
    img = img.resize((500, 500), Image.LANCZOS)
    img.save(output_cover, format="JPEG", quality=98)


def convert_flac_to_flac16(input_file, output_dir):
    """
    input FLAC file
    -> 16 / 24bit lossless 44.1 / 48kHz or more

    output FLAC file
    -> 16bit lossless 44.1 / 48kHz ONLY
    """

    global T_COUNT, COMPLETED

    for name in ["cover.jpg", "cover.png"]:
        cover_path = os.path.join(os.path.dirname(input_file), name)
        if os.path.exists(cover_path):
            break
    else:
        print(f"No cover file found for {input_file}!")
        os._exit(1)

    in_audio = FLAC(input_file)

    album_artist = in_audio.get("albumartist", [in_audio.get("artist", ["Unknown"])[0]])[0]
    artist       = in_audio.get("artist", ["Unknown"])[0]
    album_name   = in_audio.get("album", ["Unknown"])[0]
    track_number = in_audio.get("tracknumber", ["0"])[0]
    title        = in_audio.get("title", ["Unknown"])[0]

    output_file = os.path.join(output_dir, tofilename(album_artist), tofilename(album_name), f"{track_number}. {tofilename(artist) + ' - ' if artist != album_artist else ''}{tofilename(title)}.flac")
    OUTFILES.append(output_file)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    tiny_cover = os.path.join(os.path.dirname(output_file), "cover.jpg")

    if tiny_cover not in OUTFILES:
        OUTFILES.append(tiny_cover)

        if not os.path.exists(tiny_cover):
            print(f"Creating {tiny_cover}")
            make_tiny_cover(cover_path, tiny_cover)

    if os.path.exists(output_file):
        T_COUNT -= 1
        COMPLETED += 1
        return

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

    # print(f"IN: {input_srate} Hz -> OUT: {output_srate} Hz")

    if (subprocess.run([
        "ffmpeg",
        "-loglevel", "error",
        "-y",
        "-i", input_file,
        "-vn",
        "-map_metadata", "0",
        "-af", f"aresample={output_srate}:resampler=soxr:precision=28,aformat=sample_fmts=s16",
        "-c:a", "flac",
        "-compression_level", "5",
        output_file
    ]).returncode != 0):
        print(f"Error converting {input_file} to ALAC!")
        os._exit(1)

    update_cover(output_file, cover_path)

    T_COUNT -= 1
    COMPLETED += 1

    print(f"{COMPLETED/TOTAL * 100:.2f}% - {output_file.split('/')[-1]}")


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

    input_root  = sys.argv[1]
    output_root = sys.argv[2]

    if not os.path.exists("ipod5_list.txt"):
        print("error: ipod5_list.txt not found!")
        sys.exit(1)

    with open("ipod5_list.txt", 'r') as f:
        album_list = [line.strip() for line in f if line.strip()]

    todo = []

    if not os.path.isdir(input_root):
        print(f"Error: {input_root} is not a directory.")
        sys.exit(1)

    for album in os.listdir(input_root):
        if not os.path.isdir(os.path.join(input_root, album)):
            continue

        if should_ignore(album, album_list):
            continue

        for file in os.listdir(os.path.join(input_root, album)):
            filepath = os.path.join(input_root, album, file)

            if not (os.path.isfile(filepath) and filepath.lower().endswith(".flac")):
                continue

            todo.append(filepath)

    TOTAL = len(todo)

    for input_file in todo:
        T_COUNT += 1
        while T_COUNT >= M_COUNT:
            time.sleep(0.1)
        threading.Thread(target=convert_flac_to_flac16, args=(input_file, output_root)).start()

    while T_COUNT > 0:
        time.sleep(0.1)

    os.system("stty sane")

    # list all output files and remove those that are not in OUTFILES
    for root, dirs, files in os.walk(output_root):
        for file in files:
            path = os.path.join(root, file)
            if path in OUTFILES:
                continue
            print(f"do you want to remove {path}? (Y/n)")
            if input() in ["Y", "y", ""]:
                os.remove(path)
        
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if os.listdir(dir_path):
                continue
            print(f"do you want to remove empty directory {dir_path}? (Y/n)")
            if input() in ["Y", "y", ""]:
                os.rmdir(dir_path)

    print("All conversions completed.")

    os._exit(0)
