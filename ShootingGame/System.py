import pygame

class System(object):
    def __init__(self):
        self.SCREENSIZE = (800, 1000)
        self.writeXMARGIN = 200
        self.writeYMARGIN = 200
        
        self.FPSCLOCK = pygame.time.Clock()
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
        surface = Font.render(Text, True, color)
        rect = surface.get_rect()
        self.GAMESCREEN.blit(surface, (x_pos, y_pos))