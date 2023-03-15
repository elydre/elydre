class Mapeu:
    def __init__(self):
        self.objs = []

    def set_obj(self, obj):
        self.objs.append(obj)

class Objeu:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

class Mouseu:
    def __init__(self):
        self.pos = (0, 0)
        self.click = (False, False) # left, right
    
    def update_click(self, click, button):
        if button == 1:
            self.click = (click, self.click[1])
        elif button == 3:
            self.click = (self.click[0], click)

    def update_pos(self, pos):
        self.pos = pos

    def debug(self):
        print(f"Mouse: {self.pos} | Click: {self.click}")
