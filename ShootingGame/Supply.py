import pygame
import System
import HitBox

IconDic = {'ATK': pygame.image.load('ShootingGame/ItemIcon/ATK_item.png'),
           'HP': None}

class Supply(System.System):
    def __init__(self, Type, x_pos, y_pos):
        super().__init__()
        self.type = Type
        self.icon = IconDic[Type]
        self.pos = pygame.math.Vector2(x_pos, y_pos)
        self.VEL = pygame.math.Vector2(0, 5)
        self.HitBox = HitBox.HitBox(self.icon, x_pos, y_pos)
        
    def GetType(self):
        return self.type
        
    def Draw(self):
        self.GAMESCREEN.blit(self.icon, (self.pos.x, self.pos.y))
    
    def Update(self):
        self.pos += self.VEL
        
        self.HitBox.UpdatePos(self.pos.x, self.pos.y)