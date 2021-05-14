import random
import LifeObject
import ItemObject
import pygame

'''
오브젝트 관련 변수
'''
ENEMYATKCOOL = 1

'''
아이템 아이콘, 이펙트 관련 변수
'''
ICE = 'char_sprite/ice.png'
ARMOR = 'items/shield.png'
HASTE = 'items/haste.png'
ATTACKSPEED = 'items/attackspeed.png'
HPRECOVERY = 'items/hprecovery.png'
MAXHPUP = 'items/hpmaxup.png'
COIN = 'items/coin.png'

ItemTypes = [ICE, ARMOR, HASTE, ATTACKSPEED, HPRECOVERY, MAXHPUP] # 아이템 타입, 주로 스프라이트 파일로 통해 아이템 획득을 구분할 예정

DETECTICON = pygame.image.load('effect_icon/detectIcon.png')

'''
적 타입 및 이름을 나타내는 변수
'''
NORMAL = 'Normal'
BOSS = 'Boss'

class EnemyObject(LifeObject.LifeObject):
    def __init__(self, Type, System, x_pos, y_pos=None):
        '''
        적의 기본적인 정보를 저장하는 생성자
        '''
        super().__init__(System, x_pos, y_pos)
        
        self.Type = Type
        self.Name = None
        self.direction = 'right'
        self.isDrop = False # 아이템 드랍 관련 불값
        self.isDetect = False # 플레이어 발견 관련 불값
        self.atkcool = ENEMYATKCOOL
        
        static = [pygame.image.load('enemy_sprite/Seal_sprite/seal_static.png')]
        dead = [pygame.image.load('enemy_sprite/Seal_sprite/seal_dead.png')]
        walk = [pygame.image.load('enemy_sprite/Seal_sprite/seal_walk_' + str(i) + '.png') for i in range(1, 3)]
        attack = [pygame.image.load('enemy_sprite/Seal_sprite/seal_attack_' + str(i) + '.png') for i in range(1, 3)]
        getattack = [pygame.image.load('enemy_sprite/Seal_sprite/seal_get_attack.png')]
        
        self.spritelist = [static, walk, attack, getattack, dead]
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
        self.animation_time = round(100 / len(self.spritelist[self.cur] * 100), 2)
        
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
            
    def GetName(self):
        return self.Name
    
    def GetType(self):
        return self.Type
    

    def dropItem(self, Stage):
        '''
        아이템을 드롭시키는 함수, 나중에 확률에 따라 드랍시킬 생각
        '''
        trueDrop = random.choices(range(1, len(ItemTypes)), weights = [1, 1, 1, 1, 1])
        if (trueDrop.pop() >= 4):
            image = random.choice(ItemTypes)
            Stage.appendItem(ItemObject.ItemObject(self.x_pos, self.y_pos, image))
        
        if (self.Type == NORMAL):
            coindrops = random.randrange(1,3)
            for i in range(-coindrops, coindrops):
                Stage.appendItem(ItemObject.ItemObject(self.x_pos + i * 20, self.y_pos, COIN))
        elif (self.Type == BOSS):
            coindrops = random.randrange(3,9)
            for i in range(-coindrops, coindrops):
                Stage.appendItem(ItemObject.ItemObject(self.x_pos + i * 12, self.y_pos, COIN))
    
    def detectPlayer(self):
        '''
        플레이어를 감지하는 함수
        '''
        if (self.isDetect is False):
            self.effectStart = pygame.time.get_ticks()
        self.isDetect = True
        self.effectElapsed = (pygame.time.get_ticks() - self.effectStart) / 1000
        if (self.effectElapsed >= self.effectTime):
            self.effectStart = 0
            self.effectElapsed = 0
            
    def AI(self, Stage):
        '''
        기본적의 적의 AI
        플레이어에 상태에 따라서 업데이트가 된다
        '''
        pass
    
    def drawEffect(self):
        if (self.isDetect):
            if (self.effectElapsed != 0):
                self.system.GetScreen().blit(DETECTICON, (self.x_pos - 30, self.hitbox.top - 30))

    def drawStat(self):
        if (self.Type == NORMAL):
            Length = 125
            convertCoefficient = Length / self.MAXHP
            pygame.draw.rect(self.system.GetScreen(), self.system.GetColor('virginred'), (self.hitbox.centerx - Length / 2,
                                             self.hitbox.bottom + 18, Length, 12), 3)
            if (self.HP >= 0):
                pygame.draw.rect(self.system.GetScreen(), self.system.GetColor('red'), (self.hitbox.centerx - Length / 2,
                                               self.hitbox.bottom + 19, self.HP * convertCoefficient, 9))
        elif (self.Type == BOSS):
            Length = 300
            convertCoefficient = Length / self.MAXHP
            
    def updatePos(self, Stage):
        '''
        오브젝트의 위치를 업데이트 시키는 메서드
        '''
        PlayerDirection = Stage.GetPlayer().GetCondition('direction')
        PlayerSpeed = Stage.GetPlayer().GetStat('speed')
        
        self.hitbox.x = self.x_pos
        self.hitbox.bottom = self.y_pos

        if (self.isWalk and self.isAttack is False):
            if (self.direction == 'left'):
                self.x_pos += -self.SPEED
            elif (self.direction == 'right'):
                self.x_pos += self.SPEED
        
        if (Stage.XCameraMoveable and (Stage.isXCameraMove or Stage.forceXMove)):
            if (PlayerDirection == 'left'):
                self.x_pos += PlayerSpeed
            elif (PlayerDirection == 'right'):
                self.x_pos -= PlayerSpeed
        
        elif (not Stage.isXCameraMove and (self.x_pos <= self.system.GetXSize() and self.x_pos >= 0)):
            if (self.hitbox.left <= 0):
                self.x_pos = 0 #좌표 보정인데.... 오류라서
            if (self.hitbox.right >= self.system.GetXSize()):
                self.x_pos = self.system.GetXSize() - self.hitbox.width
                    
        if (not Stage.GetPlayer().GetCondition('onground')):
            if (Stage.GetPlayer().airSpace != 0):
                self.y_pos -= Stage.GetPlayer().airSpace
            else:
                self.y_pos -= Stage.GetPlayer().gravity
        else:
            self.y_pos = 465
            
    def updateSprite(self, dt):# 추후 아이템 획득시에도 스프라이트 관련 업데이트를 추가할 것
        '''
        적의 스프라이트를 업데이트 시켜주는 함수
        스프라이트 업데이트 지연까지 추가함
        '''
        super().updateSprite(dt)
        if (self.direction == 'left'):
            self.hitbox = self.cursprite.get_rect(bottomright=(self.x_pos + 70, self.y_pos)) #방향전환시 좌표오류를 잡아줌
        else:
            self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
            
    def update(self, dt, Stage):
        '''
        적의 업데이트 메서드
        첫번째 변수는 스프라이트 업데이트 주기 설정, 두번째 변수는 AI가 작동될 목표
        '''
        self.AI(Stage)
        super().update(dt, Stage)