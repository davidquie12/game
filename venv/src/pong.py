import pygame
from collections import namedtuple
from random import randint, uniform
import math

class Unit:
    def __init__(self,pos : pygame.Vector2,dir_vec : pygame.Vector2,color,speed,
                 width = None ,height = None,radius = None):
        self.pos = pos
        self.width = width
        self.height = height
        self.radius = radius
        self.color = color
        self.speed = speed
        self.dir_vec = dir_vec
        
    def draw(self,screen : pygame.surface):
        pass
    
    def update(self):
        pass
    
        

    
class Paddle(Unit):
    
    def __init__(self,pos : pygame.Vector2,dir_vec : pygame.Vector2,color,speed):
        super().__init__(pos,dir_vec,color,speed)
        self.game = game 
        self.pos = pos 
        self.dir_vec = dir_vec
        self.color = color
        self.speed = speed
        self.height = 80
        self.width = 30
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        self.is_moving = False

    def draw(self, screen : pygame.surface):
        pygame.draw.rect(screen,self.color,self.rect)
        
    def update(self):
        self.rect.y += self.dir_vec.y
        
        # Check and adjust if the paddle hits the screen boundaries
        if self.rect.top <= 0:
            self.rect.y = 0
        elif self.rect.bottom >= screen.get_height():
            self.rect.y = screen.get_height() - self.height
        
class Ball(Unit):
    

    def __init__(self,center : pygame.Vector2,radius : int ,dir_vec : pygame.Vector2,color,speed = 4):
        super().__init__(center,dir_vec,color,speed) 
        self.dir_vec = dir_vec
        self.color = color
        self.speed = speed
        self.center = center
        self.radius = radius

    def check_collision_with_left_paddle(self, L_pad: Paddle):
        if (
            self.dir_vec.x < 0  # Check if the ball is moving left
            and L_pad.rect.colliderect(pygame.Rect(self.center.x - self.radius, self.center.y - self.radius, self.radius * 2, self.radius * 2))  # Check for collision
        ):
            self.dir_vec.x *= -1  

            # Check for top/bottom collision
            if self.center.y - self.radius <= L_pad.rect.top or self.center.y + self.radius >= L_pad.rect.bottom:
                self.dir_vec.y *= -1  
                if L_pad.is_moving:
                    self.speed = 10
                else:
                    self.speed = 4

            

    def check_collision_with_right_paddle(self, R_pad: Paddle):
        if (
            self.dir_vec.x > 0  # Check if the ball is moving right
            and R_pad.rect.colliderect(pygame.Rect(self.center.x - self.radius, self.center.y - self.radius, self.radius * 2, self.radius * 2))  # Check for collision
        ):
            self.dir_vec.x *= -1  

            # Check for top/bottom collision
            if self.center.y - self.radius <= R_pad.rect.top or self.center.y + self.radius >= R_pad.rect.bottom:
                self.dir_vec.y *= -1  
                if L_pad.is_moving:
                    self.speed = 10
                else:
                    self.speed = 4
                


        
    def draw(self,screen : pygame.surface):
        pygame.draw.circle(screen,self.color,self.center,self.radius)
        
    def update(self):
        self.pos.x += (self.dir_vec.x * self.speed)
        self.pos.y += (self.dir_vec.y * self.speed)
        
        
class Collision:      
    @staticmethod
    def collide_with_boundary(ball: Ball):
        
        if ball.center.x - ball.radius <= 0 or \
            ball.center.x + ball.radius >= screen.get_width():
                ball.dir_vec.x *= -1
                
        if ball.center.y - ball.radius <= 0 or \
            ball.center.y + ball.radius >= screen.get_height():
                ball.dir_vec.y *= -1
                
        



# Initialize Pygame
game = pygame.init()

# Set up the screen

screen = pygame.display.set_mode((640, 640))

# Set up colors
Color = namedtuple("Color", ("x", "y", "z"))
dark_blue = (0, 0, 145)
white = (0,0,0)

# create random generator
# Generate random angles between 0 and 2 * pi
random_angle = uniform(0, 2 * math.pi)

# Calculate the x and y components of the unit vector using trigonometry
dir_x = math.cos(random_angle) 
dir_y = math.sin(random_angle) 

# random start pos
c_x = randint(30,600) 
c_y = randint(30,600) 

center = pygame.Vector2(c_x,c_y)

L_pad_pos = pygame.Vector2(0,screen.get_height() / 2)
dir_vec_L = pygame.Vector2(0,0)

R_pad_pos = pygame.Vector2(screen.get_width() - 30 ,screen.get_height() / 2)
dir_vec_R = pygame.Vector2(0,0)

ball_dir = pygame.Vector2(dir_x,dir_y)

# Create paddles and ball
L_pad = Paddle(L_pad_pos,dir_vec_L,white,3)
R_pad = Paddle(R_pad_pos,dir_vec_R,white,3)
ball = Ball(center,10,ball_dir,white)

units = [L_pad,R_pad,ball]

# Main game loop
done = False

while not done:
    # Inside the main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done = True


    # move paddles
    keys = pygame.key.get_pressed()

    # Player 2 controls
    if keys[pygame.K_UP]:
        R_pad.dir_vec.y -= 1
        R_pad.is_moving =  True
    elif keys[pygame.K_DOWN]:
        R_pad.dir_vec.y += 1
        R_pad.is_moving =  True
        
    else:
        R_pad.dir_vec.y = 0
        R_pad.is_moving =  False
        

    # Player 1 controls
    if keys[pygame.K_z]:
        L_pad.dir_vec.y -= 1
        L_pad.is_moving = True
    elif keys[pygame.K_s]:
        L_pad.dir_vec.y += 1
        L_pad.is_moving = True
        
    else:
        L_pad.dir_vec.y = 0
        
        L_pad.is_moving = False



    # Game logic
    screen.fill(dark_blue)


    # update
   
    Collision.collide_with_boundary(ball)
    # Check collision with paddles
    ball.check_collision_with_left_paddle(L_pad)
    ball.check_collision_with_right_paddle(R_pad)


    # draw
    for unit in units:
        unit.update()
        unit.draw(screen)
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
