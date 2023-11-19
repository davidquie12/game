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
    
    max_speed = 1
    img = "venv/src/paddle.png"
    image = pygame.image.load(img)
    height = image.get_height()
    width = image.get_height()
    def __init__(self, position, dir_vect):
        super().__init__(position, dir_vect)

    def scale_image(self, scale_factor):
        return super().scale_image(self.image, scale_factor)


class Ball(Unit):
    radius = 5.0
    start_pos = [0, 0]
    img = "venv/src/ball.png"
    image = pygame.image.load(img)
    width = image.get_width()
    height = image.get_height()
    max_speed = 4

    def __init__(self, position, dir_vect):
        super().__init__(position, dir_vect)
        
    def scale_image(self, scale_factor):
        return super().scale_image(self.image, scale_factor)
    
class Boundary:
    
    def __init__(self, width=640, height=640):
        self.width = width
        self.height = height
        self.top = 0
        self.bottom = height -1
        self.left = 0
        self.right = width - 1

    
class Collision:
    @staticmethod
    def collide_with(L_pad: Paddle, R_pad: Paddle, ball: Ball):
        field = Boundary()
        
        # Ball and Paddle Collision with left paddle
        if (
            ball.position["x"] <= L_pad.position["x"] + L_pad.image.get_width()
            and ball.position["y"] >= L_pad.position["y"]
            and ball.position["y"] + ball.image.get_height() <= L_pad.position["y"] + L_pad.image.get_height()
        ):
            ball.dir_vect["x"] *= -1
            hit_pos = (ball.position["y"] + ball.image.get_height() / 2) - L_pad.position["y"]
            paddle_center = L_pad.image.get_height() / 2
            normalized_hit_pos = (hit_pos - paddle_center) / paddle_center
            ball.dir_vect["y"] = normalized_hit_pos

        # Ball and Paddle Collision with right paddle
        if (
            ball.position["x"] + ball.image.get_width() >= R_pad.position["x"]
            and ball.position["y"] >= R_pad.position["y"]
            and ball.position["y"] + ball.image.get_height() <= R_pad.position["y"] + R_pad.image.get_height()
            ):
            ball.dir_vect["x"] *= -1
            hit_pos = (ball.position["y"] + ball.height / 2) - R_pad.position["y"]
            paddle_center = R_pad.height / 2
            normalized_hit_pos = (hit_pos - paddle_center) / paddle_center
            ball.dir_vect["y"] = normalized_hit_pos

        # Ball and Boundary Collision works
        if ball.position["y"] <= field.top or ball.position["y"] + ball.image.get_height() >= field.bottom:
            ball.dir_vect["y"] *= -1

        if ball.position["x"] <= field.left or ball.position["x"] + ball.image.get_width() >= field.right:
            pygame.quit()
        #score

        # paddles works
        if L_pad.position["y"] <= field.top:
            L_pad.position["y"] = field.top
          
        if L_pad.position["y"] + L_pad.image.get_height() >= field.bottom:
            L_pad.position["y"] = field.bottom - L_pad.image.get_height()
            
        if R_pad.position["y"] <= field.top:
            R_pad.position["y"] = field.top
          
        if R_pad.position["y"] + R_pad.image.get_height() >= field.bottom:
            R_pad.position["y"] = field.bottom - R_pad.image.get_height()
        


# Initialize Pygame
pygame.init()

# Set up the screen
bounds = Boundary()
screen = pygame.display.set_mode((bounds.width, bounds.height))

# Set up colors
Color = namedtuple("Color", ("x", "y", "z"))
dark_blue = (0, 0, 145)

# Create paddles and ball
L_pad = Paddle([0, bounds.height / 2], [0, 0])
R_pad = Paddle([bounds.width - Paddle.image.get_width(), bounds.height / 2], [0, 0])
ball = Ball([bounds.width / 2, bounds.height / 2], [2, 2])

# Scale images
L_pad.scale_image(0.5)
R_pad.scale_image(0.5)
ball.scale_image(0.5)

# Main game loop
done = False

while not done:
    # Inside the main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done = False

    # Game logic
    screen.fill(dark_blue)

    # Load and display the scaled images
    L_pad.load(Paddle.image,screen)
    R_pad.load(Paddle.image,screen)
    ball.load(Ball.image,screen)
    
    #move pallets
    keys = pygame.key.get_pressed()

    # Player 2 controls
    if keys[pygame.K_UP]:
        R_pad.position["y"] -= 3
    elif keys[pygame.K_DOWN]:
        R_pad.position["y"] += 3

    # Player 1 controls
    if keys[pygame.K_z]:
        L_pad.position["y"] -= 3
    elif keys[pygame.K_s]:
        L_pad.position["y"] += 3

    Collision.collide_with(L_pad,R_pad,ball)

    # Move the ball
    ball.position["x"] += ball.dir_vect["x"]
    ball.position["y"] += ball.dir_vect["y"]
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
