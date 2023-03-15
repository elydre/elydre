from time import sleep, time

import pygame

import mod.core as core

MAX_FPS = 60

# init pygame
pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("miam | logic simulator")

# init core
mouse = core.Mouseu()

# main loop
running = True
fps = MAX_FPS

loop_start = time()
loop_count = 0

while running:
    iter_start = time()
    loop_count += 1

    # clear screen
    screen.fill((0, 0, 0))

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            mouse.update_click(event.type == pygame.MOUSEBUTTONDOWN, event.button)
        if event.type == pygame.MOUSEMOTION:
            mouse.update_pos(event.pos)

    mouse.debug()

    # fps counter
    moy_fps = 1 / (time() - loop_start) * loop_count if loop_count > 10 else MAX_FPS
    to_sleep = (1 / MAX_FPS - (time() - iter_start)) - (1 - (moy_fps / MAX_FPS))

    if to_sleep > 0: sleep(to_sleep)

    fps_text = pygame.font.SysFont("Arial", 20).render(f"FPS: {round(fps, 1)} | Moy: {round(moy_fps, 1)}", True, (255, 255, 255))
    screen.blit(fps_text, (0, 0))

    # update screen
    pygame.display.update()
    fps = 1 / (time() - iter_start)

pygame.quit()
