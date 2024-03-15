from mutagen.flac import FLAC
import os, sys

album_count = 0
track_count = 0
edit_count = 0

def tofilename(s, is_dir=False):
    # remove non-ascii characters
    to_rep = [
        ["â", "a"],
        ["é", "e"],
        ["î", "i"],
        ["ô", "o"],
        ["û", "u"],

        ["Â", "A"],
        ["É", "E"],
        ["Î", "I"],
        ["Ô", "O"],
        ["Û", "U"],

        ["ø", "o"],
        ["Ø", "O"],
        ["æ", "ae"],
        ["Æ", "AE"],
        ["œ", "oe"],
        ["Œ", "OE"],

        ["ä", "a"],
        ["ë", "e"],
        ["ï", "i"],
        ["ö", "o"],
        ["ü", "u"],

        ["Ä", "A"],
        ["Ë", "E"],
        ["Ï", "I"],
        ["Ö", "O"],
        ["Ü", "U"],

        ["’", "'"],
        ["…", ""],
        ["–", "-"],
        ["—", "-"],
        ["“", ""],

        ["\"", ""],
        ["'", " "],
        [":", ""],
        ["?", ""],
        ["/", "-"],
    ]

    for r in to_rep:
        s = s.replace(r[0], r[1])

    s = s.encode("ascii", "ignore").decode()
    if is_dir:
        s = s.replace(".", "")

    while "  " in s:
        s = s.replace("  ", " ")

    return s.strip()

def rename_album(dir_path):
    global track_count, edit_count
    album_name = None
    album_artist = None
    for file in os.listdir(dir_path):
        if file.endswith("flac"):
            try:                
                path = os.path.join(dir_path, file)
                audio = FLAC(path)
                if album_name is None:
                    album_name = audio['album'][0]
                else:
                    if album_name != audio['album'][0]:
                        print(f"Album name mismatch: {album_name} != {audio['album'][0]}")
                        return
                if album_artist is None:
                    album_artist = audio['artist'][0].split(" - ")[0].split(",")[0].strip()
                try:    # multi track album
                    new_name = f"{int(audio['tracknumber'][0]):02d}. {album_artist} - {audio['title'][0]}"
                except: # one file album
                    new_name = f"{album_artist} - {audio['album'][0]}"
                new_name = tofilename(new_name) + ".flac"
                full_path = os.path.join(dir_path, new_name)
                track_count += 1
                if full_path == path:
                    continue
                if os.path.exists(full_path):
                    print(f"Error: {full_path} already exists")
                    input("Press Enter to continue...")
                    return
                os.rename(path, full_path)
                edit_count += 1
                print(f"    {new_name}")
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")
                return

    # rename album folder
    album_name = tofilename(f"{album_artist} - {album_name}", True)
    os.rename(dir_path, os.path.join(os.path.dirname(dir_path), album_name))

def is_album_dir(dir_path):
    # check if dir contains flac files and no subdirs
    flac_files = [file for file in os.listdir(dir_path) if
                    os.path.isfile(os.path.join(dir_path, file)) and file.endswith("flac")]
    subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    return len(flac_files) > 0 and len(subdirs) == 0

def recursive_rename_albums(root_dir):
    for dir_path, _, _ in os.walk(root_dir):
        if is_album_dir(dir_path):
            global album_count
            album_count += 1
            print(f"album: {dir_path}")
            rename_album(dir_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python renamer.py <root_dir>")
        sys.exit(1)
    root_dir = sys.argv[1]
    recursive_rename_albums(root_dir)
    print(f"Done, {album_count} albums renamed ({track_count} tracks, {edit_count} edited)")
