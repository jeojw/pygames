import pygame
import AirCraft
import HitBox
import Stack
import Bullet
import Camera

tmplist = [pygame.image.load('ShootingGame/Sprite/Player_Sprite_' + str(i) + '.png') for i in range(1, 4)]
Invincible = pygame.image.load('ShootingGame/Sprite/Invincible_Sprite.png')
bullet1 = pygame.image.load('ShootingGame/Sprite/Bullet/player_bullet_step_1.png')
bullet2 = pygame.image.load('ShootingGame/Sprite/Bullet/player_bullet_step_2.png')
explode = pygame.image.load('ShootingGame/Sprite/explode_effect.png')

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
        
        self.BulletStack = Stack.Stack()
        self.index = self.BulletStack.GetSize()
        self.bulletindex = 0
        self.SpriteList = [pygame.transform.scale(tmplist[0], (60, 60)),
                           pygame.transform.scale(tmplist[0], (60, 60)),
                           pygame.transform.scale(tmplist[1], (60, 60)),
                           pygame.transform.scale(tmplist[2], (84, 60)),
                           Invincible, explode]
        self.BulletSpriteL = [pygame.image.load('ShootingGame/Sprite/Bullet/player_bullet_step_' + str(i) + '.png') for i in range(1, 3)]
        self.HitBox = HitBox.HitBox(self.SpriteList[self.index], self.pos.x, self.pos.y)
        self.SizeQueue.enqueue(self.SpriteList[self.index].get_size())
        
        self.ChangeConditionTime = 2
        self.StartTime = 0
        self.ElapsedTime = 0
        
        self.InvincibleTime = 1.5
        self.StartInvincible = 0
        self.ElapsedInvincible = 0
        
        self.TwinkleTime = 0.01
        self.StartTwinkle = 0
        self.ElapsedTwinkle = 0
        
        self.BulletInterval = 7
        self.BulletAngle = 10
        self.AtkCool = 0.2
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
        
    def DrawStat(self):
        for i in range(self.HEARTS):
            pygame.draw.circle(self.GAMESCREEN, (255, 0, 0), [740 + i * 50, 150], 20)
    
    def Draw(self):
        self.DrawPos()
        self.DrawStat()
        
    def SetBullets(self, size):
        for i in range(-1, 2, 2):
            self.ProjectileList.append(Bullet.Bullet(self.BulletSpriteL[self.bulletindex], self.HitBox.GetPos('x', True) - self.BulletInterval * i, self.HitBox.GetPos('y'), self.ATK, 10))
    
        if (size == 2):
            for i in range(-1, 2, 2):
                self.ProjectileList.append(Bullet.Bullet(self.BulletSpriteL[self.bulletindex], self.HitBox.GetPos('x', True) - self.BulletInterval * i * 2, self.HitBox.GetPos('y'), self.ATK, 10, self.BulletAngle * i))
        
        elif (size == 3):
            for i in range(-1, 2, 2):
                self.ProjectileList.append(Bullet.Bullet(self.BulletSpriteL[self.bulletindex], self.HitBox.GetPos('x', True) - self.BulletInterval * i * 2, self.HitBox.GetPos('y'), self.ATK, 10, self.BulletAngle * i))
            for i in range(-2, 3, 4):
                self.ProjectileList.append(Bullet.Bullet(self.BulletSpriteL[self.bulletindex], self.HitBox.GetPos('x', True) - self.BulletInterval * i * 2.5, self.HitBox.GetPos('y'), self.ATK, 10))
        
    def UpdateStat(self, Stage):
        if (Stage.SupplyType == 'ATK'):
            if (self.BulletStack.GetSize() <= 3):
                self.BulletStack.push(True)
                Stage.SupplyType = None
                        
        elif (Stage.SupplyType == 'HP'):
            pass
                
        if (self.BulletStack.GetSize() == 0):
            self.bulletindex = 0
        elif (self.BulletStack.GetSize() >= 1):
            self.bulletindex = 1
    
    def UpdateCondition(self, Stage):
        
        if (self.isAttack and not self.isDead):
            self.SetBullets(self.BulletStack.GetSize())
            self.isAttack = False
            self.StartCool = pygame.time.get_ticks()
        self.ElapsedCool = (pygame.time.get_ticks() - self.StartCool) / 1000
        
        if (self.ElapsedCool > self.AtkCool):
            self.isAttack = True
            self.ElapsedCool = 0
            self.StartCool = 0
        

        for enemy in Stage.EnemyList:
            for bullet in enemy.ProjectileList:
                if (self.HitBox.CheckCollision(bullet.HitBox)):
                    self.HEARTS -= 1
                    self.Condition = 'Invincible'
                    self.BulletStack.pop()
                    self.HitBox.Collidable = False
                    self.StartInvincible = pygame.time.get_ticks()
                    
        for bullet in Stage.BOSS.ProjectileList:
            if (self.HitBox.CheckCollision(bullet.HitBox)):
                self.HEARTS -= 1
                self.Condition = 'Invincible'
                self.BulletStack.pop()
                self.HitBox.Collidable = False
                self.StartInvincible = pygame.time.get_ticks()

        if (not self.HitBox.Collidable):
            self.ElapsedInvincible = (pygame.time.get_ticks() - self.StartInvincible) / 1000
            if (self.ElapsedInvincible > self.InvincibleTime):
                self.Condition = 'NonInvincible'
                self.HitBox.Collidable = True
                self.ElapsedInvincible = 0
                self.StartInvincible = 0
                
        if (self.HEARTS <= 0):
            self.isDead = True
            self.isMove = False
            self.HitBox.Collidable = False
        
    def UpdatePos(self):
        super().UpdatePos()
        
        if (self.pos.x < 0):
            self.pos.x = 0
        elif (self.pos.x + self.HitBox.GetSize('w') > self.LIMITSIZE.x):
            self.pos.x = self.LIMITSIZE.x - self.HitBox.GetSize('w')
        elif (self.pos.y < 0):
            self.pos.y = 0
        elif (self.pos.y + self.HitBox.GetSize('h') > self.LIMITSIZE.y):
            self.pos.y = self.LIMITSIZE.y - self.HitBox.GetSize('h')

        if (self.isMove):
            if (self.direction == 'LEFT'):
                self.pos.x -= self.VEL.x
            elif (self.direction == 'RIGHT'):
                self.pos.x += self.VEL.x
            elif (self.direction == 'UP'):
                self.pos.y -= self.VEL.y
            elif (self.direction == 'DOWN'):
                self.pos.y += self.VEL.y
                
        self.HitBox.UpdatePos(self.pos.x, self.pos.y, self.SpriteList[self.index])
            
    def UpdateSprite(self):
        self.index = self.BulletStack.GetSize()
        if (self.Condition == 'Invincible'):
            if (self.ElapsedInvincible > self.InvincibleTime):
                self.index = self.BulletStack.GetSize()
                self.ElapsedTime = 0
                self.StartTime = 0
                
        if (self.isDead):
            self.index = len(self.SpriteList) - 1
        
        self.HitBox.Draw()
        if (self.BulletStack.GetSize() <= 2): # 스프라이트 이미지 크기를 통해 위치 재조정 할 예정(히트박스 크기 X!)
            self.HitBox.UpdateSize(self.SpriteList[self.index])
        
    
    def Update(self, Stage):
        self.UpdateStat(Stage)
        self.UpdatePos()
        self.UpdateCondition(Stage)
        self.UpdateSprite()