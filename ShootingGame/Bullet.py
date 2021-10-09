import pygame
import HitBox
import System

'''
오브젝트들이 발사하는 탄환을 설정해주는 클래스
'''

class Bullet(System.System):
    def __init__(self, Sprite, x_pos, y_pos, ATK, SPEED ,angle=None):
        super().__init__()
        self.sprite = Sprite # 탄환
        self.pos = pygame.math.Vector2(x_pos, y_pos) # 위치
        self.angle = angle # 탄환 발사 각도
        self.VEL = pygame.math.Vector2(0, SPEED)
        if (self.angle is not None): # 만일 angle값이 None이 아닐 경우 스프라이트 회전 및 속도벡터를 회전시킴
            self.sprite = pygame.transform.rotate(self.sprite, self.angle)
            self.VEL = self.VEL.rotate(-self.angle)
        self.pos.x -= self.sprite.get_width() / 2 # 위치조정
        self.HitBox = HitBox.HitBox(self.sprite, self.pos.x, self.pos.y)
        self.ATK = ATK # 공격력 설정
        
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
        self.HitBox.Draw()

    def Update(self):
        self.pos -= self.VEL
        self.HitBox.UpdatePos(self.pos.x, self.pos.y)