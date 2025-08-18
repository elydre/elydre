from mutagen.flac import FLAC, Picture
from PIL import Image
import io, os, sys
import pykakasi


kks = pykakasi.kakasi()


ALBUM_COUNT  = 0
TRACK_COUNT  = 0
EDIT_COUNT   = 0
MISIMG_COUNT = 0

RELAOD_ALL = False # -r option

REQUIRED_TAGS = ["artist", "album", "title", "date"]
OPTIONAL_TAGS = ["tracknumber", "copyright", "isrc"]


def say_issue(track, msg):
    print(f"Error: {track}: {msg}")
    input("Press Enter to continue...")


def say_info(track, msg):
    print(f"  {track}: {msg}")


def tofilename(s):
    def transliterate_japanese(s):
        result = ""

        for e in kks.convert(s):
            result += e['hepburn']
            for c in e['orig']:
                if '\u4e00' <= c <= '\u9fff' or '\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff':
                    result += " "
                    break

        return result.strip()

    for r in [["\xa0", " "], ["œ", "oe"], ["Œ", "OE"],
              ["æ", "ae"], ["Æ", "AE"], ["’", "'"], ["…", ""],
              ["“", ""], ["`", "'"], ["´", "'"]]:
        s = s.replace(r[0], r[1])

    s = transliterate_japanese(s.replace("\xa0", " "))

    for r in [["–", "-"], ["—", "-"], ["/", "-"], ["!", ""],
              [":", ""], [";", ""], [",", ""], ["\"", ""],
              ["'", " "], [".", ""],  ["?", ""], ["<", ""],
              [">", ""],  ["\\", ""], ["|", ""]]:
        s = s.replace(r[0], r[1])

    s = s.encode("ascii", "ignore").decode()

    while "  " in s:
        s = s.replace("  ", " ")

    return s.strip()


def get_track_year(track, date):
    if date is None:
        return None
    if len(date) == 4 and date.isdigit():
        return date
    if len(date) == 10 and date[4] == "-" and date[7] == "-":
        try:
            year = date.split("-")[0]
            if len(year) == 4 and year.isdigit():
                return year
        except:
            pass
    if len(date) == 10 and date[2] == "-" and date[5] == "-":
        try:
            year = date.split("-")[2]
            if len(year) == 4 and year.isdigit():
                return year
        except:
            pass

    say_issue(track, "invalid date format {date}")
    return None


def update_mdata(audio):
    need_save = False

    track_name = audio["title"][0] if "title" in audio else None
    if track_name is None: track_name = "???"

    # check required tags
    for tag in REQUIRED_TAGS:
        if tag not in audio or len(audio[tag]) == 0:
            say_issue(track_name, f"{tag} not found")
            return False

    # full date -> year
    date = audio["date"][0]
    year = get_track_year(track_name, date)
    if year is not None and year != date:
        say_info(track_name, f"date {date} -> {year}")
        audio["date"] = year
        need_save = True

    # "tracknumber/totaltracks" -> "tracknumber"
    tracknumber = audio["tracknumber"][0]

    if "/" in tracknumber:
        tracknumber = tracknumber.split("/")[0]
    try:
        tracknumber = str(int(tracknumber))
    except:
        say_issue(track_name, f"invalid tracknumber {tracknumber}")
        return False
    if len(tracknumber) > 2 or tracknumber < "1":
        say_issue(track_name, f"invalid tracknumber {tracknumber}")
        return False
    if len(tracknumber) == 1:
        tracknumber = "0" + tracknumber
    if tracknumber != audio["tracknumber"][0]:
        say_info(track_name, f"tracknumber {audio['tracknumber'][0]} -> {tracknumber}")
        audio["tracknumber"] = tracknumber
        need_save = True

    removed_tags = []

    # remove useless tags
    for key in audio.keys():
        if key not in REQUIRED_TAGS and key not in OPTIONAL_TAGS:
            del audio[key]
        elif not isinstance(audio[key], list):
            say_issue(f"invalid type for {key}: {type(audio[key])}")
            continue
        elif len(audio[key]) == 0:
            del audio[key]
        elif len(audio[key]) > 1:
            audio[key] = audio[key][0]
        else:
            continue

        removed_tags.append(key)
        need_save = True

    if len(removed_tags) > 0:
        print(f"  {track_name}: removing tags: {', '.join(removed_tags)}")

    if need_save:
        audio.save()
        return True
    return False


def update_cover(audio, album_cover):
    if album_cover is None:
        return False

    # check if the cover is already in the right format
    if not RELAOD_ALL and len(audio.pictures) == 1 and audio.pictures[0].width == 600 and \
            audio.pictures[0].height == 600 and audio.pictures[0].type == 3:
        return False

    # remove all pictures
    audio.clear_pictures()

    # create a new picture from the album cover in 600x600
    img = Image.open(album_cover)
    img = img.convert("RGB")
    img = img.resize((600, 600), Image.LANCZOS)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)

    # add the new picture to the audio file
    picture = Picture()
    picture.data = img_byte_arr.read()
    picture.type = 3 # front cover
    picture.mime = "image/jpeg"
    picture.desc = ""
    picture.width  = 600
    picture.height = 600
    audio.add_picture(picture)

    say_info(audio["title"][0], f"new cover generated")

    audio.save()
    return True


def rename_album(dir_path):
    global TRACK_COUNT, EDIT_COUNT, MISIMG_COUNT
    album_name = None
    album_artist = None

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
        if not file.endswith("flac"):
            continue

        path = os.path.join(dir_path, file)

        # global metadata
        try:
            audio = FLAC(path)

            edited  = update_mdata(audio)
            edited |= update_cover(audio, album_cover)

            if album_name is None:
                album_name = audio['album'][0]
            elif album_name != audio['album'][0]:
                say_issue(file, f"album name mismatch: {album_name} != {audio['album'][0]}")
                return

            if album_artist is None and album_artist != "various":
                album_artist = audio['artist'][0]
            elif album_artist != audio['artist'][0]:
                album_artist = "various"

            try:    # multi track album
                new_name = f"{int(audio['tracknumber'][0]):02d}. {tofilename(audio['artist'][0])} - {tofilename(audio['title'][0])}.flac"
            except: # one file album
                new_name = f"{audio['artist'][0]} - {tofilename(audio['album'][0])}.flac"

            full_path = os.path.join(dir_path, new_name)
            TRACK_COUNT += 1

            if full_path == path:
                if edited:
                    EDIT_COUNT += 1
                continue

            if os.path.exists(full_path):
                say_issue(file, f"file already exists: {full_path}")
                return

            say_info(file, f"renaming to {new_name}")
            os.rename(path, full_path)
            EDIT_COUNT += 1

        except Exception as e:
            say_issue(file, f"Error: {e}")
            return

    # rename album folder
    album_name = f"{tofilename(album_artist)} - {tofilename(album_name)}"
    os.rename(dir_path, os.path.join(os.path.dirname(dir_path), album_name))


def is_album_dir(dir_path):
    # check if dir contains flac files and no subdirs
    flac_files = [file for file in os.listdir(dir_path) if
                    os.path.isfile(os.path.join(dir_path, file)) and file.endswith("flac")]
    subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    return len(flac_files) > 0 and len(subdirs) == 0


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
        print("Usage: python album_formater.py [-r]")
        sys.exit(1)

    recursive_rename_albums(".")
    print(f"Done, {ALBUM_COUNT} albums ({TRACK_COUNT} tracks, {EDIT_COUNT} edited, {MISIMG_COUNT} missing covers)")
