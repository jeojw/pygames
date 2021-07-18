import pygame
import AirCraft
import HitBox
import Bullet

samplesprite = pygame.image.load('ShootingGame/Sprite/AIRCRAFT_SAMPLE.png')
explode = pygame.image.load('ShootingGame/Sprite/explode_effect.png')
bulletsprite = pygame.image.load('ShootingGame/Sprite/Bullet/Enemy_Bullet.png')
flipsample = pygame.transform.flip(samplesprite, False, True)

class EnemyAirCraft(AirCraft.AirCraft):
    def __init__(self, MAXHP, ATK, DEF, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.MAXHP = MAXHP
        self.HP = MAXHP
        self.ATK = ATK
        self.DEF = DEF
        self.VEL = pygame.math.Vector2(0, -6)
        
        self.isDetect = False
        self.removeable = False
        
        self.index = 0
        self.SpriteList = [flipsample, explode]
        self.HitBox = HitBox.HitBox(self.SpriteList[self.index], self.pos.x, self.pos.y)
        self.SizeQueue.enqueue((self.HitBox.GetSize('w'), self.HitBox.GetSize('h')))
        
        self.ChangeConditionTime = 2
        self.StartTime = 0
        self.ElapsedTime = 0
        
        self.ExistTime = 0.2
        self.StartExist = pygame.time.get_ticks()
        self.ElapsedExist = 0
        
        self.BulletInterval = 7
        self.BulletAngle = 10
        self.AtkCool = 1
        self.StartCool = 0
        self.ElapsedCool = 0

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
        self.ProjectileList.append(Bullet.Bullet(bulletsprite, self.HitBox.GetPos('x', True) - self.BulletInterval, self.HitBox.GetPos('y'), self.ATK, 180))
        self.ProjectileList.append(Bullet.Bullet(bulletsprite, self.HitBox.GetPos('x', True) + self.BulletInterval, self.HitBox.GetPos('y'), self.ATK, 180))
        
    def DrawStat(self):
        Length = 125
        convertCoefficient = Length / self.MAXHP
        if (not self.isDead):
            pygame.draw.rect(self.GAMESCREEN, self.COLORDIC['RED'], [self.HitBox.GetPos('x', True) - self.HitBox.GetSize('w'), self.HitBox.GetPos('y', True) + self.HitBox.GetSize('h') / 2,
                                                                 self.MAXHP * convertCoefficient, 10], 2)
            pygame.draw.rect(self.GAMESCREEN, self.COLORDIC['RED'], [self.HitBox.GetPos('x', True) - self.HitBox.GetSize('w'), self.HitBox.GetPos('y', True) + self.HitBox.GetSize('h') / 2,
                                                                 self.HP * convertCoefficient, 10])
        
    def UpdateStat(self, Player):
        for bullet in Player.ProjectileList:
            if (self.HitBox.CheckCollision(bullet.HitBox)):
                self.HP -= (bullet.ATK - self.DEF)
    
    def UpdateCondition(self):
        if (self.isAttack and not self.isDead and self.isDetect):
            self.SetBullets()
            self.isAttack = False
            self.StartCool = pygame.time.get_ticks()
        self.ElapsedCool = (pygame.time.get_ticks() - self.StartCool) / 1000
        
        if (self.ElapsedCool > self.AtkCool):
            self.isAttack = True
            self.ElapsedCool = 0
            self.StartCool = 0
            
        if (not self.isDead):
            self.StartExist = pygame.time.get_ticks()
            
        if (self.HP <= 0):
            self.isDead = True
            self.HitBox.Collidable = False
            
        if (self.isDead):
            self.ElapsedExist = int((pygame.time.get_ticks() - self.StartExist) / 1000)
            if (self.ElapsedExist > self.ExistTime):
                self.removeable = True
        
    def UpdatePos(self, Player):
        super().UpdatePos()
        
        y_distance = abs(self.GetPos('y', True) - Player.GetPos('y', True))
        if (self.pos.x < 0):
            self.pos.x = 0
        elif (self.pos.x + self.HitBox.GetSize('w') > self.LIMITSIZE.x):
            self.pos.x = self.LIMITSIZE.x - self.HitBox.GetSize('w')
            
        if (y_distance > 600 and not self.isDetect):
            self.pos -= self.VEL * 1.5
        else:
            self.isDetect = True
            self.Static()
            
        self.HitBox.UpdatePos(self.pos.x, self.pos.y)
        
    def UpdateSprite(self):
        if (self.isDead):
            self.index = len(self.SpriteList) - 1
            
        self.HitBox.UpdateSize(self.SpriteList[self.index])
    
    def Draw(self):
        self.DrawPos()
        self.DrawStat()
        
    def Update(self, Player):
        self.UpdateStat(Player)
        self.UpdateCondition()
        self.UpdatePos(Player)
        self.UpdateSprite()