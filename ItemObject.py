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

class ItemObject(object):
    def __init__(self, x_pos, y_pos, image):
        '''
        아이템의 전체적인 정보를 저장하는 생성자
        '''
        self.x_pos = x_pos # 지속적으로 업데이트 되는 위치를 저장하는 변수
        self.y_pos = y_pos
        self.image = image # 이미지 파일 정보...(일단 임시임)
        self.icon = pygame.image.load(image)
        self.hitbox = self.icon.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
    def GetImage(self):
        '''
        아이템 아이콘 이미지를 반환하는 함수. 캐릭터의 아이템 획득 함수에 쓰임
        '''
        return self.image
    
    def draw(self):
        '''
        아이템을 그리는 함수
        '''
        Screen.blit(self.icon, (self.x_pos, self.hitbox.y))

    def checkcollision(self, Player):
        '''
        충돌판정 함수
        '''
        if (pygame.Rect.colliderect(self.hitbox, Player.hitbox)):
            return True
        else:
            return False
        
    def updatePos(self, Stage):
        PlayerCenterX = Stage.GetPlayer().GetPos(X) + Stage.GetPlayer().GetSize(WIDTH) / 2
        PlayerDirection = Stage.GetPlayer().GetCondition(DIRECTION)
        
        self.hitbox.x = self.x_pos
        self.hitbox.bottom = self.y_pos
        
        if ((Stage.XCameraMoveable and Stage.isXCameraMove) or Stage.forceXMove):
            if (PlayerCenterX <= CAMERAXMARGIN and PlayerDirection == LEFT):
                self.x_pos += Stage.GetPlayer().GetStat(SPEED)
            elif (PlayerCenterX >= CAMERAXMARGIN and PlayerDirection == RIGHT):
                self.x_pos += -Stage.GetPlayer().GetStat(SPEED)
                
        if (not Stage.GetPlayer().GetCondition(ONGROUND)):
            if (Stage.GetPlayer().airSpace != 0):
                self.y_pos -= AIRSPACE
            else:
                self.y_pos -= GRAVITY
        else:
            self.y_pos = MAP_GROUND