import pygame
import EnemyAirCraft
import Queue
import HitBox
import Bullet
import math
import Queue
import time

Boss = pygame.image.load('ShootingGame/Sprite/Boss/Boss_Sprite.png')
BossLaser = [pygame.image.load('ShootingGame/Sprite/Boss/Boss_Laser_' + str(i) + '.png') for i in range(1, 8)]
BossSpinBullet = [pygame.image.load('ShootingGame/Sprite/Boss/Boss_Spin_' + str(i) + '.png') for i in range(1, 6)]
laser = pygame.image.load('ShootingGame/Sprite/Bullet/laser.png')
BossSprite = pygame.transform.scale(Boss, (600, 450))
LaserSprite = pygame.transform.scale(laser, (30, 500))

class BossAirCraft(EnemyAirCraft.EnemyAirCraft):
    def __init__(self, MAXHP, ATK, DEF, y_pos):
        self.initx = 50
        super().__init__(MAXHP, ATK, DEF, self.initx, y_pos)
        self.SpinPos = pygame.math.Vector2(self.pos.x + 300, self.pos.y + 105)
        self.movevariable = 0

        self.isExist = False
        self.isChangeCondition = False
        self.ChangePattern = False
        
        self.isNormal = False
        
        self.LaserSprite = []
        self.OpenLaser = False
        self.isLaser = False
        self.LCoolOff = False

        self.OpenSpin = False
        self.isSpin = False
        self.SpinQueue = Queue.Queue()
        self.SpinAngle = 0
        self.SCoolOff = False

        self.conindex = 0
        self.index = 0
        self.SpriteList = [[BossSprite], 
                           [pygame.transform.scale(sp, (600, 540)) for sp in BossLaser], 
                           [pygame.transform.scale(sp, (600, 450)) for sp in BossSpinBullet], 
                           []
                          ]
        self.spinbullet = pygame.image.load('ShootingGame/Sprite/Bullet/spinbullet.png')
        self.HitBox = HitBox.HitBox(BossSprite, self.pos.x, self.pos.y)
        self.SizeQueue.enqueue((self.HitBox.GetSize('w'), self.HitBox.GetSize('h')))

        self.CurPattern = 'SPINBULLET'
        self.NextPattern = None
        
        self.InitCool = 8 # 초기 쿨타임(조우시)
        self.InitStart = 0
        self.InitElapsed = 0
        
        self.PatternCool = 5
        self.CoolStart = 0
        self.CoolElapsed = 0
        
        self.LaserCool = 7
        self.LCStart = 0
        self.LCElapsed = 0
        
        self.SpinCool = 7
        self.SCStart = 0
        self.SCElapsed = 0
        
        self.LaserTime = 3.3
        self.LaserStart = 0
        self.LaserElapsed = 0
        
        self.NormalTime = 2
        self.NormalStart = 0
        self.NormalElapsed = 0
        
        self.PatternQueue = Queue.Queue()
        
        self.Changedelay = 0.5
        self.StartChange = 0
        self.ElapsedChange = 0
        
        self.current_time = 0
        self.animation_time = round(100 / len(self.SpriteList[self.conindex] * 100), 2)
        
        self.NormalDelay = 0.9
        self.StartNormal = 0
        self.ElapsedNormal = 0
        
        self.LaserDelay = 1
        self.StartLaser = 0
        self.ElapsedLaser = 0
        
        self.SpinDelay = 0.05
        self.StartSpin = 0
        self.ElapsedSpin = 0
        
        self.BulletIntervalx = 120
        self.BulletIntervaly = 50
        
    def SetBullets(self, Type):
        if (Type == 'NORMAL'):
            self.ProjectileList.append(Bullet.Bullet(self.bullet, self.HitBox.GetPos('x', True), self.HitBox.GetPos('y') + self.HitBox.GetSize('h'), self.ATK, 10, 180))
            self.ProjectileList.append(Bullet.Bullet(self.bullet, self.HitBox.GetPos('x', True) - self.BulletIntervalx, self.HitBox.GetPos('y') + self.HitBox.GetSize('h') - self.BulletIntervaly, self.ATK, 10, 180))
            self.ProjectileList.append(Bullet.Bullet(self.bullet, self.HitBox.GetPos('x', True) - self.BulletIntervalx * 2 , self.HitBox.GetPos('y') + self.HitBox.GetSize('h') - self.BulletIntervaly * 1.5, self.ATK, 10, 180))
            self.ProjectileList.append(Bullet.Bullet(self.bullet, self.HitBox.GetPos('x', True) + self.BulletIntervalx, self.HitBox.GetPos('y') + self.HitBox.GetSize('h') - self.BulletIntervaly, self.ATK, 10, 180))
            self.ProjectileList.append(Bullet.Bullet(self.bullet, self.HitBox.GetPos('x', True) + self.BulletIntervalx * 2 , self.HitBox.GetPos('y') + self.HitBox.GetSize('h') - self.BulletIntervaly * 1.5, self.ATK, 10, 180))
        
        elif (Type == 'LASER'):
            self.LaserSprite = [Bullet.Bullet(pygame.transform.scale(laser, (27, 1000)), self.HitBox.GetPos('x', True) - 2, self.HitBox.GetPos('y') + self.HitBox.GetSize('h') + 36, self.ATK, 0, 180),
                                  Bullet.Bullet(pygame.transform.scale(laser, (20, 1000)), self.HitBox.GetPos('x', True) - 135, self.HitBox.GetPos('y') + self.HitBox.GetSize('h'), self.ATK, 0, 180),
                                  Bullet.Bullet(pygame.transform.scale(laser, (20, 1000)), self.HitBox.GetPos('x', True) + 135, self.HitBox.GetPos('y') + self.HitBox.GetSize('h'), self.ATK, 0, 180),
                                  Bullet.Bullet(pygame.transform.scale(laser, (20, 1000)), self.HitBox.GetPos('x', True) - 237, self.HitBox.GetPos('y') + self.HitBox.GetSize('h') - 31, self.ATK, 0, 180),
                                  Bullet.Bullet(pygame.transform.scale(laser, (20, 1000)), self.HitBox.GetPos('x', True) + 237, self.HitBox.GetPos('y') + self.HitBox.GetSize('h') - 31, self.ATK, 0, 180)]
        
        elif (Type == 'SPINBULLET'):
            if (self.isSpin):
                self.ProjectileList.append(Bullet.Bullet(self.spinbullet, self.SpinPos.x, self.SpinPos.y , self.ATK, 4,  self.SpinAngle * 12.5))
                self.isSpin = False
                self.StartSpin = pygame.time.get_ticks()
                    
            self.ElapsedSpin = (pygame.time.get_ticks() - self.StartSpin) / 1000
            if (self.ElapsedSpin > self.SpinDelay):
                self.isSpin = True
                self.SpinAngle += 1
                self.StartSpin = 0
                self.ElapsedSpin = 0
        
    def pattern_1(self):
        if (not self.OpenLaser):
            self.LaserStart = pygame.time.get_ticks()
            self.OpenLaser = True

        if (self.index == len(self.SpriteList[self.conindex]) - 1):
            if (self.isLaser):
                self.SetBullets('LASER')
                self.isLaser = False
                self.StartLaser = pygame.time.get_ticks()
            self.ElapsedLaser = (pygame.time.get_ticks() - self.StartLaser) / 1000
            if (self.ElapsedLaser > self.LaserDelay):
                self.isLaser = True
                self.ElapsedLaser = 0
                self.StartLaser = 0
                
            self.LaserElapsed = (pygame.time.get_ticks() - self.LaserStart) / 1000
            if (self.LaserElapsed != 0):
                self.LCStart = pygame.time.get_ticks()
            if (self.LaserElapsed >= self.LaserTime):
                self.LaserElapsed = 0
                self.LaserStart = 0
                self.isLaser = False
                self.CurPattern = 'LASEROFF'
            
    def pattern_2(self):
        if (not self.OpenSpin):
            self.OpenSpin = True

        if (self.index == len(self.SpriteList[self.conindex]) - 1):
            self.SetBullets('SPINBULLET')
                
            if (self.SpinAngle >= 100):
                self.SpinAngle = 0
                self.CurPattern = 'SPINOFF'
        
    def pattern_3(self):
        pass
    
    def PatternCycle(self):
        '''
        if (self.isDetect):
            self.InitStart = pygame.time.get_ticks()
            self.isDetect = False
            self.ChangePattern = False ## *** 추구 지켜봐야할 코드
        
        
        if (self.ChangePattern):
            if (self.NextPattern is not None):
                self.CurPattern = self.NextPattern
            self.CoolStart = pygame.time.get_ticks()
            self.ChangePattern = False
        '''

        if (self.CurPattern == 'NORMAL'):
            if (self.isNormal):
                self.isMove = True
                self.SetBullets('NORMAL')
                self.isNormal = False
                self.NormalStart = pygame.time.get_ticks()
            self.NormalElapsed = (pygame.time.get_ticks() - self.NormalStart) / 1000
            
            if (self.NormalElapsed > self.NormalDelay):
                self.isNormal = True
                self.NormalElapsed = 0
                self.NormalStart = 0
            self.UpdatePattern()
        
        elif (self.CurPattern == 'LASER'):
            self.pattern_1()

        elif (self.CurPattern == 'LASEROFF'):
            self.LaserSprite.clear()
            self.OpenLaser = False
            if (self.index == 0):
                self.CurPattern = 'NORMAL'
                self.UpdatePattern()
                
        elif (self.CurPattern == 'SPINBULLET'):
            self.pattern_2()

        elif (self.CurPattern == 'SPINOFF'):
            self.OpenSpin = False
            if (self.index == 0):
                self.CurPattern = 'NORMAL'
                self.UpdatePattern()
            
        elif (self.CurPattern == 'TBD'):
            pass
        
        if (self.CurPattern != 'LASER'):
            self.CoolUpdate('LASER')

        if (self.CurPattern != 'SPINBULLET'):
            self.CoolUpdate('SPINBULLET')

    def CoolUpdate(self, Type):
        if (Type == 'LASER'):
            self.LCElapsed = (pygame.time.get_ticks() - self.LCStart) / 1000
            if (self.LCElapsed >= self.LaserCool):
                self.LCElapsed = 0
                self.LCStart = 0
            if (self.LCElapsed == 0):
                self.LCoolOff = True

        elif (Type == 'SPINBULLET'):
            self.SCElapsed = (pygame.time.get_ticks() - self.SCStart) / 1000
            if (self.SCElapsed >= self.SpinCool):
                self.SCElapsed = 0
                self.SCStart = 0
            if (self.SCElapsed == 0):
                self.SCoolOff = True
    
    def UpdatePattern(self):
        '''
        self.InitElapsed = (pygame.time.get_ticks() - self.InitStart) / 1000
        if (self.InitElapsed != 0):
            return -1
            
        if (self.InitElapsed > self.InitCool):
            self.InitElapsed = 0
            self.InitStart = 0
        '''
        
        self.CoolElapsed = (pygame.time.get_ticks() - self.CoolStart) / 1000
        if (self.CoolElapsed > self.PatternCool):
            if (self.CurPattern == 'NORMAL'):
                if (not self.PatternQueue.isEmpty()):
                    self.NextPattern = self.PatternQueue.dequeue()
            self.ChangePattern = True
            self.CoolElapsed = 0
            self.CoolStart = 0

        if (self.LCoolOff):
            self.PatternQueue.enqueue('LASER')
            
        if (self.SCoolOff):
            self.PatternQueue.enqueue('SPINBULLET')

    def UpdateCycle(self):
        self.ElapsedChange = (pygame.time.get_ticks() - self.StartChange) / 1000
        if (self.ElapsedChange > self.Changedelay):
            self.isChangeCondition = False
            self.StartChange = 0
            self.ElapsedChange = 0
        
    def DrawPos(self):
        self.GAMESCREEN.blit(self.SpriteList[self.conindex][self.index], (self.pos.x, self.pos.y))
        
    def DrawStat(self):
        Length = 125
        convertCoefficient = Length / self.MAXHP
        if (not self.isDead and self.isExist):
            pygame.draw.rect(self.GAMESCREEN, self.COLORDIC['RED'], [self.HitBox.GetPos('x', True) - self.HitBox.GetSize('w'), self.HitBox.GetPos('y', True) + self.HitBox.GetSize('h') / 2,
                                                                 self.MAXHP * convertCoefficient, 10], 2)
            pygame.draw.rect(self.GAMESCREEN, self.COLORDIC['RED'], [self.HitBox.GetPos('x', True) - self.HitBox.GetSize('w'), self.HitBox.GetPos('y', True) + self.HitBox.GetSize('h') / 2,
                                                                 self.HP * convertCoefficient, 10])
    
    def UpdateCondition(self, Player):
        y_distance = abs(self.GetPos('y', True) - Player.GetPos('y', True))
        if (y_distance <= 600):
            self.isDetect = True
            
        if (self.HP <= 0):
            self.isDead = True
            self.HitBox.Collidable = False
            
        if (not self.isDead):
            self.StartExist = pygame.time.get_ticks()
            
        else:
            self.ElapsedExist = int((pygame.time.get_ticks() - self.StartExist) / 1000)
            if (self.ElapsedExist > self.ExistTime):
                self.removeable = True
        
    def UpdatePos(self):
        if (not self.isDetect):
            self.pos -= self.VEL * 1.5
        else:
            if (self.CurPattern == 'NORMAL'):
                self.movevariable += 0.05
                self.pos = self.EightMovement(self.movevariable)
                self.SpinPos.x = self.pos.x + 300
                self.SpinPos.y = self.pos.y + 105
            else:
                self.Static()
            
        self.HitBox.UpdatePos(self.pos.x, self.pos.y)
        
    def EightMovement(self, t):
        return pygame.math.Vector2(math.sin(4 * t) * 40 + self.initx, math.sin(8 * t) * 5)
        
    def UpdateSprite(self, dt):
        self.current_time += dt
        
        if (self.CurPattern == 'NORMAL'):
            self.conindex = 0
            self.UpdateCycle()
        elif (self.CurPattern == 'LASER' or 
              self.CurPattern == 'LASEROFF'):
            self.conindex = 1
            self.UpdateCycle()
        elif (self.CurPattern == 'SPINBULLET'):
            self.conindex = 2
            self.UpdateCycle()
        elif (self.isDead):
            self.conindex = 3
            self.UpdateCycle()

        if (self.current_time >= self.animation_time):
            self.current_time = 0

            if (self.CurPattern == 'LASER'):
                self.index += 1
                if (self.index >= len(self.SpriteList[self.conindex])):
                    self.index = len(self.SpriteList[self.conindex]) - 1

            elif (self.CurPattern == 'LASEROFF'):
                self.index -= 1
                if (self.index <= 0):
                    self.index = 0
                    
            elif (self.CurPattern == 'SPINBULLET'):
                self.index += 1
                if (self.index >= len(self.SpriteList[self.conindex])):
                    self.index = len(self.SpriteList[self.conindex]) - 1
                    
            elif (self.CurPattern == 'SPINOFF'):
                self.index -= 1
                if (self.index <= 0):
                    self.index = 0

            else:
                self.index += 1
                if (self.index >= len(self.SpriteList[self.conindex])):
                    self.index = 0
        
    def Update(self, Player, dt):
        
        self.PatternCycle()
        
        self.UpdateStat(Player)
        self.UpdateCondition(Player)
        self.UpdatePos()
        self.UpdateSprite(dt)