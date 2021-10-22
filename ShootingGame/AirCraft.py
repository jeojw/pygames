import pygame
import System
import Queue
import HitBox
'''
비행체의 기초를 구현한 클래스
'''
samplesprite = pygame.image.load('ShootingGame/Sprite/Player_Sprite_1.png')

class AirCraft(System.System):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.pos = pygame.math.Vector2(x_pos, y_pos) # 위치0
        
        self.ProjectileList = [] # 투사체를 관리하는 리스트
        self.isAttack = True # 공격 가능 유무를 설정하는 변수
        self.isMove = False # 이동의 유무를 설정하는 변수
        self.isDead = False # 사망 여부를 설정하는 변수
        self.isGetAttack = False #일단 보류...
        self.SpriteList = [samplesprite] # 스프라이트 리스트
        self.index = 0 # 스프라이트 인덱스
        self.CurSprite = self.SpriteList[self.index]
        self.HitBox = HitBox.HitBox(self.SpriteList[self.index], self.pos.x, self.pos.y) # 히트박스 설정
        self.direction = None # 방향
        
        self.SizeQueue = Queue.Queue() # 스프라이트 사이즈 큐, 이걸로 스프라이트 크기 변화에 따라 위치를 조정함
        
    def Move(self):
        '''
        이동 메서드
        '''
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
        
    def GetAttack(self):
        self.isGetAttack = True
        
    def NotGetAttack(self):
        self.isGetAttack = False
    
    def DrawPos(self):
        '''
        오브젝트의 위치를 나타내주는 메서드
        '''
        self.GAMESCREEN.blit(self.CurSprite, (self.pos.x, self.pos.y))
        
    def UpdatePos(self):
        '''
        오브젝트의 위치를 업데이트시켜주는 메서드
        이 메서드는 위치조정을 주로 맡고, 나머지는 자식 클래스에서 새로 설정하도록 함
        '''
        before = self.SizeQueue.dequeue()
        diffPos = pygame.math.Vector2(abs(self.SpriteList[self.index].get_width() - before[0]) / 2, abs(self.SpriteList[self.index].get_height() - before[1]) / 2)
        self.pos -= diffPos
        self.SizeQueue.enqueue(self.SpriteList[self.index].get_size())