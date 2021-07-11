import pygame
import System
import HitBox

LEFTUP = 'LEFTUP'

class AirCraft(System.System):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.pos = pygame.math.Vector2(x_pos, y_pos)
        
        self.ProjectileList = [] # 투사체를 관리하는 리스트
        self.isAttack = True
        self.isMove = False
        self.isDead = False
        self.isGetAttack = False
        self.Condition = None
        self.SpriteList = []
        self.cursprite = None
        self.direction = None
        
    def Move(self):
        self.isMove = True
        
    def Left(self):
        self.direction = 'LEFT'
        
    def Right(self):
        self.direction = 'RIGHT'
        
    def Up(self):
        self.direction = 'UP'
        
    def Down(self):
        self.direction = 'DOWN'
        
    def Static(self):
        self.isMove = False
        self.direction = None
        
    def GetAttack(self, Another):
        pass
    
    def DrawPos(self):
        self.GAMESCREEN.blit(self.cursprite, (self.pos.x, self.pos.y))
        
    def UpdatePos(self):
        pass