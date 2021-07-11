import System
import pygame

class HitBox(System.System):
    def __init__(self, Sprite, x_pos, y_pos):
        super().__init__()
        self.HitBox = Sprite.get_rect(topleft=(x_pos, y_pos))
        self.Collidable = True
        
    def Draw(self):
        pygame.draw.rect(self.GAMESCREEN, (255, 0, 0), [self.HitBox.x, self.HitBox.y, self.HitBox.width, self.HitBox.height], 2)
        
    def GetPos(self, t, center=None):
        if (center is not None):
            try:
                if (t == 'x'):
                    return self.HitBox.centerx
                elif (t == 'y'):
                    return self.HitBox.centery
                else:
                    raise ValueError
            except ValueError:
                return -1
        try:
            if (t == 'x'):
                return self.HitBox.x
            elif (t == 'y'):
                return self.HitBox.y
            else:
                raise ValueError
        except ValueError:
            return -1
    
    def GetSize(self, t):
        try:
            if (t == 'w'):
                return self.HitBox.width
            elif (t == 'h'):
                return self.HitBox.height
            else:
                raise ValueError
        except ValueError:
            return -1
        
    def CheckCollision(self, Another):
        return pygame.Rect.colliderect(self.HitBox, Another.HitBox)
    
    def Update(self, x_pos, y_pos):
        self.HitBox.x = x_pos
        self.HitBox.y = y_pos