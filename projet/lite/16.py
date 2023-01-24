import tkinter as tk

class Case:
    def __init__(self, plateau):
        self.bouton = tk.Button(plateau.fenettre, text="", bg='#DDDDDD', command=lambda plateau = plateau: self.jouer_case(plateau))
        self.state = -1

    def place(self, i):
        self.bouton.place(x=30 + i//3*120, y=30 + i%3*120, width=100, height=100)

    def jouer_case(self, plateau):
        if self.state == -1:
            self.state = PLAYER
            self.bouton.config(background="#4281f5" if PLAYER == 1 else "#32e66b", activebackground="#FF0000")
            plateau.play_done()

class Plateau:
    def __init__(self):
        self.fenettre = tk.Tk()
        self.fenettre.title("MORT PION")
        self.fenettre.geometry("400x450")
        self.fenettre.resizable(width=False, height=False)
        self.fenettre.configure(background='#FFFFFF')
        self.info = tk.Label(self.fenettre, text="Au tour du joueur 1", bg='#FFFFFF')
        self.info.configure(font=("Courier", 20))
        self.info.place(x=0, y = 380, width=400, height=50)
        self.cases = []

    def load_case(self):
        for c in self.cases:
            c.destroy()

        for i in range(9):
            self.cases.append(Case(self))
            self.cases[i].place(i)

    def chek_gagnant(self):
        for i in range(3):
            if self.cases[i*3].state == self.cases[i*3+1].state == self.cases[i*3+2].state != -1:
                return True
        for i in range(3):
            if self.cases[i].state == self.cases[i+3].state == self.cases[i+6].state != -1:
                return True
        if self.cases[0].state == self.cases[4].state == self.cases[8].state != -1:
            return True
        if self.cases[2].state == self.cases[4].state == self.cases[6].state != -1:
            return True

    def is_full(self):
        return all(c.state != -1 for c in self.cases)

    def end_game(self):
        for c in self.cases:
            c.bouton.config(state="disabled")
        
        self.info.after(3000, self.fenettre.destroy)


    def play_done(self):
        global PLAYER

        if self.chek_gagnant():
            self.info.config(text=f"Le joueur {str(PLAYER + 1)} a gagné")
            self.end_game()

        elif self.is_full():
            self.info.config(text="Match nul")
            self.end_game()

        else:
            PLAYER = not PLAYER
            self.info.config(text=f"Au tour du joueur {str(PLAYER + 1)}")


    def loop(self):
        self.fenettre.mainloop()
    
global PLAYER
PLAYER = 0

p = Plateau()
p.load_case()


p.loop()