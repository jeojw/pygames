import pygame
import System
import HitBox

'''
아이템을 생성시켜주는 클래스
'''

IconDic = {'ATK': pygame.image.load('ShootingGame/ItemIcon/ATK_item.png'),
           'HP': None}

class Supply(System.System):
    def __init__(self, Type, x_pos, y_pos):
        super().__init__()
        self.type = Type # 아이템 타입
        self.icon = IconDic[Type] # 아이템 아이콘
        self.pos = pygame.math.Vector2(x_pos, y_pos)
        self.VEL = pygame.math.Vector2(0, 5) # 속도
        self.HitBox = HitBox.HitBox(self.icon, x_pos, y_pos)
        
    def GetType(self):
        '''
        타입을 리턴해주는 메서드
        '''
        return self.type
        
    def Draw(self):
        self.GAMESCREEN.blit(self.icon, (self.pos.x, self.pos.y))
    
    def Update(self):
        self.pos += self.VEL
        
        self.HitBox.UpdatePos(self.pos.x, self.pos.y)