from mutagen.mp4 import MP4, MP4Cover
from PIL import Image
import io, os, sys


def update_cover(audio, album_cover):
    if album_cover is None:
        return False

    # Redimensionne l'image en 600x600 JPEG
    img = Image.open(album_cover)
    img = img.convert("RGB")
    img = img.resize((600, 600), Image.LANCZOS)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_data = img_byte_arr.getvalue()

    # Ajoute la nouvelle couverture
    cover = MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)
    audio["covr"] = [cover]

    try:
        title = audio.get("\xa9nam", ["(unknown)"])[0]
        print(f"[✓] {title} → cover mise à jour")
    except Exception:
        pass

    audio.save()
    return True


def rename_album(dir_path):
    # check for album cover
    for name in ["cover.jpg", "cover.png"]:
        if os.path.exists(os.path.join(dir_path, name)):
            album_cover = os.path.join(dir_path, name)
            break
    else:
        print("  No cover file found, please add one")
        MISIMG_COUNT += 1
        album_cover = None

    for file in os.listdir(dir_path):
        if not file.endswith("m4a"):
            continue

        path = os.path.join(dir_path, file)

        # global metadata
        audio = MP4(path)

        EDIT_COUNT += update_cover(audio, album_cover)


def is_album_dir(dir_path):
    # check if dir contains m4a files and no subdirs
    m4a_files = [file for file in os.listdir(dir_path) if
                    os.path.isfile(os.path.join(dir_path, file)) and file.endswith("m4a")]
    subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    return len(m4a_files) > 0 and len(subdirs) == 0


def recursive_rename_albums(root_dir):
    dirs_paths = [e for e, _, _ in os.walk(root_dir) if is_album_dir(e)]

    # sort directories by name
    dirs_paths.sort(key=lambda x: x.lower())

    for dir_path in dirs_paths:
        dir_path = os.path.abspath(dir_path)
        global ALBUM_COUNT
        ALBUM_COUNT += 1
        print(f"\033[90m{dir_path.split('/')[-1]}\033[0m")
        rename_album(dir_path)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "-r":
        RELAOD_ALL = True

    elif len(sys.argv) != 1:
        print("Usage: python renamer.py [-r]")
        sys.exit(1)

    recursive_rename_albums(".")
