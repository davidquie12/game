import pygame
from collections import namedtuple

class Unit:
    def __init__(self, position, dir_vect):
        self.position = {"x": position[0], "y": position[1]}
        self.dir_vect = {"x": dir_vect[0], "y": dir_vect[1]}

    def load(self, image, surface):
        surface.blit(image, (self.position["x"], self.position["y"]))
        
    def scale_image(self, image, scale_factor):
        new_width = int(image.get_width() * scale_factor)
        new_height = int(image.get_height() * scale_factor)
        return pygame.transform.scale(image, (new_width, new_height))


class Paddle(Unit):
    width = 30
    height = 100
    max_speed = 1
    img = "venv/src/paddle.png"
    image = pygame.image.load(img)

    def __init__(self, position, dir_vect):
        super().__init__(position, dir_vect)
    
    def scale_image(self, scale_factor):
        return super().scale_image(self.image, scale_factor)


class Ball(Unit):
    radius = 5.0
    start_pos = [0, 0]
    img = "venv/src/ball.png"
    image = pygame.image.load(img)
    max_speed = 4

    def __init__(self, position, dir_vect):
        super().__init__(position, dir_vect)
        
    def scale_image(self, scale_factor):
        return super().scale_image(self.image, scale_factor)

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 640, 640
screen = pygame.display.set_mode((width, height))

# Set up colors
Color = namedtuple("Color", ("x", "y", "z"))
dark_blue = (0, 0, 145)

# Create paddles and ball
pad1 = Paddle([0, height / 2], [0, 0])
pad2 = Paddle([width - Paddle.image.get_width(), height / 2], [0, 0])
ball = Ball([width / 2, height / 2], [0, 0])

# Scale images
pad1.scale_image(0.5)
pad2.scale_image(0.5)
ball.scale_image(0.5)

# Main game loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            pad1.position["y"] -= 3
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            pad1.position["y"] += 3
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            pad2.position["y"] -= 3
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            pad2.position["y"] += 3

    # Game logic
    screen.fill(dark_blue)

    # Load and display the scaled images
    pad1.load(Paddle.image,screen)
    pad2.load(Paddle.image,screen)
    ball.load(Ball.image,screen)

    # Move the ball
    ball.position["x"] += ball.max_speed

    # Check for ball collisions with walls
    if ball.position["x"] >= screen.get_width() - ball.image.get_width()  or ball.position["x"] <= 0:
        ball.max_speed = -ball.max_speed

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
