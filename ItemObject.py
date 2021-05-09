import main

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
                self.y_pos -= Stage.GetPlayer().airSpace
            else:
                self.y_pos -= Stage.GetPlayer().gravity
        else:
            self.y_pos = MAP_GROUND