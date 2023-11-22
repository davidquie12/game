import pygame
from collections import namedtuple
from random import randint, uniform
import math
from pygwidgets import TextButton

window = pygame.Vector2(640,640)

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
        
    def draw(self):
        pass
    
    def update(self):
        pass
    
     
class Paddle(Unit):
    
    def __init__(self,pos : pygame.Vector2,dir_vec : pygame.Vector2,color,speed):
        super().__init__(pos,dir_vec,color,speed)
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
        elif self.rect.bottom >= window.x:
            self.rect.y = window.y - self.height
        
class Ball(Unit):
    

    def __init__(self,center : pygame.Vector2,radius : int ,dir_vec : pygame.Vector2,color,speed = 4):
        super().__init__(center,dir_vec,color,speed) 
        self.dir_vec = dir_vec
        self.color = color
        self.speed = speed
        self.center = center
        self.radius = radius

    def check_collision_with_left_paddle(self, L_pad: Paddle,smash):
        if (
            self.dir_vec.x < 0  # Check if the ball is moving left
            and L_pad.rect.colliderect(pygame.Rect(self.center.x - self.radius, self.center.y - self.radius, self.radius * 2, self.radius * 2))  # Check for collision
        ):
            if not smash:
                self.dir_vec.x *= -1  
            else:
                self.dir_vec.x *= (-1 * 5)

            # Check for top/bottom collision
            if self.center.y - self.radius <= L_pad.rect.top or self.center.y + self.radius >= L_pad.rect.bottom:
                self.dir_vec.y *= -1  
                if L_pad.is_moving:
                    self.speed = 10
                else:
                    self.speed = 4
        

        
    def check_collision_with_right_paddle(self, R_pad: Paddle, smash):
        if (
            self.dir_vec.x > 0  # Check if the ball is moving right
            and R_pad.rect.colliderect(pygame.Rect(self.center.x - self.radius, self.center.y - self.radius, self.radius * 2, self.radius * 2))  # Check for collision
        ):
            if not smash:
                self.dir_vec.x *= -1  
            else:
                self.dir_vec.x *= (-1 * 5)

            # Check for top/bottom collision
            if self.center.y - self.radius <= R_pad.rect.top or self.center.y + self.radius >= R_pad.rect.bottom:
                self.dir_vec.y *= -1  
                if R_pad.is_moving:
                    self.speed = 10
                else:
                    self.speed = 4
                
   
    def draw(self,window : pygame.surface):
        pygame.draw.circle(window,self.color,self.center,self.radius)
        
    def update(self):
        self.pos.x += (self.dir_vec.x * self.speed)
        self.pos.y += (self.dir_vec.y * self.speed)
        
class Collision:      
    @staticmethod
    def collide_with_boundary(ball: Ball):
        
        if ball.center.x - ball.radius <= 0 or \
            ball.center.x + ball.radius >= window.x:
                return True

                
        if ball.center.y - ball.radius <= 0 or \
            ball.center.y + ball.radius >= window.y:
                ball.dir_vec.y *= -1
                
        
                
                
class two_Play:
    def __init__(self, screen : pygame.Surface):
        self.screen = screen
        self.game_over = False
        self.smash : bool
        # Set up colors
        self.dark_blue = (0, 0, 145)
        self.white = (255, 255, 255)

        # Create random generator
        self.random_angle = uniform(0, 2 * math.pi)
        self.dir_x = math.cos(self.random_angle)
        self.dir_y = math.sin(self.random_angle)

        # Random start pos
        self.center = pygame.Vector2(randint(30, 600), randint(30, 600))

        self.L_pad_pos = pygame.Vector2(0, self.screen.get_height() / 2)
        self.dir_vec_L = pygame.Vector2(0, 0)

        self.R_pad_pos = pygame.Vector2(self.screen.get_width() - 30, self.screen.get_height() / 2)
        self.dir_vec_R = pygame.Vector2(0, 0)

        self.ball_dir = pygame.Vector2(self.dir_x, self.dir_y)

        # Create paddles and ball
        self.L_pad = Paddle(self.L_pad_pos, self.dir_vec_L, self.white, 3)
        self.R_pad = Paddle(self.R_pad_pos, self.dir_vec_R, self.white, 3)
        self.ball = Ball(self.center, 10, self.ball_dir, self.white)

        self.units = [self.L_pad, self.R_pad, self.ball]

    def update(self,screen):
        self.smash = False
        # Update game logic
        self.game_over = Collision.collide_with_boundary(self.ball)
        self.ball.check_collision_with_left_paddle(self.L_pad,self.smash)
        self.ball.check_collision_with_right_paddle(self.R_pad,self.smash)
        
        keys = pygame.key.get_pressed()

        #smash ball
        if keys[pygame.K_SPACE]:
            self.smash = True
        else:
            self.smash = False
        # Player 2 controls
        if keys[pygame.K_UP]:
            self.R_pad.dir_vec.y -= 1
            self.R_pad.is_moving = True
        elif keys[pygame.K_DOWN]:
            self.R_pad.dir_vec.y += 1
            self.R_pad.is_moving = True
        else:
            self.R_pad.dir_vec.y = 0
            self.R_pad.is_moving = False

        # Player 1 controls
        if keys[pygame.K_z]:
            self.L_pad.dir_vec.y -= 1
            self.L_pad.is_moving = True
        elif keys[pygame.K_s]:
            self.L_pad.dir_vec.y += 1
            self.L_pad.is_moving = True
        else:
            self.L_pad.dir_vec.y = 0
            self.L_pad.is_moving = False

        screen.fill(self.dark_blue)



        # Draw the game elements
        for unit in self.units:
            unit.update()
            unit.draw(self.screen)
            
    def process_event(self):
        if self.game_over:
            return True

        
