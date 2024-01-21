import pygame
import cv2
import numpy as np

pygame.font.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
running = True

font = pygame.font.Font("Comfortaa.ttf", 38)

h = pygame.display.Info().current_h
w = pygame.display.Info().current_w

cap = cv2.VideoCapture(0)

conversation = [
    (0, "Hello there! How can I help you today?"),
    (1, "Hi! I'm looking for some information about Python programming."),
    (
        0,
        "Sure, I'd be happy to assist you with that. What specifically would you like to know?",
    ),
    (1, "I'm interested in learning about lists and how to create them."),
    (
        0,
        "Great! Lists are a fundamental data structure in Python that allow you to store and organize collections of items. To create a list, you simply enclose a sequence of items in square brackets, like this: my_list = [1, 2, 3, 'apple', 'banana'].",
    ),
    (
        1,
        "Oh, that seems pretty straightforward. Can you tell me more about how to access and modify items within a list?",
    ),
    (
        0,
        "Absolutely! To access individual items in a list, you use their index, which starts from 0. For example, to get the first item in the list my_list, you would use my_list[0]. To modify items, you can also use their index. For instance, to change the second item to 'orange', you would use my_list[1] = 'orange'.",
    ),
    (
        1,
        "That makes sense. Thanks for the explanation! I think I'm starting to get the hang of lists now.",
    ),
    (
        0,
        "You're welcome! I'm glad I could help. If you have any other questions, feel free to ask.",
    ),
    (1, "I will. Thanks again!"),
]

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1
        # if y + fontHeight > rect.bottom:
        #     break
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1     
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left-(rect.width//2), y-(rect.height//2)))
        y += fontHeight + lineSpacing
        text = text[i:]

    return text

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    head = pygame.font.Font("Comfortaa.ttf", 96).render("Anisha v1", True, (0, 0, 0))
    rect = head.get_rect()
    rect.center = (w // 2, h // 10)
    screen.blit(head, rect)

    c = font.render("Speaker: Anisha", True, (0, 0, 0))
    rect = c.get_rect()
    rect.center = (w // 2, h // 2.5)
    screen.blit(c, rect)

    _, frame = cap.read()
    frame = np.rot90(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame)
    rect = frame.get_rect()
    rect.center = (w // 2, h // 4)
    rect.width = 640 / 1080 * w
    rect.height = 480 / 1920 * h
    screen.blit(frame, rect)

    text_rect = pygame.Rect(w // 2, h // 1.5, 640 / 1080 * w, 960 / 1920 * h)
    drawText(screen, "",(0, 0, 0), text_rect, font)


    pygame.display.update()
