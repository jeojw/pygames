import GameSystem
import pygame


'''
차후 변수 관련해서 반드시 수정할 것!!
'''
pygame.init() # pygame 초기화

'''
아이템 아이콘, 이펙트 관련 변수
'''
ICE = 'char_sprite/ice.png'
ARMOR = 'items/shield.png'
HASTE = 'items/haste.png'
ATTACKSPEED = 'items/attackspeed.png'
HPRECOVERY = 'items/hprecovery.png'
MAXHPUP = 'items/hpmaxup.png'

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
        
        self.StatDic = {'ice': [0, 0, 100, 0, 0, 1],
                        'armor': [0, 0, 0, 20, 0, 1],
                        'haste': [0, 0, 0, 0, 5, 1],
                        'attackspeed': [0, 0, 0, 0, 0, 1.5],
                        'maxhpup': [250, 0, 0, 0, 0, 1]}
        
    def GetImage(self):
        '''
        아이템 아이콘 이미지를 반환하는 함수. 캐릭터의 아이템 획득 함수에 쓰임
        '''
        return self.image
    
    def GetStat(self, Image):
        try:
            if (Image == ICE):
                return self.StatDic['ice']
            elif (Image == ARMOR):
                return self.StatDic['armor']
            elif (Image == HASTE):
                return self.StatDic['haste']
            elif (Image == ATTACKSPEED):
                return self.StatDic['attackspeed']
            elif (Image == MAXHPUP):
                return self.StatDic['maxhpup']
            else:
                raise ValueError
        except ValueError:
            print(Image, 'is not Item Image!!!')
    
    def draw(self, System):
        '''
        아이템을 그리는 함수
        '''
        System.GetScreen().blit(self.icon, (self.x_pos, self.hitbox.y))

    def checkcollision(self, Player):
        '''
        충돌판정 함수
        '''
        if (pygame.Rect.colliderect(self.hitbox, Player.hitbox)):
            return True
        else:
            return False
        
    def updatePos(self, Stage):
        PlayerCenterX = Stage.GetPlayer().GetPos('x') + Stage.GetPlayer().GetSize('width') / 2
        PlayerDirection = Stage.GetPlayer().GetCondition('direction')
        
        self.hitbox.x = self.x_pos
        self.hitbox.bottom = self.y_pos
        
        if ((Stage.XCameraMoveable and Stage.isXCameraMove) or Stage.forceXMove):
            if (PlayerCenterX <= Stage.CAMERAXMARGIN and PlayerDirection == 'left'): ##체크
                self.x_pos += Stage.GetPlayer().GetStat('speed')
            elif (PlayerCenterX >= Stage.CAMERAXMARGIN and PlayerDirection == 'right'): ##체크
                self.x_pos += -Stage.GetPlayer().GetStat('speed')
                
        if (not Stage.GetPlayer().GetCondition('onground')):
            if (Stage.GetPlayer().airSpace != 0):
                self.y_pos -= Stage.GetPlayer().airSpace ##체크
            else:
                self.y_pos -= Stage.GetPlayer().gravity ##체크
        else:
            self.y_pos = Stage.MAP_GROUND ##체크