class four_Play:
    def __init__(self, screen : pygame.Surface):
        self.smash : bool
        self.screen = screen
        self.game_over = False
        # Set up colors
        self.dark_blue = (0, 0, 145)
        self.white = (255, 255, 255)

        # Create random generator
        self.random_angle = uniform(0, 2 * math.pi)
        self.dir_x = math.cos(self.random_angle)
        self.dir_y = math.sin(self.random_angle)

        # Random start pos
        self.center = pygame.Vector2(randint(30, 600), randint(30, 600))

        self.L1_pad_pos = pygame.Vector2(0, self.screen.get_height() / 4)
        self.L2_pad_pos = pygame.Vector2(0, self.screen.get_height() / 0.5)
        
        self.dir_vec_L1 = pygame.Vector2(0, 0)
        self.dir_vec_L2 = pygame.Vector2(0, 0)
        

        self.R1_pad_pos = pygame.Vector2(self.screen.get_width() - 30, self.screen.get_height() / 4)
        self.R2_pad_pos = pygame.Vector2(self.screen.get_width() - 30, self.screen.get_height() / 0.5)
        
        self.dir_vec_R1 = pygame.Vector2(0, 0)
        self.dir_vec_R2 = pygame.Vector2(0, 0)
        

        self.ball_dir = pygame.Vector2(self.dir_x, self.dir_y)

        # Create paddles and ball
        self.L1_pad = Paddle(self.L1_pad_pos, self.dir_vec_L1, self.white, 3)
        self.L2_pad = Paddle(self.L2_pad_pos, self.dir_vec_L2, self.white, 3)
        
        self.R1_pad = Paddle(self.R1_pad_pos, self.dir_vec_R1, self.white, 3)
        self.R2_pad = Paddle(self.R2_pad_pos, self.dir_vec_R2, self.white, 3)
        
        self.ball = Ball(self.center, 10, self.ball_dir, self.white)

        self.units = [self.L1_pad,self.L2_pad, self.R1_pad,self.R2_pad, self.ball]

    def update(self,screen):
        
        # Update game logic
        self.game_over = Collision.collide_with_boundary(self.ball)
        
        self.smash = self.ball.check_collision_with_left_paddle(self.L1_pad,self.smash )
        self.smash = self.ball.check_collision_with_left_paddle(self.L2_pad,self.smash )
        
        self.smash = self.ball.check_collision_with_right_paddle(self.R1_pad,self.smash )
        self.smash = self.ball.check_collision_with_right_paddle(self.R2_pad,self.smash )
        
        keys = pygame.key.get_pressed()

        #smash ball
        if keys[pygame.K_SPACE]:
            self.smash = True
        else:
            self.smash = False
            
        # Player 2A controls
        if keys[pygame.K_UP]:
            self.R1_pad.dir_vec.y -= 1
            self.R1_pad.is_moving = True
        elif keys[pygame.K_DOWN]:
            self.R1_pad.dir_vec.y += 1
            self.R1_pad.is_moving = True
        else:
            self.R1_pad.dir_vec.y = 0
            self.R1_pad.is_moving = False
            
        # Player 2B controls
        if keys[pygame.K_o]:
            self.R2_pad.dir_vec.y -= 1
            self.R2_pad.is_moving = True
        elif keys[pygame.K_l]:
            self.R2_pad.dir_vec.y += 1
            self.R2_pad.is_moving = True
        else:
            self.R2_pad.dir_vec.y = 0
            self.R2_pad.is_moving = False

        # Player 1A controls
        if keys[pygame.K_z]:
            self.L1_pad.dir_vec.y -= 1
            self.L1_pad.is_moving = True
        elif keys[pygame.K_s]:
            self.L1_pad.dir_vec.y += 1
            self.L1_pad.is_moving = True
        else:
            self.L1_pad.dir_vec.y = 0
            self.L1_pad.is_moving = False
            
            # Player 1B controls
        if keys[pygame.K_r]:
            self.L2_pad.dir_vec.y -= 1
            self.L2_pad.is_moving = True
        elif keys[pygame.K_f]:
            self.L2_pad.dir_vec.y += 1
            self.L2_pad.is_moving = True
        else:
            self.L2_pad.dir_vec.y = 0
            self.L2_pad.is_moving = False

        screen.fill(self.dark_blue)
        

        # Draw the game elements
        for unit in self.units:
            unit.update()
            unit.draw(self.screen)
            
    def process_event(self):
        if self.game_over:
            return True
        


