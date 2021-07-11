import pygame
import HitBox
import System

class Bullet(System.System):
    def __init__(self, Sprite, x_pos, y_pos, ATK, angle=None):
        super().__init__()
        self.sprite = Sprite
        self.pos = pygame.math.Vector2(x_pos, y_pos)
        self.angle = angle
        if (self.angle is not None):
            self.sprite = pygame.transform.rotate(self.sprite, self.angle)
            self.HitBox = HitBox.HitBox(self.sprite, x_pos, y_pos)
        else:
            self.HitBox = HitBox.HitBox(self.sprite, x_pos, y_pos)
        self.VEL = pygame.math.Vector2(0, 10)
        
        self.ATK = ATK
        
    def GetPos(self, t):
        try:
            if (t == 'x'):
                return self.pos.x
            elif (t == 'y'):
                return self.pos.y
            else:
                raise ValueError
        except ValueError:
            return -1
    
    def Draw(self):
        self.GAMESCREEN.blit(self.sprite, (self.pos.x, self.pos.y))

    def Update(self):
        self.pos -= self.VEL
        self.HitBox.Update(self.pos.x, self.pos.y)