import pygame
import AirCraft
import HitBox
import Stack
import Bullet
import Camera

samplesprite = pygame.image.load('ShootingGame/Sprite/AIRCRAFT_SAMPLE.png')
Invincible = pygame.image.load('ShootingGame/Sprite/Invincible_Sprite.png')
bulletsprite = pygame.image.load('ShootingGame/Sprite/Player_Bullet.png')

class PlayerAirCraft(AirCraft.AirCraft):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.HEARTS = 4
        self.ATK = 100 # 공격력
        self.DEF = 20 # 방어력
        self.ATKCOUNTS = 2 # 발사되는 투사체 개수
        self.VEL = pygame.math.Vector2(6, 6) # 속도
        self.PlayerStat = [4, 100, 20, 2] # 플레이어의 스텟을 저장하는 리스트
        self.Condition = 'NonInvincible'
        
        self.isGetItem = False

        self.index = 0
        self.SpriteList = [samplesprite]
        self.cursprite = self.SpriteList[self.index]
        self.HitBox = HitBox.HitBox(self.cursprite, self.pos.x, self.pos.y)
        
        self.BulletStack = Stack.Stack()
        
        self.ChangeConditionTime = 2
        self.StartTime = 0
        self.ElapsedTime = 0
        
        self.BulletInterval = 7
        self.BulletAngle = 20
        self.AtkCool = 0.1
        self.StartCool = 0
        self.ElapsedCool = 0
        
    def DrawStat(self):
        pass
    
    def Draw(self):
        self.DrawPos()
        self.DrawStat()
        
    def UpdateStat(self, Stage):
        for item in Stage.ItemList:
            if (self.HitBox.checkcollision(item)):
                if (item.GetType() == 'ATK'):
                    pass
    
    def UpdateCondition(self, Stage):
        if (self.isAttack):
            if (self.BulletStack.GetSize() == 0):
                self.ProjectileList.append(Bullet.Bullet(bulletsprite, self.HitBox.GetPos('x', True) - self.BulletInterval, self.HitBox.GetPos('y'), self.ATK))
                self.ProjectileList.append(Bullet.Bullet(bulletsprite, self.HitBox.GetPos('x', True) + self.BulletInterval, self.HitBox.GetPos('y'), self.ATK))
                self.ProjectileList.append(Bullet.Bullet(bulletsprite, self.HitBox.GetPos('x', True) - self.BulletInterval * 2, self.HitBox.GetPos('y'), self.ATK, self.BulletAngle))
                self.ProjectileList.append(Bullet.Bullet(bulletsprite, self.HitBox.GetPos('x', True) + self.BulletInterval * 2, self.HitBox.GetPos('y'), self.ATK, self.BulletAngle))
            elif (self.BulletStack.GetSize() == 1):
                self.ProjectileList.append(Bullet.Bullet(bulletsprite, self.HitBox.GetPos('x', True) - self.BulletInterval, self.HitBox.GetPos('y'), self.ATK))
                self.ProjectileList.append(Bullet.Bullet(bulletsprite, self.HitBox.GetPos('x', True) + self.BulletInterval, self.HitBox.GetPos('y'), self.ATK))
                self.ProjectileList.append(Bullet.Bullet(bulletsprite, self.HitBox.GetPos('x', True) - self.BulletInterval, self.HitBox.GetPos('y'), self.ATK), self.BulletAngle)
                self.ProjectileList.append(Bullet.Bullet(bulletsprite, self.HitBox.GetPos('x', True) + self.BulletInterval, self.HitBox.GetPos('y'), self.ATK), self.BulletAngle)
            self.isAttack = False
            self.StartCool = pygame.time.get_ticks()
        self.ElapsedCool = (pygame.time.get_ticks() - self.StartCool) / 1000
        
        if (self.ElapsedCool > self.AtkCool):
            self.isAttack = True
            self.ElapsedCool = 0
            self.StartCool = 0
            
        if (self.ElapsedCool > self.AtkCool):
            self.ElapsedCool = 0
        
        for bullet in Stage.BulletList:
            if (self.HitBox.CheckCollision(bullet)):
                self.isGetAttack = True
                self.Condition = 'Invincible'
                self.BulletStack.pop()
                self.StartTime = pygame.time.get_ticks()

        if (self.Condition == 'Invincible'):
            self.ElapsedTime = int((pygame.time.get_ticks() - self.StartTime) / 1000)
            if (self.ElapsedTime > self.ChangeConditionTime):
                self.Condition = 'NonInvincible'
                self.isGetAttack = False
        
    def UpdatePos(self):
        if (self.pos.x < 0):
            self.pos.x = 0
        elif (self.pos.x + self.HitBox.GetSize('w') > self.SCREENSIZE[0]):
            self.pos.x = self.SCREENSIZE[0] - self.HitBox.GetSize('w')
        elif (self.pos.y < 0):
            self.pos.y = 0
        elif (self.pos.y + self.HitBox.GetSize('h') > self.SCREENSIZE[1]):
            self.pos.y = self.SCREENSIZE[1] - self.HitBox.GetSize('h')
        
        if (self.isMove):
            if (self.direction == 'LEFT'):
                self.pos.x -= self.VEL.x
            elif (self.direction == 'RIGHT'):
                self.pos.x += self.VEL.x
            elif (self.direction == 'UP'):
                self.pos.y -= self.VEL.y
            elif (self.direction == 'DOWN'):
                self.pos.y += self.VEL.y
                
        self.HitBox.Update(self.pos.x, self.pos.y)
        self.HitBox.Draw()
            
    def UpdateSprite(self):
        pass
    
    def Update(self, Stage):
        self.UpdateStat(Stage)
        self.UpdatePos()
        self.UpdateCondition(Stage)
        self.UpdateSprite()