class State:
    def process_event(self, event):
        pass

    def update(self,screen : pygame.surface):
        pass

class PlayingState(State):
    def __init__(self,screen, players : int):
        self.should_exit = False
        self.next_state = None
        if players == 2:
            self.game =  two_Play(screen)
        elif players == 4:
            self.game = four_Play(screen)        
            
    def process_event(self, event):
        if self.game.process_event():
            self.next_state = GameOverState()
         

    def update(self,screen):
        # Update logica voor het speelscherm
        self.game.update(screen)

    # Voeg andere functionaliteiten toe die nodig zijn voor het speelscherm


class GameOverState(State):
    def __init__(self):
        self.should_exit = False
        self.next_state = None
        
        self.font = pygame.font.Font(None, 80)  # You can adjust the font size here
        self.game_over_text = self.font.render("Game Over", True, (255, 0, 0))  # Red color


    def process_event(self, event):
        # Verwerk gebeurtenissen voor het game over-scherm
        pass

    def update(self, screen):
        screen.fill((0, 0, 0))  # Fill the screen with black

        # Calculate the text position to center it
        text_rect = self.game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        # Blit the "Game Over" text onto the screen
        screen.blit(self.game_over_text, text_rect)

    # Voeg andere functionaliteiten toe die nodig zijn voor het game over-scherm

class MainMenuState(State):
    def __init__(self,screen):
        self.should_exit = False
        self.next_state = None
        self.screen = screen
        # Maak knoppen voor het hoofdmenu
        self.two_player = TextButton(window=screen,loc=(200,250), text='two_player' ,fontSize=50,textColor=(125,125,125))
        self.four_player = TextButton(window=screen,loc=(200,300), text='four_game ' ,fontSize=50,textColor=(125,125,125))
        self.exit_button = TextButton(window=screen,loc=(200,350), text='Exit game ', fontSize=50, textColor=(125,125,125))

    def process_event(self, event):
        # Verwerk gebeurtenissen voor het hoofdmenu

            
        if self.two_player.handleEvent(event):
            # Logica om het spel te starten
            self.next_state = PlayingState(self.screen,2)
            
        if self.four_player.handleEvent(event):
            # Logica om het spel te starten
            self.next_state = PlayingState(self.screen,4)
            
        elif self.exit_button.handleEvent(event):
            self.should_exit = True

    def update(self,screen):
        # Update logica voor het hoofdmenu
        screen.fill((0, 0, 0))  # Fill the screen with black
        # Draw the buttons onto the screen
        self.two_player.draw()
        self.four_player.draw()
        self.exit_button.draw()

    # Voeg andere functionaliteiten toe die nodig zijn voor het hoofdmenu

# De main methode
def main():
    pygame.init()
    screen = pygame.display.set_mode((640,640))
    pygame.display.set_caption("pong")
    game_state = MainMenuState(screen=screen)  # Begin met het hoofdmenu
    
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        game_state.process_event(event)
        game_state.update(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

        if game_state.should_exit:
            running = False

        if game_state.next_state:
            game_state = game_state.next_state

    pygame.quit()

if __name__ == "__main__":
    main()

                


