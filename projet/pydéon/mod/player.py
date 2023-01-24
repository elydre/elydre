import pygame, time
from _thread import start_new_thread

class Play:
    def __init__(self, nom):
        self.nom = nom
        self.runing = False
        pygame.mixer.init()
        self.son = pygame.mixer.Sound("wav/"+nom)
    
    def TH_play(self):
        self.runing = True
        self.son.play()
        while True:
            time.sleep(0.01)
            if not self.runing:
                pygame.mixer.stop()
                break
            #si la lecture est finie on relance
            if self.son.get_num_channels() == 0:
                self.son.play()
            

    def play(self):
        start_new_thread(self.TH_play, ())
    
    def stop(self):
        self.runing = False