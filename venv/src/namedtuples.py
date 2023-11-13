import pygame
import sys
from collections import namedtuple

pygame.init()
width = 640
height = 480

surface = pygame.display.set_mode((width, height))
done = False
color1 = namedtuple("red",("x","y","z"))
color2 = namedtuple("blue",("x","y","z"))
red = color1(255, 0, 0)
blue = color2(0, 0, 255)

bg_color = namedtuple("background_color",("x","y","z"))
bg = bg_color(127, 127, 127)

ball = namedtuple("ball_coord",["x","y","speed"])
p = ball(10,surface.get_height() // 2,0.2)


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            done = True

    surface.fill(bg)   
     
    p = p._replace(x=p.x + p.speed)

    if p.x >= width  or p.x <= 0:
        p = p._replace(speed=-p.speed)
        

    pygame.draw.rect(surface, red, rect=pygame.Rect(p.x,p.y,20,40))
    pygame.display.update()

pygame.quit()
sys.exit()
