import pygame, sys

pygame.init()
width = 640
height = 480

screen = pygame.display.set_mode((width,height))
done = False
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

bg = (127,127,127)


      
while not done:
   
   for event in pygame.event.get():
      screen.fill(bg)
      if event.type == pygame.QUIT:
         done = True
      font = pygame.font.SysFont("arial",55,bold=True,italic=True)
   words = font.render("Hello World",antialias=True,color=red)
   screen.blit(words,(screen.get_width() - 480 , screen.get_height() // 2))
   pygame.display.update()
   