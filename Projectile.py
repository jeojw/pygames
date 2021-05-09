import main
import pygame

pygame.init() # pygame 초기화

'''
맵 관련 변수
'''
MAP_GROUND = 465
MAP_HEIGHT = 0
MAP_LIMIT_LEFT = 0
MAP_LIMIT_RIGHT = 800
XMARGIN = 200
YMARGIN = 0

CAMERAXMARGIN = 250
CAMERAYMARGIN = 200

JUMPDISTANCE = 80
AIRSPACE = -10
GRAVITY = 10
DURATION = 20
AMMUNITION = 30

'''
오브젝트 관련 변수
'''
PLAYERATKCOOL = 1
ENEMYATKCOOL = 1

SEALATTACKRANGE = 75
SNOWMANATTACKDISTANCE = 200
SNOWBALLRANGE = 300
PLYAERRANGE = 300
POLARBEARATTACKRANGE = 0

'''
오브젝트의 스텟 관련 변수
'''
MAXHP = 'maxhp'
HP = 'hp'
ATK = 'atk'
DEF = 'def'
SPEED = 'speed'

'''
오브젝트의 컨디션 관련 전역변수
'''
LEFT = 'left'
RIGHT = 'right'
DIRECTION = 'direction'
STATIC = 'static'
WALK = 'walk'
ATTACK = 'attack'
GETATTACK = 'getattack'
DEAD = 'dead'
HITBOX = 'hitbox'
ATKHITBOX = 'atkhitbox'
ONGROUND = 'onground'

'''
히트박스 사이즈 및 위치 전역변수
'''
X = 'x'
Y = 'y'
WIDTH = 'width'
HEIGHT = 'height'

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

BASIC = 'char_sprite/bubble.png'
REINFORCE = 'char_sprite/ice.png'

SNOWBALL = 'enemy_sprite/SnowMan_sprite/snowball.png'

ICEICON = pygame.image.load(ICE)
ARMORICON = pygame.image.load(ARMOR)
HASTEICON = pygame.image.load(HASTE)
ATTACKSPEEDICON = pygame.image.load(ATTACKSPEED)
HPRECOVERYICON = pygame.image.load(HPRECOVERY)
MAXHPUPICON = pygame.image.load(MAXHPUP)
COINICON = pygame.image.load(COIN)

DETECTICON = pygame.image.load('effect_icon/detectIcon.png')

'''
오브젝트 관련 리스트 및 변수 -> 이 리스트들을 GameStage 클래스 내부에 조만간 편입시켜야 할듯.
'''
Enemylist = [] # 화면에 그릴 적 리스트
ItemTypes = [ICE, ARMOR, HASTE, ATTACKSPEED, HPRECOVERY, MAXHPUP] # 아이템 타입, 주로 스프라이트 파일로 통해 아이템 획득을 구분할 예정
Itemlist = [] # 아이템을 담는 리스트
ProjectileList = []

'''
기본적인 스텟 함수
'''
PlayerStat = [750, 750, 1000, 0, 10]
EnemyStatdic = {'Seal': [2500, 2500, 80, 20, 4.5],
                'SnowMan': [2000, 2000, 120, 0, 3],
                'PolarBear': [4500, 4500, 180, 60, 3]}

'''
적 타입 및 이름을 나타내는 변수
'''
NORMAL = 'Normal'
BOSS = 'Boss'

SEAL = 'Seal'
SNOWMAN = 'SnowMan'
POLARBEAR = 'PolarBear'

'''
아이템 획득 시 스텟 변환 리스트
'''
ICEStat = [0, 0, 100, 0, 0, 1]
ARMORStat = [0, 0, 0, 20, 0, 1]
HASTEStat = [0, 0, 0, 0, 5, 1]
ATTACKSPEEDStat = [0, 0, 0, 0, 0, 1.5]
MAXHPUPStat = [250, 0, 0, 0, 0, 1]

'''
텍스트 작성 함수
'''
Font = pygame.font.SysFont('굴림', 40)

def write(Font, Text, color, x_pos, y_pos):
    surface = Font.render(Text, True, color)
    rect = surface.get_rect()
    Screen.blit(surface, (x_pos, y_pos))

'''
기본적인 색상
'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
VIRGINRED = (204, 0, 0)

'''
기본적인 시스템 변수 설정
'''
x_size = 800
y_size = 600
FPS = 60

map_x_size = 2400
map_y_size = 1000

# make enemylist!!!
stage_1_map = pygame.image.load('map_images/stage_1_map.png')
stage_2_map = pygame.image.load('map_images/stage_2_map.png')
stage_1_scale = pygame.transform.scale(stage_1_map, (map_x_size, map_y_size))
stage_2_scale = pygame.transform.scale(stage_2_map, (map_x_size, map_y_size))

Clock = pygame.time.Clock()
Screen = pygame.display.set_mode((x_size, y_size))
BigFont = pygame.font.SysFont('notosanscjkkrblack', 70)
SmallFont = pygame.font.SysFont('notosanscjkkrblack', 40)


class Projectile(object):
    '''
    해당 클래스는 투사체의 기본적인 틀을 정해놓았다. 기본적으로는 버블임
    '''
    def __init__(self, image, x_pos, y_pos, ATK, direction):
        '''
        생성자에서 위치, 스텟, 방향, 이미지, 히트박스 설정을 관리함
        '''
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.init_x_pos = x_pos
        self.init_y_pos = y_pos
        self.ATK = ATK
        self.SPEED = 7
        self.direction = direction
        tmpimage = pygame.image.load(image)
        self.image = pygame.transform.scale(tmpimage, (30, 30))
        self.hitbox = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        
    def SetStat(self, ATK, SPEED):
        '''
        투사체의 스텟 설정
        '''
        self.ATK = ATK
        self.SPEED = SPEED
        
    def GetPos(self, pos):
        try:
            if (pos == 'x'):
                return self.x_pos
            elif (pos == 'y'):
                return self.y_pos
            else:
                raise ValueError
        except ValueError:
            print('Not Pos!!!!')
            
    def GetInitPos(self, pos):
        try:
            if (pos == 'x'):
                return self.init_x_pos
            elif (pos == 'y'):
                return self.init_y_pos
            else:
                raise ValueError
        except ValueError:
            print('Not Pos!!!!')

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
            print('Not Lenght!!!')
        
    def draw(self):
        '''
        스크린에다가 투사체를 그려넣음
        '''
        Screen.blit(self.image, (self.x_pos, self.y_pos))

    def checkcollision(self, enemy):
        '''
        충돌 판정
        '''
        if (pygame.Rect.colliderect(self.hitbox, enemy.hitbox)):
            return True
        else:
            return False
        
    def updatePos(self, Stage):
        '''
        투사체가 자동으로 움직이도록 하는 메서드
        업데이트까지 겸함
        '''
        PlayerOnGround = Stage.GetPlayer().GetCondition(ONGROUND)
        AirSpace = Stage.GetPlayer().airSpace
        Gravity = Stage.GetPlayer().gravity
        
        if (self.direction == LEFT):
            self.x_pos += -self.SPEED
        else:
            self.x_pos += self.SPEED
            
        if (not PlayerOnGround):
            if (AirSpace != 0):
                self.y_pos -= AirSpace
            else:
                self.y_pos -= Gravity
                
        self.hitbox.x = self.x_pos
        self.hitbox.y = self.y_pos