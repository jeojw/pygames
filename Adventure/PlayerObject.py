import LifeObject
import Projectile
import pygame

JUMPDISTANCE = 80
AIRSPACE = -10
GRAVITY = 10
DURATION = 20
AMMUNITION = 30

'''
오브젝트 관련 변수
'''
PLAYERATKCOOL = 1
PLAYAERRANGE = 300

'''
아이템 아이콘, 이펙트 관련 변수
'''
ICE = 'Adventure/char_sprite/ice.png'
ARMOR = 'Adventure/items/shield.png'
HASTE = 'Adventure/items/haste.png'
ATTACKSPEED = 'Adventure/items/attackspeed.png'
HPRECOVERY = 'Adventure/items/hprecovery.png'
MAXHPUP = 'Adventure/items/hpmaxup.png'
COIN = 'Adventure/items/coin.png'

BASIC = 'Adventure/char_sprite/bubble.png'
REINFORCE = 'Adventure/char_sprite/ice.png'

ICEICON = pygame.image.load(ICE)
ARMORICON = pygame.image.load(ARMOR)
HASTEICON = pygame.image.load(HASTE)
ATTACKSPEEDICON = pygame.image.load(ATTACKSPEED)
HPRECOVERYICON = pygame.image.load(HPRECOVERY)
MAXHPUPICON = pygame.image.load(MAXHPUP)
COINICON = pygame.image.load(COIN)

