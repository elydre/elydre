import itertools
import time
import pygame
from pygame.locals import *

class GrapheProjet4:
    """
    Recherche d'un chemin dans un labyrinthe.
    """
    def __init__(self, labyrinthe):
        self.hauteur = len(labyrinthe)
        self.largeur = len(labyrinthe[0])
        # On crée un dictionnaire vide
        self.listeAdjacence = {}
        # On génère la liste d'adjacence à partir du labyrinthe
        self.creeListeAdjacence(labyrinthe)
        self.echecs = {}

        self.trace(labyrinthe)

    def creeListeAdjacence(self, labyrinthe):
        """
        Fabrique la liste d'adjcence du graphe représentant le labyrinthe.
        """
        for y, x in itertools.product(range(self.hauteur), range(self.largeur)):
            self.listeAdjacence[(x, y)] = []
            if labyrinthe[y][x] == ".":
                if x > 0 and labyrinthe[y][x - 1] == ".":
                    self.listeAdjacence[(x, y)].append((x-1, y))
                if x + 1 < self.largeur and labyrinthe[y][x + 1] == ".":
                    self.listeAdjacence[(x, y)].append((x+1, y))
                if y > 0 and labyrinthe[y - 1][x] == ".":
                    self.listeAdjacence[(x, y)].append((x, y-1))
                if y + 1 < self.hauteur and labyrinthe[y + 1][x] == ".":
                    self.listeAdjacence[(x, y)].append((x, y+1))


    def trace(self, labyrinthe):
        """
        Méthode principale qui gère tous les affichages.
        """
        pygame.init()
        # Taille d'un carré de base
        self.tailleCarre = 50
        # On crée une fenêtre à la taille du labyrinthe
        self.fenetre = pygame.display.set_mode((self.tailleCarre*self.largeur, self.tailleCarre*self.hauteur))
        # On dessine le labyrinthe
        self.traceLabirynthe(labyrinthe)

        # On recherche un chemin
        chemin = self.trouveChemin()

        # On trace le chemin
        self.traceChemin(chemin)

        # On attend l'appui sur le bouton fermer de la fenêtre
        continuer = 1
        while continuer:
            for event in pygame.event.get():
                # Si appui sur le bouton fermer
                if event.type == QUIT:
                    continuer = 0

        pygame.quit()

    def traceLabirynthe(self,labyrinthe):
        """
        Trace le labyrinthe.

        Les cases noires représentent les murs.
        """
        carre = pygame.Surface((self.tailleCarre,self.tailleCarre), pygame.SRCALPHA)
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if labyrinthe[y][x] == "#":
                    color = (0, 0, 0, 255)
                elif labyrinthe[y][x] == ".":
                    color = (255, 255, 255, 255)
                carre.fill(color)
                self.fenetre.blit(carre, (x*self.tailleCarre, y*self.tailleCarre))
        #modifie la fenêtre
        pygame.display.flip()

    def traceChemin(self, chemin):
        """
        Trace le chemin dans le labyrinthe.

        chemin : liste de tuples contenant les coordonnées (x, y) des cases constituant le chemin
        """
        color = (255, 0, 0, 255)
        for i in range(len(chemin)-1):
            pygame.draw.line(self.fenetre, color, (chemin[i][0]*self.tailleCarre+int(self.tailleCarre/2), chemin[i][1]*self.tailleCarre+int(self.tailleCarre/2)), (chemin[i+1][0]*self.tailleCarre+int(self.tailleCarre/2), chemin[i+1][1]*self.tailleCarre+int(self.tailleCarre/2)), 5)

        pygame.display.flip()

    def effaceChemin(self, chemin):
        """
        Efface le chemin en appliquant des carrés blancs

        chemin : liste de tuples contenant les coordonnées (x, y) des cases constituant le chemin
        """
        carre = pygame.Surface((self.tailleCarre,self.tailleCarre), pygame.SRCALPHA)
        color = (255, 255, 255, 255)
        carre.fill(color)
        for coord in chemin:
            self.fenetre.blit(carre, (coord[0]*self.tailleCarre, coord[1]*self.tailleCarre))
        pygame.display.flip()

    def apercuChemin(self, chemin):
        """
        Trace le chemin actuel et l'efface aussitôt

        chemin : liste de tuples contenant les coordonnées (x, y) des cases constituant le chemin
        """
        self.traceChemin(chemin)
        time.sleep(0.02)
        self.effaceChemin(chemin)

    def trouveChemin(self):
        """
        Retourne un chemin entre le coin supérieur gauche et le coin inférieur droit ne passant que par les cases blanches.
        """
        return self.trouveRecursif((0,0), (self.largeur - 1, self.hauteur - 1), [])

    def trouveRecursif(self, start, end, chaine):
        """
        Partie récursive de l'algorithme de recherche de chemin
        """
        chaine.append(start)
        if start == end:
            return chaine
        for voisin in self.listeAdjacence[start]:
            # pour tout les noeuds adjacents pas encore visités
            if voisin not in chaine:
                chemin = self.trouveRecursif(voisin, end, chaine)
                if chemin != None:
                    return chemin
        chaine.remove(start)
        return None

lab_2 = ["..#.###...",
         "#.#...#.#.",
         "....#...#.",
         ".#####.###",
         ".#...#...#",
         "...#.#.###",
         "####.#....",
         "#....##.##",
         "..####...#",
         "#....#.#.."]


lab_3 = [".#....#......#....#...#.....#.",
         ".#.##.#.####.#.##.#.#.#.###.#.",
         "....#.#....#....#...#.#.#.#...",
         "###.#.##.#.#.##.#######...#.##",
         "....#....#......#....#..#.....",
         ".#######.#.###.##.##.#.######.",
         ".....#.......#....#..#........",
         "#.##.#.#####.######.##.#.#.###",
         "..#..#.#.....#......#..#.#..#.",
         ".##.##.#.#####.###.##.##.##...",
         "..###..#.........#.#..#...##.#",
         "#.#...##.#.#####.....####.#...",
         "#...###..#...#.#.###....#.###.",
         "#.###...####.#.#...##.#...#...",
         "..#...####...#.#........#.#.##",
         ".##.###....#.#.###.#.##.#.....",
         ".#....#.##.#.......#..#.#.##.#",
         ".#.##.#..#.####.#.###...#..#..",
         "...#..##.#.#....#.#.#.####.##.",
         "####.....#...####...#....#.#.."]

graphe = GrapheProjet4(lab_2)
