import tkinter as tk


fenettre = tk.Tk()
fenettre.title("Calculatrice")
fenettre.geometry("280x450")

p = ("Helvetica", 20)

TEXTE = ""

class Clr:
    nb = "#222222"
    op = "#660066"
    eq = "#ff00ff"
    cl = "#cc00cc"

def add_to_text(char):
    global TEXTE
    TEXTE += str(char)
    display.config(text=TEXTE)

def clear_last():
    global TEXTE
    TEXTE = TEXTE[:-1]
    display.config(text=TEXTE)

def calc():
    global TEXTE
    try:
        res = eval(TEXTE)
        TEXTE = str(res)
        display.config(text=TEXTE)
    except Exception as e:
        display.config(text="Erreur")
        print(e)        # debug

# display area
display = tk.Label(fenettre, text=TEXTE, font=p, bg=Clr.nb, fg=Clr.eq)
display.place(x=0, y=0, width=280, height=100)

# num pad
[tk.Button(fenettre, bg = Clr.nb, fg = "#ffffff", font = p, text=i + 1, command = lambda i = i: add_to_text(i + 1)).place(x= (i*70) % (70 * 3), y= 310 - (i // 3) * 70, width=70, height=70) for i in range(9)]

# buttons
tk.Button(fenettre, bg = Clr.nb, fg = "#ffffff", font = p, text = "0", command = lambda: add_to_text("0")).place(x=0, y=380, width=140, height=70)      # zero
tk.Button(fenettre, bg = Clr.nb, fg = "#ffffff", font = p, text = ".", command = lambda: add_to_text(".")).place(x=140, y=380, width=70, height=70)     # point
tk.Button(fenettre, bg = Clr.eq, fg = "#ffffff", font = p, text = "=", command = calc).place(x=210, y=380, width=70, height=70)                         # egal
tk.Button(fenettre, bg = Clr.cl, fg = "#ffffff", font = p, text = "..", command = clear_last).place(x=210, y=100, width=70, height=70)                  # clear
tk.Button(fenettre, bg = Clr.op, fg = "#ffffff", font = p, text = "+", command = lambda: add_to_text(" + ")).place(x=210, y=170, width=70, height=70)   # add
tk.Button(fenettre, bg = Clr.op, fg = "#ffffff", font = p, text = "-", command = lambda: add_to_text(" - ")).place(x=210, y=240, width=70, height=70)   # sub
tk.Button(fenettre, bg = Clr.op, fg = "#ffffff", font = p, text = "*", command = lambda: add_to_text(" * ")).place(x=210, y=310, width=70, height=70)   # mul
tk.Button(fenettre, bg = Clr.op, fg = "#ffffff", font = p, text = "/", command = lambda: add_to_text(" / ")).place(x=0, y=100, width=70, height=70)     # div
tk.Button(fenettre, bg = Clr.op, fg = "#ffffff", font = p, text = "(", command = lambda: add_to_text("(")).place(x=70, y=100, width=70, height=70)      # open_bracket
tk.Button(fenettre, bg = Clr.op, fg = "#ffffff", font = p, text = ")", command = lambda: add_to_text(")")).place(x=140, y=100, width=70, height=70)     # close_bracket

fenettre.mainloop()
