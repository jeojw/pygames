import pygame

'''
모든 오브젝트에 적용되는 파이게임의 시스템을 한데 모은 모듈
이 모듈은 다른 모든 클래스로 상속이 됨
'''

class System(object):
    def __init__(self):
        self.SCREENSIZE = (1000, 1000) # 창 사이즈
        self.writeXMARGIN = 200 
        self.writeYMARGIN = 200
        self.LIMITSIZE = pygame.math.Vector2(700, 1000) # 게임 스크린 사이즈
        
        self.FPSCLOCK = pygame.time.Clock() #fps 시계
        self.GAMESCREEN = pygame.display.set_mode(self.SCREENSIZE)
        self.BIGFONT = pygame.font.SysFont('notosanscjkkrblack', 70)
        self.SMALLFONT = pygame.font.SysFont('notosanscjkkrblack', 40)
        self.FPS = 60
        
        self.COLORDIC = {'BLACK': (0, 0, 0),
                         'WHITE': (255, 255, 255),
                         'RED': (255, 0, 0),
                         'GREEN': (0, 255, 0),
                         'BLUE': (0, 0, 255)}
    
    def InputText(self, Font, Text, color, x_pos, y_pos):
        '''
        스크린 내에 텍스트를 집어넣는 함수
        '''
        surface = Font.render(Text, True, color)
        rect = surface.get_rect()
        self.GAMESCREEN.blit(surface, (x_pos, y_pos))