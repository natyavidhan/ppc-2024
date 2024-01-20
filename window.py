import pygame

screen = pygame.display.set_mode((1280, 720))
running = True

pygame.display.set_caption("Anisha v1")

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill((255, 255, 255))

	pygame.display.update()