class PlayerObject(LifeObject.LifeObject):
    def __init__(self, System, x_pos, y_pos=None):
        '''
        플레이어의 기본적인 정보를 설정하는 생성자
        여기에서 스프라이트 및 쿨타임 등을 관리함
        '''
        super().__init__(System, x_pos, y_pos)
        
        self.direction = 'right'
        self.getitem = False
        self.itemcounts = 0 #누적으로 획득한 아이템 개수
        self.coincounts = 0 #코인 개수
        self.itemType = None
        self.projectileimage = BASIC
        self.ammunition = 30 # 강화 공격 제한 개수
        self.duration = 20 # 아이템 지속 시간
        self.itemStart = 0 # 아이템 시작 시간
        self.itemElapsed = 0 # 아이템 획득 후 경과시간
        self.atkcool = PLAYERATKCOOL
        
        self.PlayerStat = [750, 750, 1000, 0, 10]
        
        static = [pygame.image.load('Adventure/char_sprite/char_static.png')]
        dead = [pygame.image.load('Adventure/char_sprite/char_dead.png')]
        walk = [pygame.image.load('Adventure/char_sprite/char_walk_' + str(i) + '.png') for i in range(1, 4)]
        attack = [pygame.image.load('Adventure/char_sprite/char_attack.png')]
        getattack = [pygame.image.load('Adventure/char_sprite/char_get_attack.png')]

        self.spritelist = [static, walk, attack, getattack ,dead]
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
        self.animation_time = round(100 / len(self.spritelist[self.cur] * 100), 2)
        
    def ResetCondition(self):
        '''
        플레이어의 체력을 제외한 모든 스텟 및 시간을 초기화시키는 메서드
        주로 아이템을 중복으로 먹었을 시에 활성화 됨
        '''
        self.MAXHP = self.PlayerStat[0]
        self.ATK = self.PlayerStat[2]
        self.DEF = self.PlayerStat[3]
        self.SPEED = self.PlayerStat[4]
        self.projectileimage = BASIC
        
        self.duration = DURATION
        self.itemStart = 0
        self.itemElapsed = 0
        self.atkcool = PLAYERATKCOOL
        self.ammunition = AMMUNITION
        
    def GetPos(self, pos):
        '''
        오브젝트의 위치 반환
        '''
        try:
            if (pos == 'x'):
                return self.hitbox.x
            elif (pos == 'y'):
                return self.hitbox.y
            else:
                raise ValueError
        except ValueError:
            print(pos, 'is not Pos!!!!')
        
    def GetSize(self, length):
        '''
        오브젝트의 크기 반환
        '''
        try:
            if (length == 'width'):
                return self.hitbox.width
            elif (length == 'height'):
                return self.hitbox.height
            else:
                raise ValueError
        except ValueError:
            print(length, 'is not Lenght!!!')
                
    def attack(self):
        '''
        플레이어의 공격 상태를 설정하는 메서드
        플레이어는 원거리 공격을 주로 하므로 공격판정마다 projectilelist 내에 방향을 추가
        (overriding)
        '''
        super().attack()
        if (self.itemType == ICE and self.coolElapsed == 0):
            self.ammunition -= 1
        if (self.isDead is False and self.isGetattack is False and self.coolElapsed == 0):
            if (self.direction == 'left'):
                self.projectilelist.append(Projectile.Projectile(self.projectileimage, self.hitbox.left, self.hitbox.y, self.ATK, 'left'))
            else:
                self.projectilelist.append(Projectile.Projectile(self.projectileimage, self.hitbox.right, self.hitbox.y, self.ATK, 'right'))
                 
    def getItem(self, Stage):
        '''
        아이템을 얻게 해주는 메서드 아이템 종류에 따라 효과가 다르게 발동되도록 변경
        '''
        for item in Stage.GetItemlist():
            if (self.checkcollision(item)):
                Stage.removeItem(item)
                self.getitem = True
                if (item.GetImage() != COIN):
                    self.isChangeStat = True
                    self.itemcounts += 1
                    if (item.GetImage() == ICE):
                        self.itemType = ICE
                        self.ResetCondition()
                        self.ChangeStat(*item.GetStat(ICE))
                        self.projectileimage = REINFORCE
                        self.getitem = False
                    elif (item.GetImage() == ARMOR):
                        self.itemType = ARMOR
                        self.ResetCondition()
                        self.ChangeStat(*item.GetStat(ARMOR))
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == HASTE):
                        self.itemType = HASTE
                        self.ResetCondition()
                        self.ChangeStat(*item.GetStat(HASTE))
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == ATTACKSPEED):
                        self.itemType = ATTACKSPEED
                        self.ResetCondition()
                        self.ChangeStat(*item.GetStat(ATTACKSPEED))
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == MAXHPUP):
                        self.itemType = MAXHPUP
                        self.ResetCondition()
                        self.ChangeStat(*item.GetStat(MAXHPUP))
                        self.HP = self.MAXHP
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == HPRECOVERY):
                        self.HP = self.MAXHP
                        self.getitem = False
                else:
                    self.coincounts += 1
                    self.getitem = False
                
    def ItemReset(self):
        '''
        아이템 효과가 다할 시에 관련 변수들을 리셋시켜주는 메서드
        복잡하길래 그냥 하나로 묶어버림
        '''
        self.itemType = None
        self.ResetCondition()
        self.isChangeStat = False
        if (self.itemType == ICE):
            self.projectileimage = BASIC
            self.ammunition = AMMUNITION
        else:
            self.itemElapsed = 0
            self.itemStart = 0

    def drawStat(self):
        '''
        플레이어의 스텟을 그려주는 메서드
        '''
        Length = 200
        convertCoefficient = Length / self.MAXHP
        pygame.draw.rect(self.system.GetScreen(), self.system.GetColor('virginred'), (10, 10, Length, 30), 2)
        if (self.HP >= 0):
            pygame.draw.rect(self.system.GetScreen(), self.system.GetColor('red'), (10, 10, self.HP * convertCoefficient , 30))
            
        if (self.itemType == ICE):
            self.system.GetScreen().blit(ICEICON, (Length + 20, 15))
            self.system.write(self.system.GetSmallFont(), ' X ' + str(self.ammunition), self.system.GetColor('black'), Length + 40, 15)
        elif (self.itemType == ARMOR):
            self.system.GetScreen().blit(ARMORICON, (Length + 20, 15))
            self.system.write(self.system.GetSmallFont(), ' : ' + str(self.duration - self.itemElapsed) + ' sec ', self.system.GetColor('black'), Length + 40, 15)
        elif (self.itemType == HASTE):
            self.system.GetScreen().blit(HASTEICON, (Length + 20, 15))
            self.system.write(self.system.GetSmallFont(), ' : ' + str(self.duration - self.itemElapsed) + ' sec ', self.system.GetColor('black'), Length + 40, 15)
        elif (self.itemType == ATTACKSPEED):
            self.system.GetScreen().blit(ATTACKSPEEDICON, (Length + 20, 15))
            self.system.write(self.system.GetSmallFont(), ' : ' + str(self.duration - self.itemElapsed) + ' sec ', self.system.GetColor('black'), Length + 40, 15)
            
    def updateCondition(self, Stage):
        '''
        플레어어의 컨디션을 업데이트 시켜주는 함수
        불값을 기반으로 업데이트 시켜줌
        
        아이템 관련 및 피격까지 관리함
        '''
        super().updateCondition()
        for enemy in Stage.GetEnemylist():
            if (enemy.GetName() == 'Seal'):
                if (self.isHitbox):
                    if (self.checkcollision(enemy) and enemy.GetCondition('atkhitbox')):
                        self.getattack(enemy)
            
            if (enemy.GetName() == 'SnowMan'):
                for projectile in enemy.GetProjectiles():
                    if (len(enemy.GetProjectiles()) != 0):
                        if (self.isHitbox):
                            if (self.checkcollision(projectile)):
                                self.getattack(enemy)
                                enemy.GetProjectiles().remove(projectile)
                    
        if (self.isChangeStat):
            if (self.itemType == ICE):
                if (self.ammunition == 0):
                    self.ItemReset()
            elif (self.itemType == ARMOR):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
            elif (self.itemType == HASTE):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
            elif (self.itemType == ATTACKSPEED):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
            elif (self.itemType == MAXHPUP):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
                    if (self.HP > self.MAXHP):
                        self.HP = self.MAXHP
                        
    def updatePos(self, Stage):
        '''
        오브젝트의 위치를 업데이트 시키는 메서드
        플레이어는 카메라의 위치에 따라 위치가 보정되도록 변경됨
        '''
        self.hitbox.x = self.x_pos
        self.hitbox.bottom = self.y_pos

        if (Stage.GetCameraView('x') <= Stage.map_x_size - self.system.GetXSize() or Stage.GetCameraView('x') >= 0): ## check
            if (self.hitbox.centerx > Stage.GetCameraRange('x') and self.direction == 'right'):
                if (Stage.XCameraMoveable and not Stage.forceXMove):
                    Stage.CameraXMovement(self.SPEED)
                    self.x_pos -= self.SPEED
            if (self.hitbox.centerx <= Stage.GetCameraRange('x') and Stage.GetCameraView('x') > 0 and self.direction == 'left'): ## check
                if (Stage.XCameraMoveable):
                    Stage.CameraXMovement(-self.SPEED)
                    self.x_pos += self.SPEED
                    
            if (Stage.forceXMove):
                Stage.CameraXMovement(self.SPEED)
                self.x_pos -= self.SPEED
                
        if (Stage.XCameraMoveable is False):
            if (self.hitbox.left <= Stage.GetMapLimit('left')):
                self.x_pos = Stage.GetMapLimit('left')
            if (self.hitbox.right >= Stage.GetMapLimit('right')):
                self.x_pos = Stage.GetMapLimit('right') - self.hitbox.width
                
        if (self.isOnGround is False):
            self.y_pos += self.airSpace
            Stage.CameraYMovement(self.airSpace)
            if (self.y_pos <= Stage.GetMapLimit('onground') - JUMPDISTANCE):
                self.airSpace = 0
                self.gravity = GRAVITY
            self.y_pos += self.gravity
            Stage.CameraYMovement(self.gravity)
        if (self.y_pos >= Stage.GetMapLimit('onground')):
            self.y_pos = Stage.GetMapLimit('onground')
            self.isOnGround = True
            self.gravity = 0
            self.airSpace = AIRSPACE
                
        if (self.isWalk and self.isAttack is False):
            if (self.direction == 'left'):
                self.x_pos += -self.SPEED
            elif (self.direction == 'right'):
                self.x_pos += self.SPEED
                
    def updateSprite(self, dt):# 추후 아이템 획득시에도 스프라이트 관련 업데이트를 추가할 것
        '''
        적의 스프라이트를 업데이트 시켜주는 함수
        스프라이트 업데이트 지연까지 추가함
        '''  
        self.current_time += dt
        
        if (self.Condition == 'static'):
            self.cur = 0
            self.updateCycle()
        if (self.Condition == 'walk'):
            self.cur = 1
            self.updateCycle()
        if (self.Condition == 'attack'):
            self.cur = 2
            self.updateCycle()
        if (self.Condition == 'getattack'):
            self.cur = 3
            self.updateCycle()
            self.isGetattack = False
        if (self.Condition == 'dead'):
            self.cur = 4
            self.isChangeCondition = False
        
        if (self.current_time >= self.animation_time or self.isChangeCondition):
            self.current_time = 0
            
            self.index += 1
            if (self.index >= len(self.spritelist[self.cur]) or self.isChangeCondition):
                self.index = 0
        
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
                
    def update(self, dt, Stage):
        '''
        통합 update 메서드
        가독성을 위해
        '''
        self.updateCondition(Stage)
        self.updatePos(Stage)
        self.updateSprite(dt)