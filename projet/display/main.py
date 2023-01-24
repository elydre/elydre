'''    _             _
  ___ | | _   _   __| | _ __   ___
 / _ \| || | | | / _` || '__| / _ |
|  __/| || |_| || (_| || |   |  __/
 \___||_| \__, | \__,_||_|    \___|
          |___/
___________________________________

 - codé en : UTF-8
 - langage : python3
 - GitHub  : github.com/elydre
 - Licence : GNU GPL v3
'''

#import

from PIL import Image,ImageDraw
from utils import *
from page import *
import time, sys
from os import system

# init
run_command("sudo resize2fs /dev/mmcblk0p2")

background_color_config = 255
page = Page(background_color_config)
page.timer = 1
menu_image = Image.new('1', (epd.height, epd.width), 255)
menu_draw = ImageDraw.Draw(menu_image)

epd.init(epd.FULL_UPDATE)
epd.displayPartBaseImage(epd.getbuffer(menu_image)) 
epd.init(epd.PART_UPDATE)

global servinfo, msg, to_sleep
serveur = ""
msg = ""
to_sleep = 0.1

def clear(a,b,c,d):
    menu_draw.rectangle((a, b , c ,d), fill = 0)
    epd.displayPartial(epd.getbuffer(menu_image))
    time.sleep(to_sleep)
    menu_draw.rectangle((a, b , c ,d), fill = 255)
    epd.displayPartial(epd.getbuffer(menu_image))
    time.sleep(to_sleep)

def aff(quoi):
    
    if quoi == "h":
        clear(0, 0 , 255 ,23)
        for _ in range(8):
            menu_draw.text((60, 5), time.strftime('%H:%M - %d/%m') , font = font(16), fill = 0)
            epd.displayPartial(epd.getbuffer(menu_image))
            time.sleep(to_sleep)

    if quoi == "s":
        clear(5, 25 , 245 ,50)
        for _ in range(2):
            menu_draw.rectangle((5, 25 , 245 ,50 ), outline = 0)
            menu_draw.text((10, 25), serveur , font = font(20), fill = 0)
            epd.displayPartial(epd.getbuffer(menu_image))
            time.sleep(to_sleep)

    if quoi == "m":
        clear(0, 53,255, 255)
        for _ in range(2):
            menu_draw.text((10, 53), msg , font = font(20), fill = 0)
            epd.displayPartial(epd.getbuffer(menu_image))
            time.sleep(to_sleep)


aff("h")
while True:
    for _ in range(20):
        for _ in range(3):
            system("python3 /home/pi/nas-kit-master/actu.py")
            temp = open("/home/pi/nas-kit-master/data.txt", "r").read()
            tpS = temp.split("nvifgudhihgifukdh")[0]
            tpM = temp.split("nvifgudhihgifukdh")[1]

            if tpS != serveur:
                serveur = tpS
                aff("s")

            if tpM != msg:
                msg = tpM
                if msg == "pf4: §sd":
                    sys.exit()
                aff("m")
            time.sleep(5)

        aff("h")
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(menu_image))
    epd.init(epd.PART_UPDATE)
    time.sleep(3)
    aff("s")
    aff("m")