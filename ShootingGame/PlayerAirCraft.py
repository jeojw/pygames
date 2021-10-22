import pygame
import AirCraft
import HitBox
import Stack
import Bullet
import Camera

# 플레이어 탄환 스프라이트 조정할 것!!!
tmplist = [pygame.image.load('ShootingGame/Sprite/Player_Sprite_' + str(i) + '.png') for i in range(1, 4)]
Invincible = pygame.image.load('ShootingGame/Sprite/Invincible_Sprite.png')
explode = pygame.image.load('ShootingGame/Sprite/explode_effect.png')
explode_effect = pygame.transform.scale(explode, (70, 70))
shield= pygame.image.load('ShootingGame/Sprite/Player_Shield_1.png')
shield_1 = pygame.transform.scale(shield, (90, 90))
shield_2 = pygame.transform.scale(shield, (120, 120))

class PlayerAirCraft(AirCraft.AirCraft):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)
        self.MAXHEARTS = 6
        self.HEARTS = 4
        self.ATK = 30 # 공격력
        self.ATKcoff = 1.2
        self.ATKCOUNTS = 2 # 발사되는 투사체 개수
        self.VEL = pygame.math.Vector2(6, 6) # 속도
        self.PlayerStat = [4, 100, 20, 2] # 플레이어의 스텟을 저장하는 리스트
        self.Condition = 'Normal'
        self.TwinkleStack = 0
        
        self.isGetItem = False
        self.isShield = False
        self.isTwinkle = False
        self.curShield = shield_1
        self.shieldpos = pygame.math.Vector2(x_pos, y_pos)
        
        self.BulletStack = Stack.Stack()
        self.index = self.BulletStack.GetSize()
        self.bulletindex = self.BulletStack.GetSize()
        self.SpriteList = [pygame.transform.scale(tmplist[0], (60, 60)),
                           pygame.transform.scale(tmplist[0], (60, 60)),
                           pygame.transform.scale(tmplist[1], (60, 60)),
                           pygame.transform.scale(tmplist[2], (84, 60)),
                           pygame.transform.scale(Invincible, (60, 60)),
                           pygame.transform.scale(Invincible, (60, 60)),
                           pygame.transform.scale(Invincible, (60, 60)),
                           pygame.transform.scale(Invincible, (84, 60)),
                           explode_effect]
        self.BulletSpriteL = [pygame.image.load('ShootingGame/Sprite/Bullet/PlayerBullet/player_bullet_step_' + str(i) + '.png') for i in range(1, 4)]
        self.HitBox = HitBox.HitBox(self.SpriteList[self.index], self.pos.x, self.pos.y)
        self.SizeQueue.enqueue(self.SpriteList[self.index].get_size())
        
        self.ChangeConditionTime = 2
        self.StartTime = 0
        self.ElapsedTime = 0
        
        self.TwinkleTime = 0.5
        self.StartTwinkle = 0
        self.ElapsedTwinkle = 0
        
        self.BulletInterval = 7
        self.BulletAngle = 10
        self.AtkCool = 0.5
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
        
        if (self.isShield):
            self.GAMESCREEN.blit(self.curShield, (self.shieldpos.x, self.shieldpos.y))
    
    def Draw(self):
        self.HitBox.Draw()
        self.DrawPos()
        self.DrawStat()
        
    def SetBullets(self, size):
        if (size <= 1):
            for i in range(-1, 2, 2):
                self.ProjectileList.append(Bullet.Bullet(self.BulletSpriteL[size], self.HitBox.GetPos('x', True) - self.BulletInterval * i, self.HitBox.GetPos('y'), self.ATK, 10))
    
        if (size == 2):
            for i in range(-1, 2, 2):
                self.ProjectileList.append(Bullet.Bullet(self.BulletSpriteL[size], self.HitBox.GetPos('x', True) - self.BulletInterval * i, self.HitBox.GetPos('y'), self.ATK * (self.ATKcoff * (size - 1)), 10))
                self.ProjectileList.append(Bullet.Bullet(self.BulletSpriteL[size - 2], self.HitBox.GetPos('x', True) - self.BulletInterval * i * 2, self.HitBox.GetPos('y'), self.ATK, 10, self.BulletAngle * i))
        
        elif (size == 3):
            for i in range(-1, 2, 2):
                self.ProjectileList.append(Bullet.Bullet(self.BulletSpriteL[size -  1], self.HitBox.GetPos('x', True) - self.BulletInterval * i, self.HitBox.GetPos('y'), self.ATK * (self.ATKcoff * (size - 1)), 10))
                self.ProjectileList.append(Bullet.Bullet(self.BulletSpriteL[size - 2], self.HitBox.GetPos('x', True) - self.BulletInterval * i * 2, self.HitBox.GetPos('y'), self.ATK * (self.ATKcoff * (size - 2)), 10, self.BulletAngle * i))
            for i in range(-2, 3, 4):
                self.ProjectileList.append(Bullet.Bullet(self.BulletSpriteL[size - 3], self.HitBox.GetPos('x', True) - self.BulletInterval * i * 2.5, self.HitBox.GetPos('y'), self.ATK, 10))
                
    def GetShield(self):
        self.isShield = True
        
    def ShieldOff(self):
        self.isShield = False
        
    def UpdateStat(self, Stage):
        if (Stage.SupplyType == 'ATK'):
            if (self.BulletStack.GetSize() <= 3):
                self.BulletStack.push(True)
            Stage.SupplyType = None
                        
        elif (Stage.SupplyType == 'RECOVERY'):
            if (self.HEARTS < self.MAXHEARTS):
                self.HEARTS += 1
            Stage.SupplyType = None
        
        elif (Stage.SupplyType == 'SHIELD'):
            self.GetShield()
            Stage.SupplyType = None
            
        elif (Stage.SupplyType == 'AS'):
            self.AtkCool = 0.3
            Stage.SupplyType = None
            
        if (self.isShield):
            if (self.BulletStack.GetSize() < 3):
                self.curShield = shield_1
            elif (self.BulletStack.GetSize() == 3):
                self.curShield = shield_2   
            
            diffsize = pygame.math.Vector2(abs(self.curShield.get_width() - self.SpriteList[self.index].get_width()) / 2, abs(self.curShield.get_height() - self.SpriteList[self.index].get_height()) / 2)
            self.shieldpos = pygame.math.Vector2(self.pos.x - diffsize.x, self.pos.y - diffsize.y)        
            self.HitBox.UpdateSize(self.curShield)
    
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
        
        
        if (self.isGetAttack):
            if (not self.isShield):
                self.HEARTS -= 1
                self.Condition = 'Invincible'
                self.BulletStack.pop()
                if (self.AtkCool != 0.5):
                    self.AtkCool = 0.5
                self.HitBox.Collidable = False
            else:
                self.ShieldOff()
            self.NotGetAttack()
        
        if (not self.HitBox.Collidable):
            if (not self.isTwinkle):
                self.StartTwinkle = pygame.time.get_ticks()
                self.isTwinkle = True
        
            self.ElapsedTwinkle = (pygame.time.get_ticks() - self.StartTwinkle) / 1000
            if (self.ElapsedTwinkle > self.TwinkleTime):
                self.TwinkleStack += 1
                self.isTwinkle = False
                self.ElapsedTwinkle = 0
                self.StartTwinkle = 0

            if (self.TwinkleStack > 4):
                self.Condition = 'Normal'
                self.HitBox.Collidable = True
                self.TwinkleStack = 0
                
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
                
        self.HitBox.UpdatePos(self.pos.x, self.pos.y, self.CurSprite)
            
    def UpdateSprite(self):
        self.index = self.BulletStack.GetSize()
        if (self.isTwinkle):
            self.index = self.BulletStack.GetSize() + 4
        else:
            self.index = self.BulletStack.GetSize()
                
        if (self.isDead):
            self.index = len(self.SpriteList) - 1
            
        self.CurSprite = self.SpriteList[self.index]
        
        if (self.BulletStack.GetSize() <= 2): # 스프라이트 이미지 크기를 통해 위치 재조정 할 예정(히트박스 크기 X!)
            self.HitBox.UpdateSize(self.CurSprite)
        
    
    def Update(self, Stage):
        self.UpdateStat(Stage)
        self.UpdatePos()
        self.UpdateCondition(Stage)
        self.UpdateSprite()