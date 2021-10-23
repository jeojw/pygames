import pygame
import AirCraft
import HitBox
import Bullet
import math
import time

tmpsprite = pygame.image.load('ShootingGame/Sprite/Enemy/Enemy_Normal.png')
samplesprite = pygame.transform.scale(tmpsprite, (90, 45))
explode = pygame.image.load('ShootingGame/Sprite/explode_effect.png')

class EnemyAirCraft(AirCraft.AirCraft):
    def __init__(self, MAXHP, ATK, DEF, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.MAXHP = MAXHP
        self.HP = MAXHP
        self.ATK = ATK
        self.DEF = DEF
        self.DEF = DEF
        self.VEL = pygame.math.Vector2(0, -6)
        self.initpos = pygame.math.Vector2(x_pos, y_pos) #최초 생성 좌표 후에 movement함수에서 y축 위치 조정용으로 쓰일 예정
        self.moveposy = 600
        self.movesec = 0
        
        self.bullet = pygame.image.load('ShootingGame/Sprite/Bullet/Enemy_Bullet.png')
        
        self.isDetect = False
        self.removeable = False
        
        self.index = 0
        self.SpriteList = [samplesprite, explode]
        self.HitBox = HitBox.HitBox(self.SpriteList[self.index], self.pos.x, self.pos.y)
        self.SizeQueue.enqueue((self.HitBox.GetSize('w'), self.HitBox.GetSize('h')))
        
        self.ChangeConditionTime = 2
        self.StartTime = 0
        self.ElapsedTime = 0
        
        self.ExistTime = 0.2
        self.StartExist = pygame.time.get_ticks()
        self.ElapsedExist = 0

    def GetPos(self, t, center=None):
        try:
            if (t == 'x'):
                if (center is not None):
                    return self.HitBox.GetPos('x', center)
                else:
                    return self.pos.x
            elif (t == 'y'):
                 if (center is not None):
                    return self.HitBox.GetPos('y', center)
                 else:
                    return self.pos.y
            else:
                raise ValueError
        except ValueError:
            return -1
        
    def GetSize(self, t):
        try:
            if (t == 'w'):
                return self.HitBox.GetSize('w')
            elif (t == 'h'):
                return self.HitBox.GetSize('h')
            else:
                raise ValueError
        except ValueError:
            return -1
        
    def SetBullets(self):
        pass
        
    def DrawStat(self):
        Length = 125
        convertCoefficient = Length / self.MAXHP
        if (not self.isDead):
            pygame.draw.rect(self.GAMESCREEN, self.COLORDIC['RED'], [self.HitBox.GetPos('x', True) - Length / 2, self.HitBox.GetPos('y', True) + self.HitBox.GetSize('h') * 0.75,
                                                                 self.MAXHP * convertCoefficient, 7], 2)
            pygame.draw.rect(self.GAMESCREEN, self.COLORDIC['RED'], [self.HitBox.GetPos('x', True) - Length / 2, self.HitBox.GetPos('y', True) + self.HitBox.GetSize('h') * 0.75,
                                                                 self.HP * convertCoefficient, 7])
        
    def Movement(self, t):
        '''
        적기의 움직임을 반환하는 메서드
        '''
        pass
        
    def UpdateStat(self, Player):
        '''
        스텟 업데이트 메서드
        여기에서는 피격시 hp감소만 구현
        '''
        for bullet in Player.ProjectileList:
            if (self.isGetAttack):
                self.HP -= (bullet.ATK - self.DEF)
                self.NotGetAttack()
    
    def UpdateCondition(self):
        '''
        적기의
        '''
        if (self.pos.y >= 200):
            self.isDetect = True
            self.initpos.y = 200
            
        if (not self.isDead):
            self.StartExist = pygame.time.get_ticks()
            
        if (self.HP <= 0):
            self.isDead = True
            self.HitBox.Collidable = False
            
        if (self.isDead):
            self.ElapsedExist = int((pygame.time.get_ticks() - self.StartExist) / 1000)
            if (self.ElapsedExist > self.ExistTime):
                self.removeable = True
        
    def UpdatePos(self):
        super().UpdatePos()
        
        if (self.pos.x < 0):
            self.pos.x = 0
        elif (self.pos.x + self.HitBox.GetSize('w') > self.LIMITSIZE.x):
            self.pos.x = self.LIMITSIZE.x - self.HitBox.GetSize('w')
        
    def UpdateSprite(self):
        if (self.isDead):
            self.index = len(self.SpriteList) - 1
            
        self.CurSprite = self.SpriteList[self.index]
        
        self.HitBox.UpdateSize(self.CurSprite)
    
    def Draw(self):
        self.DrawPos()
        self.DrawStat()
        
    def Update(self, Player):
        self.UpdateStat(Player)
        self.UpdateCondition()
        self.UpdatePos()
        self.UpdateSprite()
        
        
#-----------------------------------------------------------------------------------------------


class NormalEnemy(EnemyAirCraft):
    def __init__(self, MAXHP, ATK, DEF, x_pos, y_pos):
        super().__init__(MAXHP, ATK, DEF, x_pos, y_pos)
        self.SpriteList = [samplesprite, explode]
        
        self.AtkCool = 0.5
        self.StartCool = 0
        self.ElapsedCool = 0
        
    def SetBullets(self):
        self.ProjectileList.append(Bullet.Bullet(self.bullet, self.HitBox.GetPos('x', True) + 35, self.HitBox.GetPos('y') + self.HitBox.GetSize('h'), self.ATK, 10, 180))
        self.ProjectileList.append(Bullet.Bullet(self.bullet, self.HitBox.GetPos('x', True) - 30, self.HitBox.GetPos('y') + self.HitBox.GetSize('h'), self.ATK, 10, 180))
        
    def Movement(self, t):
        if (t >= 0 and t < math.pi):
            return pygame.math.Vector2(math.sin(t) * 240 + self.initpos.x, math.cos(t) * 10 + self.initpos.y)
        elif (t >= math.pi and t <= 2 * math.pi):
            return pygame.math.Vector2(math.sin(t) * 10 + self.initpos.x, math.cos(t) * 10 + self.initpos.y)
        
    def UpdatePos(self):
        super().UpdatePos()
        self.movesec += 0.1
        if (self.movesec >= 2 * math.pi):
            self.movesec = 0
        
        if (not self.isDetect):
            self.pos -= self.VEL * 1.5
        else:
            self.pos = self.Movement(self.movesec)
            
        self.HitBox.UpdatePos(self.pos.x, self.pos.y)
    
    def UpdateCondition(self):
        super().UpdateCondition()
        
        if (self.isAttack and not self.isDead and self.isDetect):
            self.SetBullets()
            self.atkcount += 1
            self.isAttack = False
            self.StartCool = pygame.time.get_ticks()
        self.ElapsedCool = (pygame.time.get_ticks() - self.StartCool) / 1000
        
        if (self.ElapsedCool > self.AtkCool):
            self.isAttack = True
            self.ElapsedCool = 0
            self.StartCool = 0
            
            
#-----------------------------------------------------------------------------------------------

            
tmplist = [pygame.image.load('ShootingGame/Sprite/Enemy/Enemy_Missile.png'),
           pygame.image.load('ShootingGame/Sprite/Enemy/Enemy_MissileOff.png')]
spritelist = [pygame.transform.scale(s, (90, 45)) for s in tmplist]

class MissileEnemy(EnemyAirCraft):
    def __init__(self, MAXHP, ATK, DEF, x_pos, y_pos):
        super().__init__(MAXHP, ATK, DEF, x_pos, y_pos)
        self.SpriteList = spritelist + [explode]
        
        self.MissileReady = True
        self.MissileShoot = False
        self.MissileOff = False
        self.missilemove = 0
        self.missilecount = 0
        self.missile = pygame.image.load('ShootingGame/Sprite/Bullet/Missile.png')
        
        self.AtkCool = 1
        self.StartCool = 0
        self.ElapsedCool = 0
        
    def SetMissile(self):
        if (self.missilecount < 2):
            for i in range(-1, 2, 2):
                self.ProjectileList.append(Bullet.Bullet(self.missile, self.HitBox.GetPos('x', True) + 30 * i, self.HitBox.GetPos('y') + self.HitBox.GetSize('h'), self.ATK * 2, self.MissileMovement(self.missilemove), 180))
            self.missilecount += 2
        
        else:
            self.MissileShoot = True
            self.MissileReady = False
    
    def SetBullets(self):
        self.ProjectileList.append(Bullet.Bullet(self.bullet, self.HitBox.GetPos('x', True), self.HitBox.GetPos('y') + self.HitBox.GetSize('h'), self.ATK, 10, 180))
        
    def MissileMovement(self, t):
        if (t <= 14 and t >= 0):
            return math.pow(t, 0.8) * -1
        elif (t > 14):
            return math.pow((t - 12), 1.9) * -1
        
    def Movement(self, t):
        if (t >= 0 and t < math.pi):
            return pygame.math.Vector2(math.sin(t) * 240 + self.initpos.x, math.cos(t) * 10 + self.initpos.y)
        elif (t >= math.pi and t <= 2 * math.pi):
            return pygame.math.Vector2(math.sin(t) * 10 + self.initpos.x, math.cos(t) * 10 + self.initpos.y)
        
    def UpdatePos(self):
        super().UpdatePos()
        if (not self.isDead):
            self.movesec += 0.1
            if (self.movesec >= 2 * math.pi):
                self.movesec = 0
        
            if (not self.isDead):
                if (not self.isDetect):
                    self.pos -= self.VEL * 1.5
                else:
                    if (self.MissileReady):
                        self.Static()
                    else:
                        self.Static()
                        #self.pos = self.Movement(self.movesec)
            
                self.HitBox.UpdatePos(self.pos.x, self.pos.y)
        
    def UpdateCondition(self):
        super().UpdateCondition()
        
        if (self.MissileReady and self.isDetect):
            self.SetMissile()
        elif (not self.MissileReady and self.MissileShoot):
            self.missilemove += 1
            for i in range(len(self.ProjectileList)):
                self.ProjectileList[i].VEL.y = self.MissileMovement(self.missilemove)
            
            if (len(self.ProjectileList) == 0):
                self.MissileOff = True
                self.MissileShoot = False
        
        if (self.MissileOff and not self.MissileShoot):
            if (self.isAttack and not self.isDead and self.isDetect):
                self.SetBullets()
                self.isAttack = False
                self.StartCool = pygame.time.get_ticks()
            self.ElapsedCool = (pygame.time.get_ticks() - self.StartCool) / 1000
        
            if (self.ElapsedCool > self.AtkCool):
                self.isAttack = True
                self.ElapsedCool = 0
                self.StartCool = 0
                
    
    def UpdateSprite(self):
        if (self.MissileShoot):
            self.index = 1
            
        super().UpdateSprite()

    def Update(self, Player):
        super().Update(Player)