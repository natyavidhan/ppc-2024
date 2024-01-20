import pygame
import cv2

pygame.font.init()

screen = pygame.display.set_mode((720, 1280))
running = True

pygame.display.set_caption("Anisha v1")
font = pygame.font.Sysfont("consolas", 32)
conversation = [
   (0, "Hello there! How can I help you today?"),
   (1, "Hi! I'm looking for some information about Python programming."),
   (0, "Sure, I'd be happy to assist you with that. What specifically would you like to know?"),
   (1, "I'm interested in learning about lists and how to create them."),
   (0, "Great! Lists are a fundamental data structure in Python that allow you to store and organize collections of items. To create a list, you simply enclose a sequence of items in square brackets, like this: my_list = [1, 2, 3, 'apple', 'banana']."),
   (1, "Oh, that seems pretty straightforward. Can you tell me more about how to access and modify items within a list?"),
   (0, "Absolutely! To access individual items in a list, you use their index, which starts from 0. For example, to get the first item in the list my_list, you would use my_list[0]. To modify items, you can also use their index. For instance, to change the second item to 'orange', you would use my_list[1] = 'orange'."),
   (1, "That makes sense. Thanks for the explanation! I think I'm starting to get the hang of lists now."),
   (0, "You're welcome! I'm glad I could help. If you have any other questions, feel free to ask."),
   (1, "I will. Thanks again!"),
]


while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill((255, 255, 255))

	for i, j in conversation:
		user = "bot" if i == 0 else "user"
		text = font.render(j, True, (0, 0, 0))

		scre

	pygame.display.update()