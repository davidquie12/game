import pygame
import sys

pygame.init()
width = 640
height = 480

screen = pygame.display.set_mode((width, height))
done = False
red = (255, 0, 0)
blue = (0, 0, 255)

bg = (127, 127, 127)

x = 0
y = screen.get_height() // 2
speed = 1

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            done = True

    screen.fill(bg)
    font = pygame.font.SysFont("arial", 55)
    words = font.render("Hello World", True, red)
    screen.blit(words, (x, y))
    x += speed

    if x >= width - words.get_width() or x <= 0:
        speed = -speed

    pygame.display.update()

pygame.quit()
sys.exit()
