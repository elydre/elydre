def ajouter_duree(total_secondes, duree):
    minutes, secondes = map(int, duree.split(":"))
    return total_secondes + minutes * 60 + secondes

def afficher_mm_ss(total_secondes):
    minutes = total_secondes // 60
    secondes = total_secondes % 60
    return f"{minutes:02d}:{secondes:02d}"

total = 0

while True:
    entree = input("Entrer une durée (MM:SS) ou 'q' pour quitter : ")

    if entree.lower() == "q":
        break

    total = ajouter_duree(total, entree)
    print("Total :", afficher_mm_ss(total))

print("Total final :", afficher_mm_ss(total))

""" list.txt example:
file 'track1.flac'
file 'track2.flac'
file 'track3.flac'
"""

# ffmpeg -f concat -safe 0 -i list.txt -c copy album.flac && ffmpeg -i album.flac album.wav && ffmpeg -i album.wav -ab 320k album.mp3
# ffmpeg -loop 1 -i main.png -i album.mp3 -c:v libx264 -tune stillimage -c:a copy -shortest -pix_fmt yuv420p -movflags +faststart video_youtube.mp4
