# open cat.png and convert it to a list of pixels

import itertools
import pygame

CAT_WIDTH = 32
CAT_HEIGHT = 32
CAT_COEF = 4

CAT_SPEED = 5

pygame.init()

def load_cat_sprits(path):
    image = pygame.image.load(path)

    img_pixel = pygame.PixelArray(image)
    img_width, img_height = image.get_size()

    cats = []

    for i in range(img_width // CAT_WIDTH * img_height // CAT_HEIGHT):
        lines = [[] for _ in range(CAT_WIDTH * CAT_COEF)]
        for x, y, j, _ in itertools.product(range(CAT_WIDTH), range(CAT_HEIGHT), range(CAT_COEF), range(CAT_COEF)):
            lines[x * CAT_COEF + j].append(
                img_pixel[
                            x + (i % (img_width // CAT_WIDTH)) * CAT_WIDTH,
                            y + (i // (img_width // CAT_WIDTH)) * CAT_HEIGHT
                        ]
            )

        cats.append(pygame.Surface((CAT_WIDTH * CAT_COEF, CAT_HEIGHT * CAT_COEF), pygame.SRCALPHA))
        cats[-1].lock()
        for x in range(CAT_WIDTH * CAT_COEF):
            for y in range(CAT_HEIGHT * CAT_COEF):
                cats[-1].set_at((x, y), lines[x][y])
        cats[-1].unlock()

    return cats

class Cat:
    def __init__(self, path):
        self.cat_sprits = load_cat_sprits(path)
        self.x = 0
        self.y = 0
    
    def draw(self, surface, x, y, index):
        surface.blit(self.cat_sprits[index], (x, y))

    def walk_to(self, x, y):
        # dont teleport the cat but walk to the position
        vector = (x - self.x, y - self.y)
        length = (vector[0] ** 2 + vector[1] ** 2) ** 0.5
        if length != 0:
            vector = (vector[0] / length, vector[1] / length)
            self.x += vector[0] * CAT_SPEED
            self.y += vector[1] * CAT_SPEED

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

bob = Cat("cat.png")

while not pygame.event.get(pygame.QUIT):
    screen.fill((40,30,50))

    # draw at the mouse position a red circle

    x, y = pygame.mouse.get_pos()

    pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)
    bob.walk_to(x, y)
    bob.draw(screen, bob.x, bob.y, 0)

    pygame.display.flip()
    clock.tick(60)