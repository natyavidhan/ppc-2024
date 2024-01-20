import pygame
import cv2
import numpy as np

pygame.font.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
running = True

font = pygame.font.Font("Comfortaa.ttf", 40)

h = pygame.display.Info().current_h
w = pygame.display.Info().current_w

cap = cv2.VideoCapture(0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    head = pygame.font.Font("Comfortaa.ttf", 96).render("Anisha v1", True, (0, 0, 0))
    rect = head.get_rect()
    rect.center = (w//2, h//10)
    screen.blit(head, rect)

    c = font.render("Conversation", True, (0, 0, 0))
    rect = c.get_rect()

    _, frame = cap.read()
    frame = np.rot90(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame)
    rect = frame.get_rect()
    rect.center = (w//2, h//4)
    screen.blit(frame, rect)

    pygame.display.update()