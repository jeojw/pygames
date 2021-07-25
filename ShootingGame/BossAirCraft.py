import pygame
import EnemyAirCraft
import Queue
import HitBox
import Bullet

Boss = pygame.image.load('ShootingGame/Sprite/Boss/Boss_Sprite.png')
BossLaser = [pygame.image.load('ShootingGame/Sprite/Boss/Boss_Laser_' + str(i) + '.png') for i in range(1, 7)]
BossSpinBullet = [pygame.image.load('ShootingGame/Sprite/Boss/Boss_Spin_' + str(i) + '.png') for i in range(1, 6)]
laser = pygame.image.load('ShootingGame/Sprite/Bullet/laser.png')
BossSprite = pygame.transform.scale(Boss, (600, 450))
LaserSprite = pygame.transform.scale(laser, (18, 240))

class BossAirCraft(EnemyAirCraft.EnemyAirCraft):
    def __init__(self, MAXHP, ATK, DEF, y_pos):
        super().__init__(MAXHP, ATK, DEF, 50, y_pos)
        
        self.isExist = False
        self.isChangeCondition = False
        self.AddPattern = False
        self.ChangePattern = False
        self.isLaser = False
        self.isPattern = False
        self.isNormal = False
        self.conindex = 0
        self.index = 0
        self.SpriteList = [[BossSprite], 
                           [pygame.transform.scale(sp, (600, 540)) for sp in BossLaser], 
                           [pygame.transform.scale(sp, (600, 450)) for sp in BossSpinBullet], 
                           []
                          ]
        self.HitBox = HitBox.HitBox(BossSprite, self.pos.x, self.pos.y)
        self.SizeQueue.enqueue((self.HitBox.GetSize('w'), self.HitBox.GetSize('h')))
        self.CurPattern = ('NORMAL', None)
        self.NextPattern = None
        
        self.PatternCool = 5
        self.CoolStart = 0
        self.CoolElapsed = 0
        
        self.LaserCool = 7
        self.LCStart = 0
        self.LCElapsed = 0
        
        self.SpinCool = 7
        self.SCStart = 0
        self.SCElapsed = 0
        
        self.LaserTime = 4
        self.LaserStart = 0
        self.LaserElapsed = 0
        
        self.NormalTime = 2
        self.NormalStart = 0
        self.NormalElapsed = 0
        
        self.SpinTime = 2
        self.SpinStart = 0
        self.SpinElapsed = 0
        
        self.PatternQueue = Queue.Queue()
        self.PatternQueue.enqueue(('LASER', self.pattern_1()))
        self.PatternQueue.enqueue(('LASER', self.pattern_1()))
        self.PatterList = [('NORMAL', None), 
                           ('LASER', self.pattern_1()), 
                           ('SPINBULLET', self.pattern_2()), 
                           ('TBD', self.pattern_3())
                          ]
        
        self.Changedelay = 0.5
        self.StartChange = 0
        self.ElapsedChange = 0
        
        self.current_time = 0
        self.animation_time = round(100 / len(self.SpriteList[self.conindex] * 100), 2)
        
    def SetBullets(self, Type):
        if (Type == 'NORMAL'):
            pass
        
        elif (Type == 'LASER'):
            pass
        
        elif (Type == 'SPINBULLET'):
            pass
        
    def pattern_1(self):
        if (self.CurPattern[0] != 'LASER'):
            self.isChangeCondition = True
            self.StartChange = pygame.time.get_ticks()
        
        self.isLaser = True
        if (self.index == len(self.SpriteList[1]) - 1):
            self.SetBullets('LASER')
            
    def pattern_2(self):
        pass
        
    def pattern_3(self):
        pass
    
    def PatternCycle(self):  
        if (self.ChangePattern):
            self.CurPattern = self.NextPattern
            self.CoolStart = pygame.time.get_ticks()
            self.ChangePattern = False
            
        if (self.isNormal):
            self.CurPattern = ('NORMAL', None)
            self.CoolStart = pygame.time.get_ticks()
            self.isNormal = False
        
        if (self.CurPattern[0] == 'NORMAL'):
            self.StartChange = pygame.time.get_ticks()
            self.SetBullets('NORMAL')
            self.UpdatePattern()
        
        elif (self.CurPattern[0] == 'LASER'):
            self.NextPattern = ('NORMAL', None)
            self.SetBullets('LASER')
            self.LaserElapsed = (pygame.time.get_ticks() - self.LaserStart) / 1000
            if (self.LaserElapsed > self.LaserTime):
                self.LCStart = pygame.time.get_ticks()
                self.LaserElapsed = 0
                self.LaserTime = 0
                self.AddPattern = True
                if (self.index == 0):
                    self.isLaser = False
                    self.isNormal = True
                    
                self.UpdatePattern()
                
        elif (self.CurPattern[0] == 'SPINBULLET'):
            pass
            
        elif (self.CurPattern[0] == 'TBD'):
            pass
        
    def UpdatePattern(self):
        if (self.NextPattern is None):
            self.NextPattern = self.PatternQueue.dequeue()
        
        self.CoolElapsed = (pygame.time.get_ticks() - self.CoolStart) / 1000
        if (self.CoolElapsed > self.PatternCool):
            self.CoolElapsed = 0
            self.CoolStart = 0
            
            if (self.LCStart != 0): # 시간경과가 안됨... 코드 바꿔야 할듯
                self.LCElapsed = (pygame.time.get_ticks() - self.LCStart) / 1000
                if (self.LCElapsed > self.LaserCool):
                    self.PatternQueue.enqueue(('LASER', self.pattern_1()))
                    self.LCElapsed = 0
                    self.LCStart = 0
            
        if (self.CurPattern[0] == 'NORMAL'):
            self.ChangePattern = True
            
        if (self.NextPattern[0] == 'LASER'):
            self.AddPattern = False
            self.ChangePattern = True
            self.LaserStart = pygame.time.get_ticks()
                    
        elif (self.NextPattern[0]  == 'SPINBULLET'):
            pass
            
        elif (self.NextPattern[0]  == 'TBD'):
            pass
            
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
        
    def UpdateStat(self, Player):
        for bullet in Player.ProjectileList:
            if (self.HitBox.CheckCollision(bullet.HitBox)):
                self.HP -= (bullet.ATK - self.DEF)
    
    def UpdateCondition(self):
        if (self.HP <= 0):
            self.isDead = True
            self.HitBox.Collidable = False
            
        if (not self.isDead):
            self.StartExist = pygame.time.get_ticks()
            
        else:
            self.ElapsedExist = int((pygame.time.get_ticks() - self.StartExist) / 1000)
            if (self.ElapsedExist > self.ExistTime):
                self.removeable = True
        
    def UpdatePos(self, Player):
        if (self.pos.y + self.HitBox.GetSize('h') < 400):
            self.pos -= self.VEL * 1.5
        else:
            self.Static()
            
        self.HitBox.UpdatePos(self.pos.x, self.pos.y)
        
    def UpdateSprite(self, dt):
        self.current_time += dt
        
        if (self.CurPattern[0] == 'NORMAL'):
            self.conindex = 0
            self.UpdateCycle()
        elif (self.CurPattern[0] == 'LASER'):
            self.conindex = 1
            self.UpdateCycle()
        elif (self.CurPattern[0] == 'SPINBULLET'):
            self.conindex = 2
            self.UpdateCycle()
        elif (self.isDead):
            self.conindex = 3
            self.UpdateCycle()

        if (self.current_time >= self.animation_time):
            self.current_time = 0

            if (self.CurPattern[0] == 'LASER'):
                if (self.LaserElapsed != 0):
                    self.index += 1
                    if (self.index >= len(self.SpriteList[self.conindex])):
                        self.index = len(self.SpriteList[self.conindex]) - 1
                else:
                    self.index -= 1
                    if (self.index <= 0):
                        self.index = 0
                        
            else:
                self.index += 1
                if (self.index >= len(self.SpriteList[self.conindex]) or self.isChangeCondition):
                    self.index = 0
        
    def Update(self, Player, dt):
        self.PatternCycle()
        self.UpdateStat(Player)
        self.UpdateCondition()
        self.UpdatePos(Player)
        self.UpdateSprite(dt)