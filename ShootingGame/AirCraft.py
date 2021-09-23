import pygame
import System
import Queue
import HitBox

samplesprite = pygame.image.load('ShootingGame/Sprite/AIRCRAFT_SAMPLE.png')

class AirCraft(System.System):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.pos = pygame.math.Vector2(x_pos, y_pos)
        
        self.ProjectileList = [] # 투사체를 관리하는 리스트
        self.isAttack = True
        self.isMove = False
        self.isDead = False
        self.isGetAttack = False #일단 보류...
        self.SpriteList = [samplesprite]
        self.index = 0
        self.HitBox = HitBox.HitBox(self.SpriteList[self.index], self.pos.x, self.pos.y)
        self.direction = None
        
        self.SizeQueue = Queue.Queue()
        
    def Move(self):
        if (not self.isDead):
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
    
    def DrawPos(self):
        self.GAMESCREEN.blit(self.SpriteList[self.index], (self.pos.x, self.pos.y))
        
    def UpdatePos(self):
        before = self.SizeQueue.dequeue()
        diffPos = pygame.math.Vector2(abs(self.SpriteList[self.index].get_width() - before[0]), abs(self.SpriteList[self.index].get_height() - before[1]))
        self.pos -= diffPos
        self.SizeQueue.enqueue(self.SpriteList[self.index].get_size())