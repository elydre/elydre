import random
import pygame
import math

pygame.init()
PG_SCREEN = pygame.display.set_mode((800, 800))

TRACE_LENGTH = 500

def get_trace_color(defaut_color, index):
    return (int(defaut_color[0] * (index / TRACE_LENGTH)), int(defaut_color[1] * (index / TRACE_LENGTH)), int(defaut_color[2] * (index / TRACE_LENGTH)))

def randfloat(a, b):
    return random.random() * (b - a) + a

class Vector:
    def __init__(self, direction, magnitude):
        self.direction = direction
        self.magnitude = magnitude

    def __add__(self, other):
        # calculate the x and y components of the vectors
        x = self.magnitude * math.cos(self.direction) + other.magnitude * math.cos(other.direction)
        y = self.magnitude * math.sin(self.direction) + other.magnitude * math.sin(other.direction)

        # calculate the magnitude of the vector
        magnitude = math.sqrt(x**2 + y**2)

        # calculate the direction of the vector
        direction = math.atan2(y, x)

        # return the new vector
        return Vector(direction, magnitude)

class Planet:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = (radius**10) / 100000000
        self.velo = Vector(0, 0)
        self.last_pos = []
        self.links = []

    def draw(self):
        pygame.draw.circle(PG_SCREEN, self.color, (self.x, self.y), self.radius)
        for i in range(len(self.last_pos) - 1):
            pygame.draw.line(PG_SCREEN, get_trace_color(self.color, i), self.last_pos[i], self.last_pos[i + 1], 1)

    def set_velocity(self, velocity):
        self.velo = velocity
    
    def add_link(self, others):
        if type(others) == list:
            for other in others:
                self.links.append(other)
        else:
            self.links.append(others)
    
    def update(self):
        self.x += self.velo.magnitude * math.cos(self.velo.direction)
        self.y += self.velo.magnitude * math.sin(self.velo.direction)

        if self.x < 0 or self.x > 800:
            self.velo.direction = math.pi - self.velo.direction
            self.velo.direction %= 2 * math.pi
        if self.y < 0 or self.y > 800:
            self.velo.direction = -self.velo.direction
            self.velo.direction %= 2 * math.pi

        if self.x < 0:
            self.x = 0
        elif self.x > 800:
            self.x = 800

        self.last_pos.append((self.x, self.y))
        if len(self.last_pos) > TRACE_LENGTH:
            self.last_pos.pop(0)
    
    def get_distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def calc_gravity(self, other):
        distance = self.get_distance(other)
        if distance == 0:
            return Vector(0, 0)

        gravity = (self.mass * other.mass / distance**2) / 10000

        direction = math.atan2(other.y - self.y, other.x - self.x)

        # gravity = min(gravity, distance / 2)
    
        return Vector(direction, gravity)
    
    def apply_gravity(self, other):
        gravity = self.calc_gravity(other)
        self.velo += gravity
    
    def apply_all_gravity(self):
        for other in self.links:
            if other != self:
                self.apply_gravity(other)


sun = Planet(400, 400, 20, (255, 255, 0))

planets = [None for _ in range(5)]

planets[0] = Planet(400, 200, 9, (0, 0, 255))       # neptune
planets[1] = Planet(100, 400, 12, (255, 0, 0))      # titanus
planets[2] = Planet(100, 600, 6, (0, 255, 255))     # uranus
planets[3] = Planet(700, 600, 4, (0, 255, 0))       # auror
planets[4] = Planet(100, 100, 7, (255, 255, 255))   # white

planets[0].set_velocity(Vector(math.pi, 1.2))
planets[1].set_velocity(Vector(math.pi / 2, 4))
planets[2].set_velocity(Vector(-math.pi / 2, .4))
planets[3].set_velocity(Vector(math.pi, .3))
planets[4].set_velocity(Vector(math.pi / 4, .1))

for _ in range(10):
    planets.append(Planet(random.randint(0, 800), random.randint(0, 800), random.randint(1, 3), (random.randint(10, 180), random.randint(10, 180), random.randint(10, 180))))
    planets[-1].set_velocity(Vector(randfloat(-math.pi, math.pi), randfloat(0, .1)))

for planet in planets:
    planet.add_link([p for p in planets if p != planet] + [sun])

mouse_down = False

while True:
    PG_SCREEN.fill((0, 0, 0))

    for planet in planets:
        planet.apply_all_gravity()
        planet.update()
        planet.draw()

    sun.update()
    sun.draw()

    pygame.display.update()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            sun.x, sun.y = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_down:
                sun.x, sun.y = pygame.mouse.get_pos()
