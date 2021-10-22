import pygame
import HitBox
import System

'''
오브젝트들이 발사하는 탄환을 설정해주는 클래스
'''
'''
탄환 충돌 시 이펙트가 출력되는 효과를 제대로 구현해 볼것 -> 일단 Bullet 클래스 내에서 구현해볼 예정
'''

effect = pygame.image.load('ShootingGame/Sprite/Bullet/CollideEffect.png')


class Bullet(System.System):
    def __init__(self, Sprite, x_pos, y_pos, ATK, SPEED ,angle=None):
        super().__init__()
        self.sprite = Sprite # 탄환
        self.Type = 'NORMAL'
        self.Object = None
        self.EffectDic = {'NORMAL': pygame.transform.scale(effect, (20,10)),
                          'MISSILE': pygame.image.load('ShootingGame/Sprite/Bullet/CollideEffect.png'),
                          'LASER': pygame.image.load('ShootingGame/Sprite/Bullet/CollideEffect.png')}
        self.isExist = True
        self.Collide = False
        self.pos = pygame.math.Vector2(x_pos, y_pos) # 위치
        self.angle = angle # 탄환 발사 각도
        self.VEL = pygame.math.Vector2(0, SPEED)
        if (self.angle is not None): # 만일 angle값이 None이 아닐 경우 스프라이트 회전 및 속도벡터를 회전시킴
            self.sprite = pygame.transform.rotate(self.sprite, self.angle)
            self.VEL = self.VEL.rotate(-self.angle)
        self.pos.x -= self.sprite.get_width() / 2 # 위치조정
        self.HitBox = HitBox.HitBox(self.sprite, self.pos.x, self.pos.y)
        self.ATK = ATK # 공격력 설정
        
        self.ExistTime = 0.1
        self.StartExist = 0
        self.ElapsedExist = 0
        
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
        
    def IsCollide(self, Obj):
        self.Collide = True
        self.Object = Obj
    
    def Draw(self):
        self.GAMESCREEN.blit(self.sprite, (self.pos.x, self.pos.y))
        
    def DrawEffect(self):
        diffpos = pygame.math.Vector2(abs(self.EffectDic[self.Type].get_width() - self.sprite.get_width()) / 2, abs(self.EffectDic[self.Type].get_height() - self.sprite.get_height()) / 2)
        
        if (self.Object.Type !='BOSS'):
            self.GAMESCREEN.blit(self.EffectDic[self.Type], (self.pos.x - diffpos.x, self.pos.y - diffpos.y))

        else:
            self.GAMESCREEN.blit(self.EffectDic[self.Type], (self.pos.x - diffpos.x, self.pos.y - diffpos.y))
    def Update(self):
        
        if (not self.Collide):
            self.pos -= self.VEL
            self.HitBox.UpdatePos(self.pos.x, self.pos.y)
        
        if (not self.Collide):
            self.StartExist = pygame.time.get_ticks()
        else:
            self.ElapsedExist = (pygame.time.get_ticks() - self.StartExist) / 1000
            if (self.ElapsedExist > self.ExistTime):
                self.isExist = False
