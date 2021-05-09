import main

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