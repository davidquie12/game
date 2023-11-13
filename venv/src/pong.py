import pygame
import sys
from collections import namedtuple


class unit:
    
    def __init__(self,position,color,speed) -> None:
        self.position = {
            "x" : position,
            "color" : color,
            "speed" : speed     
        }

        
class paddle(unit): 
    width = 30
    height = 100
    speed = 1
    def __init__(self, position, color, speed) -> None:
        super().__init__(position, color, speed) 
        self.speed = speed
        
    def draw(self,rect,surface):
        pygame.draw.rect(surface=surface,color=self.position["color"],rect=rect)
          
        

class ball(unit):
    radius = 5.0
    start_pos = [0,0]
    speed = 0.5
    def __init__(self, position, color, speed) -> None:
        super().__init__(position, color, speed)
        self.speed = speed
        
    def draw(self,surface):
        pygame.draw.circle(surface=surface,color=self.position["color"],center=self.start_pos,radius=self.radius)


    