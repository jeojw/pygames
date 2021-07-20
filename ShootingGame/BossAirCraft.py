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
        self.conindex = 0
        self.index = 0
        self.SpriteList = [[BossSprite], 
                           [pygame.transform.scale(sp, (600, 540)) for sp in BossLaser], 
                           [pygame.transform.scale(sp, (600, 450)) for sp in BossSpinBullet], 
                           []]
        self.HitBox = HitBox.HitBox(BossSprite, self.pos.x, self.pos.y)
        self.SizeQueue.enqueue((self.HitBox.GetSize('w'), self.HitBox.GetSize('h')))
        self.pattern = ('None', None)
        
        self.LaserTime = 5
        self.LaserStart = 0
        self.LaserElapsed = 0 
        
        self.PatternQueue = Queue.Queue()
        self.PatternQueue.enqueue(('LASER', self.pattern_1()))
        self.PatternQueue.enqueue(('LASER', self.pattern_1()))
        #self.PatternQueue.enqueue(('TBD', self.pattern_3()))
        self.patterndelay = 0.5
        
        self.Changedelay = 0.5
        self.StartChange = 0
        self.ElapsedChange = 0
        
        self.PatternCool = 5
        self.CoolStart = 0
        self.CoolElapsed = 0
        
        self.PatternDelay = 2
        self.StartPattern = 0
        self.ElapsedPattern = 0
        
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
        if (self.pattern[0] != 'LASER'):
            self.isChangeCondition = True
            self.StartChange = pygame.time.get_ticks()
        
        self.CoolStart = pygame.time.get_ticks()
        
        if (self.index == len(self.SpriteList[1]) - 1):
            self.SetBullets('LASER')
            
    def pattern_2(self):
        pass
        
    def pattern_3(self):
        pass
    
    def AI(self):
        if (self.pattern[0] == 'None'):
            self.SetBullets('NORMAL')
        
        if (not self.PatternQueue.isEmpty()):
            self.pattern = self.PatternQueue.dequeue()
        
        if (self.pattern[0] == 'LASER'):
            self.LaserElapsed = (pygame.time.get_ticks() - self.LaserStart) / 1000
            if (self.LaserElapsed > self.LaserTime):
                self.LaserElapsed = 0
                self.LaserTime = 0
                self.CoolElapsed = (pygame.time.get_ticks() - self.StartCool) / 1000
                if (self.CoolElapsed > self.PatternCool):
                    self.CoolElapsed = 0
                    self.StartCool = 0
                    self.PatternQueue.enqueue(self.pattern_1())
                
        elif (self.pattern[0] == 'SPINBULLET'):
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
        self.pattern = ('LASER', self.pattern_1())
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
        
        if (self.pattern[0] == 'None'):
            self.conindex = 0
            self.UpdateCycle()
        if (self.pattern[0] == 'LASER'):
            self.conindex = 1
            self.UpdateCycle()
        elif (self.pattern[0] == 'SPINBULLET'):
            self.conindex = 2
            self.UpdateCycle()
        elif (self.isDead):
            self.conindex = 3
            self.UpdateCycle()

        if (self.current_time >= self.animation_time):
            self.current_time = 0

            if (self.pattern[0] == 'LASER'):
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
        self.AI()
        self.UpdateStat(Player)
        self.UpdateCondition()
        self.UpdatePos(Player)
        self.UpdateSprite(dt)