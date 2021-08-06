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
        self.ChangePattern = False

        self.isLaser = False
        self.readyLaser = False
        self.OpenLaser = False
        self.LCoolOff = False

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
        self.CurPattern = 'NORMAL'
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
        
        self.LaserTime = 4
        self.LaserStart = 0
        self.LaserElapsed = 0.1
        
        self.NormalTime = 2
        self.NormalStart = 0
        self.NormalElapsed = 0
        
        self.SpinTime = 2
        self.SpinStart = 0
        self.SpinElapsed = 0
        
        self.PatternQueue = Queue.Queue()
        
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
        if (not self.OpenLaser):
            self.LaserStart = pygame.time.get_ticks()
            self.OpenLaser = True
        self.isLaser = True

        if (self.index == len(self.SpriteList[self.conindex]) - 1):
            self.SetBullets('LASER')
            self.readyLaser = True
            
    def pattern_2(self):
        pass
        
    def pattern_3(self):
        pass
    
    def PatternCycle(self):
        '''
        if (self.isDetect):
            self.InitStart = pygame.time.get_ticks()
            self.isDetect = False
            self.ChangePattern = False ## *** 추구 지켜봐야할 코드
        '''
        
        if (self.ChangePattern):
            if (self.NextPattern is not None):
                self.CurPattern = self.NextPattern
            self.CoolStart = pygame.time.get_ticks()
            self.ChangePattern = False

        if (self.CurPattern == 'NORMAL'):
            self.isNormal = True
            self.StartChange = pygame.time.get_ticks()
            self.SetBullets('NORMAL')
            self.UpdatePattern()
        
        elif (self.CurPattern == 'LASER'):
            self.pattern_1()
            self.LaserElapsed = (pygame.time.get_ticks() - self.LaserStart) / 1000
            if (self.LaserElapsed >= self.LaserTime):
                self.LaserElapsed = 0 ## 여기에서 openlaser를 거짓으로 처리하면 평생 거짓이 됨...
                self.LaserStart = 0
                self.OpenLaser = False
                self.CurPattern = 'NORMAL' #코드 자체가 꼬인거 같은데..... 모르겠다 어떻게 바꿔야 할 지...
                self.UpdatePattern()

            if (self.LaserElapsed != 0):
                self.LCStart = pygame.time.get_ticks()
                
        elif (self.CurPattern == 'SPINBULLET'):
            pass
            
        elif (self.CurPattern == 'TBD'):
            pass
        
        if (self.CurPattern != 'LASER'):
            self.isChangeCondition = True
            self.StartCool = pygame.time.get_ticks()
            self.CoolUpdate('LASER')

    def CoolUpdate(self, Type):
        if (Type == 'LASER'):
            self.LCElapsed = (pygame.time.get_ticks() - self.LCStart) / 1000
            if (self.LCElapsed >= self.LaserCool):
                self.LCoolOff = True
                self.LCElapsed = 0
                self.LCStart = 0
        
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
            if (not self.PatternQueue.isEmpty()):
                self.NextPattern = self.PatternQueue.dequeue()
            self.ChangePattern = True
            self.CoolElapsed = 0
            self.CoolStart = 0

        if (self.LCoolOff):
            if (self.CurPattern == 'NORMAL'):
                self.CurPattern = 'LASER'
            else:
                self.PatternQueue.enqueue('LASER')
            self.LCoolOff = False

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
        
        if (self.CurPattern == 'NORMAL'):
            self.conindex = 0
            self.UpdateCycle()
        elif (self.CurPattern == 'LASER'):
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
                if (self.OpenLaser):
                    self.index += 1
                    if (self.index >= len(self.SpriteList[self.conindex])):
                        self.index = len(self.SpriteList[self.conindex]) - 1
                        
                else:
                    self.index -= 1
                    if (self.index <= 0):
                        self.index = 0
                        self.isLaser = False

            else:
                self.index += 1
                if (self.index >= len(self.SpriteList[self.conindex])):
                    self.index = 0
        
    def Update(self, Player, dt):
        self.PatternCycle()
        self.UpdateStat(Player)
        self.UpdateCondition()
        self.UpdatePos(Player)
        self.UpdateSprite(dt)