import pygame
import EnemyAirCraft
import Queue
import HitBox
import Bullet

Boss = pygame.image.load('ShootingGame/Sprite/Boss/Boss_Sprite.png')
BossLaser = [pygame.image.load('ShootingGame/Sprite/Boss/Boss_Laser_' + str(i) +_'.png') for i in range(0, 6)]
BossSpinBullet = [pygame.image.load('ShootingGame/Sprite/Boss/Boss_Spin_' + str(i) +_'.png') for i in range(0, 6)]
laser = pygame.image.load('ShootingGame/Sprite/Bullet/laser.png')
BossSprite = pygame.transform.scale(Boss, (600, 450))
LaserSprite = pygame.transform.scale(laser, (18, 240))

class BossAirCraft(EnemyAirCraft.EnemyAirCraft):
    def __init__(self, MAXHP, ATK, DEF, y_pos):
        super().__init__(MAXHP, ATK, DEF, 50, y_pos)
        
        self.isExist = False
        self.conindex = 0
        self.index = 0
        self.SpriteList = [[BossSprite], [pygame.trasform.scale(sp, (600, 540)) for sp in BossLaser], 
                           [pygame.trasform.scale(sp, (600, 450)) for sp in BossSpinBullet], []]
        self.HitBox = HitBox.HitBox(BossSprite, self.pos.x, self.pos.y)
        self.SizeQueue.enqueue((self.HitBox.GetSize('w'), self.HitBox.GetSize('h')))
        self.pattern = None
        
        self.PatternQueue = Queue.Queue()
        self.patterndelay = 0.5
        
        self.LaserTime = 2
        self.LaserStart = 0
        self.LaserElapsed = 0
        
    def SetBullets(self, Type):
        pass
    
    def pattern_1(self):
        self.SetBullets('LASER')
        self.LaserElapsed = (pygame.time.get_ticks() - self.LaserStart) / 1000
        if (self.LaserElapsed > self.LaserTime):
            self.LaserStart = 0
            self.LaserElapsed = 0
            
            return 'Finish'
    
    def pattern_2(self):
        pass
        
    def pattern_3(self):
        pass
    
    def AI(self):
        self.SetBullets('Normal')
        self.PatternQueue.enqueue(self.pattern_1)
        
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
        if (self.pos.y + self.HitBox.GetSize('h') < 400):
            self.pos -= self.VEL * 1.5
        else:
            self.index = 1
            self.Static()
            
        self.HitBox.UpdatePos(self.pos.x, self.pos.y)
        
    def UpdateSprite(self, dt):
        if (self.Condition == 'NORMAL'):
            pass
        if (self.pattern == 'LASER'):
            self.conindex = 1
            self.index = 0
        elif (self.pattern == 'SPIN'):
            self.conindex = 2
            self.index = 0
        elif (self.isDead):
            self.conindex = 3
            self.index = 0
            
        self.index += 1
        if (self.index >= len(self.SpriteList[self.conindex])):
            self.index = len(self.SpriteList[self.conindex]) - 1
        
    def Update(self, Player, dt):
         self.UpdateStat(Player)
        self.UpdateCondition()
        self.UpdatePos(Player)
        self.UpdateSprite(dt)