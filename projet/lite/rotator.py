import tkinter as tk
from PIL import Image, ImageTk
import os
from _thread import start_new_thread

fenettre = tk.Tk()
fenettre.title("image Rotator")
fenettre.geometry("800x800")
canvas = tk.Canvas(fenettre, width=800, height=800)

index = 0
image_name = ""

def get_image(folder_path):
    return [Image.open(os.path.join(folder_path, filename)) for filename in os.listdir(folder_path) if filename.endswith(".jpg")]


def show_image(image):
    global image_tk
    global image_name
    image_name = image.filename
    image_tk = ImageTk.PhotoImage(image)
    size = (image.size[0], image.size[1])
    image_tk = ImageTk.PhotoImage(image.resize((800, 600) if size[0] > size[1] else (600, 800)))
    canvas.create_image(400, 400, image=image_tk)
    canvas.pack()

def next_image(degrees):
    global index
    global image_name
    start_new_thread(rotate_image, (degrees, images[index], image_name))
    index += 1
    if index >= len(images):
        index = 0
    show_image(images[index])


def rotate_image(degrees, image, name):
    name = name.split("/")[-1]
    size = list(image.size)[::-1] if degrees in [90, -90] else image.size
    rotated_image = image.resize((12000, 12000)).rotate(degrees)
    rotated_image = rotated_image.resize(size)
    rotated_image.save(f"./rimg/{name}")
    print(f"rotate end for {name}")

images = get_image("./images/")

fenettre.bind("<Left>", lambda event: next_image(-90))
fenettre.bind("<Up>", lambda event: next_image(0))
fenettre.bind("<Right>", lambda event: next_image(90))
fenettre.bind("<Down>", lambda event: next_image(180))


show_image(images[0])
fenettre.mainloop()
