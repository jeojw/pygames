import pygame

class GameSystem(object):
    def __init__(self):
        self.Screen_x_size = 800
        self.Screen_y_size = 600
        self.XMARGIN = 200
        self.FPS = 60
        
        self.Clock = pygame.time.Clock()
        self.Screen = pygame.display.set_mode((self.Screen_x_size, self.Screen_y_size))
        self.BigFont = pygame.font.SysFont('notosanscjkkrblack', 70)
        self.SmallFont = pygame.font.SysFont('notosanscjkkrblack', 40)
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.VIRGINRED = (204, 0, 0)
        
    def GetClock(self):
        return self.Clock
    
    def GetScreen(self):
        return self.Screen
    
    def GetBigFont(self):
        return self.BigFont
    
    def GetSmallFont(self):
        return self.SmallFont
    
    def GetXSize(self):
        return self.Screen_x_size
    
    def GetYSize(self):
        return self.Screen_y_size
    
    def GetFPS(self):
        return self.FPS
    
    def GetColor(self, color):
        try:
            if (color == 'red'):
                return self.RED
            elif (color == 'blue'):
                return self.BLUE
            elif (color == 'green'):
                return self.GREEN
            elif (color == 'black'):
                return self.BLACK
            elif (color == 'white'):
                return self.WHITE
            elif (color == 'virginred'):
                return self.VIRGINRED
            else:
                raise ValueError
        except ValueError:
            print(color, 'is not Color!!!')
    
    def write(self, Font, Text, color, x_pos, y_pos):
        surface = Font.render(Text, True, color)
        rect = surface.get_rect()
        self.Screen.blit(surface, (x_pos, y_pos))