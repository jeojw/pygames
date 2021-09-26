import System
import pygame

'''
게임 오브젝트의 히트박스를 다루는 모듈
이 모듈로 통해서 오브젝트간의 충돌을 다룸
'''

class HitBox(System.System):
    def __init__(self, Sprite, x_pos, y_pos):
        super().__init__()
        self.pos = pygame.math.Vector2(x_pos, y_pos) #히트박스 위치
        self.Object = Sprite.get_rect(topleft=(x_pos, y_pos)) #히트박스 객체
        self.Collidable = True #충돌 가능 유무
        
    def Draw(self):
        pygame.draw.rect(self.GAMESCREEN, (255, 0, 0), [self.Object.x, self.Object.y, self.Object.width, self.Object.height], 2)
        
    def GetPos(self, t, center=None):
        '''
        히트박스 위치 반환 메서드
        center 유무로 중앙값, 원래값 반환
        '''
        try:
            if (t == 'x'):
                if (center is not None):
                    return self.Object.centerx
                else:
                    return self.pos.x
            elif (t == 'y'):
                 if (center is not None):
                    return self.Object.centery
                 else:
                    return self.pos.y
            else:
                raise ValueError
        except ValueError:
            return -1
    
    def GetSize(self, t=None):
        '''
        히트박스 크기 반환 메서드
        t에 따라 반환값 다르게 설정
        '''
        try:
            if (t == 'w'):
                return self.Object.width
            elif (t == 'h'):
                return self.Object.height
            elif (t is None):
                return (self.Object.width, self.Object.height)
            else:
                raise ValueError
        except ValueError:
            return -1
        
    def CheckCollision(self, Another):
        '''
        히트박스끼리 충돌 유무 조사
        '''
        if (self.Collidable):
            return pygame.Rect.colliderect(self.Object, Another.Object)
    
    def UpdateSize(self, newSprite):
        '''
        히트박스 크기 업데이트 메서드
        '''
        self.Object = newSprite.get_rect(topleft=(self.pos.x, self.pos.y))
    
    def UpdatePos(self, x_pos, y_pos, spritesize=None):
        '''
        히트박스 위치 업데이트 메서드
        현 스프라이트 사이즈와 히트박스 사이즈가 다를 경우, 히트박스 위치가 조정되도록 설정
        '''
        self.pos = pygame.math.Vector2(x_pos, y_pos)
        if (spritesize is not None):
            if (spritesize.get_size() != (self.Object.width, self.Object.height)):
                diffsize = pygame.math.Vector2(spritesize.get_width() - self.Object.width, spritesize.get_height() - self.Object.height)
                self.pos = pygame.math.Vector2(self.pos.x + diffsize.x / 2, self.pos.y + diffsize.y / 2)
        self.Object.topleft = (self.pos.x, self.pos.y)