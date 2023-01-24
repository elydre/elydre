from os import popen
import tkinter as tk

def convert(entre):
	entre = entre.replace(".","yhujgfdx")
	entre = entre.replace("-","gbhnjklm")
	entre = entre.replace("*","qwsxdcfv")
	entre = entre.replace(" ","aqzsedrf")
	entre = entre.replace("\n","gtfrdesz")
	entre = "".join(e for e in entre if e.isalnum())
	entre = entre.replace("aqzsedrf"," ")
	entre = entre.replace("gtfrdesz","\n")
	entre = entre.replace("qwsxdcfv","*")
	entre = entre.replace("gbhnjklm","-")
	entre = entre.replace("yhujgfdx",".")
	return(entre)

y = len(popen('wsl --list -v').read().split("\n"))*20

fenetre = tk.Tk()
fenetre.attributes("-fullscreen", False)
fenetre.geometry(f"520x{y}")
fenetre.resizable(width=0, height=1)
fenetre.title("wsl statut")


def wsl():
	Label_wsl.config(text=convert(popen("wsl --list -v").read()))
	Label_wsl.after(2000, wsl)

Label_wsl = tk.Label(fenetre,text=convert(popen("wsl --list -v").read()), font=("consolas", 13, "bold"),justify="left", anchor="nw")
Label_wsl.place(x=20, y=20, width=500, height=250)

wsl()

fenetre.mainloop()
