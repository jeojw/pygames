import pygame
import System
import HitBox

class Supply(System.System):
    def __init__(self, icon, x_pos, y_pos):
        super().__init__()
        self.icon = icon
        self.type = None
        self.HitBox = HitBox.HitBox(icon, x_pos, y_pos)
        
    def GetType(self):
        return self.type
        
    def Draw(self):
        self.GAMESCREEN.blit(self.icon, (self.HitBox.x, self.HitBox.y))
    
    def Update(self, x_pos, y_pos):
        self.HitBox.x = x_pos
        self.HitBox.y = y_pos