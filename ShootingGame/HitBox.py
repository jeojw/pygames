import System
import pygame

class HitBox(System.System):
    def __init__(self, Sprite, x_pos, y_pos):
        super().__init__()
        self.pos = pygame.math.Vector2(x_pos, y_pos)
        self.Object = Sprite.get_rect(topleft=(x_pos, y_pos))
        self.Collidable = True
        
    def Draw(self):
        pygame.draw.rect(self.GAMESCREEN, (255, 0, 0), [self.Object.x, self.Object.y, self.Object.width, self.Object.height], 2)
        
    def GetPos(self, t, center=None):
        try:
            if (t == 'x'):
                if (center is not None):
                    return self.Object.centerx
                else:
                    return self.pos.x
            elif (t == 'y'):
                 if (center is not None):
                    return self.Object.centery
                 else:
                    return self.pos.y
            else:
                raise ValueError
        except ValueError:
            return -1
    
    def GetSize(self, t):
        try:
            if (t == 'w'):
                return self.Object.width
            elif (t == 'h'):
                return self.Object.height
            else:
                raise ValueError
        except ValueError:
            return -1
        
    def CheckCollision(self, Another):
        if (self.Collidable):
            return pygame.Rect.colliderect(self.Object, Another.Object)
    
    def UpdateSize(self, newSprite):
        self.Object = newSprite.get_rect(topleft=(self.pos.x, self.pos.y))
    
    def UpdatePos(self, x_pos, y_pos):
        self.pos = pygame.math.Vector2(x_pos, y_pos)
        self.Object.topleft = (self.pos.x, self.pos.y)