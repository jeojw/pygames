import PlayerObject
import Seal
import SnowMan
import sys
import pygame

'''
맵 관련 변수
'''
XMARGIN = 200

'''
오브젝트 관련 변수
'''
SNOWBALLRANGE = 300

'''
아이템 아이콘, 이펙트 관련 변수
'''
ICEICON = pygame.image.load('Adventure/char_sprite/ice.png')
ARMORICON = pygame.image.load('Adventure/items/shield.png')
HASTEICON = pygame.image.load('Adventure/items/haste.png')
ATTACKSPEEDICON = pygame.image.load('Adventure/items/attackspeed.png')
HPRECOVERYICON = pygame.image.load('Adventure/items/hprecovery.png')
MAXHPUPICON = pygame.image.load('Adventure/items/hpmaxup.png')
COINICON = pygame.image.load('Adventure/items/coin.png')

# make enemylist!!!
stage_1_map = pygame.image.load('Adventure/map_images/stage_1_map.png')
stage_2_map = pygame.image.load('Adventure/map_images/stage_2_map.png')
maplist = [stage_1_map, stage_2_map]

class GameStage(object):
    '''
    해당 클래스는 게임 스테이지를 구현시켜주는 클래스로, 여기에서 스테이지 진행, 게임오버 화면, 클리어 화면, 오프닝, 카메라 뷰 등을 모두 다룸
    '''
    def __init__(self, system, stage, score):
        '''
        스테이지의 기본적인 시스템
        '''
        
        self.MAP_LIMIT_LEFT = 0
        self.MAP_LIMIT_RIGHT = 800
        self.MAP_GROUND = 465
        self.MAP_HEIGHT = 0
        self.CAMERAXMARGIN = 200
        self.CAMERAYMARGIN = 0
        
        self.map_x_size = 2400
        self.map_y_size = 1000
        
        self.system = system
        self.stage = stage # 스테이지 설정
        self.totalScore = score
        self.curScore = 0
        self.mapImages = [pygame.transform.scale(stage_map, (self.map_x_size, self.map_y_size))
                          for stage_map in maplist] # 스테이지 맵 이미지
        
        self.PLAYER = None # 스테이지 내에 그려질 플레이어
        self.ClearStage = False # 스테이지가 클리어 됬는지 아닌지 판별하는 불값
        self.GameOver = False
        self.XCameraMoveable = True # 카메라가 이동가능한 상태인지 설정시켜주는 불값
        self.isXCameraMove = False # 지금 카메라가 작동하고 있는지 판별시켜주는 불값
        self.forceXMove = False # 모든 적이 죽었르 경우 발동되는 불값
        self.isYCameraMove = False
        self.CameraDirection = 'left' # 카메라 방향
        self.Deadboollist = [] # 적 전체의 사망 판정을 관리하는 리스트
        self.Deadbooldic = {'Normal': list(),
                            'Boss': list()} #점수 차등 부여를 위한 딕셔너리 타입, 추후에 활용할 예정
        self.curDeadbool = [] # 현재 카메라가 비추는 영역에서의 적의 사망 판정으 관리하는 리스트
        self.CameraPos = [0, 0] # 카메라 위치
        
        self.clearCounts = 0
        
        self.Enemylist = []
        self.Itemlist = []
        self.EnemyProjectileList = []
        
        self.PlayerStat = [750, 750, 1000, 0, 10]
        self.EnemyStatdic = {'Seal': [2500, 2500, 0, 20, 4.5],
                            'SnowMan': [2000, 2000, 0, 0, 3],
                            'PolarBear': [4500, 4500, 180, 60, 3]}
        
    def GetMapSize(self, Type):
        '''
        맵 사이즈를 반환해주는 메서드
        '''
        try:
            if (Type == 'x'):
                return self.map_x_size
            elif (Type == 'y'):
                return self.map_y_size
            else:
                raise ValueError
        except ValueError:
            print(Type, 'is not size attribute!!!')
            
    def GetMapLimit(self, Type):
        '''
        보정 좌표를 반환해주는 메서드
        '''
        try:
            if (Type == 'left'):
                return self.MAP_LIMIT_LEFT
            elif (Type == 'right'):
                return self.MAP_LIMIT_RIGHT
            elif (Type == 'onground'):
                return self.MAP_GROUND
            else:
                raise ValueError
        except ValueError:
            print(Type, 'is not attribute!!')
        
    def GetPlayer(self):
        '''
        플레이어를 리턴시켜주는 메서드
        주로 플레이어의 정보를 필요로 하는 루프나 클래스에서 쓰임
        '''
        return self.PLAYER
    
    def GetCameraRange(self, pos):
        '''
        카메라 구동 범위를 반환해주는 메서드
        '''
        try:
            if (pos == 'x'):
                return self.CAMERAXMARGIN
            elif (pos == 'y'):
                return self.CAMERAYMARGIN
            else:
                raise ValueError
        except ValueError:
            print (pos, 'is not Pos!!!')
    
    def GetCameraView(self, pos):
        '''
        카메라뷰 위치를 리턴시켜주는 메서드
        '''
        try:
            if (pos == 'x'):
                return self.CameraPos[0]
            elif (pos == 'y'):
                return self.CameraPos[1]
            else:
                raise ValueError
        except ValueError:
            print(pos, 'is not Pos!!!')
            
    def GetStageCondition(self, condition):
        try:
            if (condition == 'clear'):
                return self.ClearStage
            elif (condition == 'gameover'):
                return self.GameOver
            else:
                raise ValueError
        except ValueError:
            print(condition, 'is not Condition variable!!!')
            
    def GetStageCount(self):
        return len(self.mapImages)
            
    def GetEnemylist(self):
        return self.Enemylist
    
    def GetItemlist(self):
        return self.Itemlist
    
    def GetEnemyProjectiles(self):
        return self.EnemyProjectileList
    
    def appendItem(self, Item):
        self.Itemlist.append(Item)
        
    def removeItem(self, Item):
        self.Itemlist.remove(Item)
        
    def appendProjectile(self, Proj):
        self.EnemyProjectileList.append(Proj)
    
    def removeProjectile(self, Proj):
        self.EnemyProjectileList.remove(Proj)
            
    def OpeningScreen(self):
        '''
        게임 오프닝을 보여주는 메서드
        '''
        while True:
            self.system.GetScreen().fill(self.system.GetColor('white'))
            self.system.write(self.system.GetBigFont(), 'Adventure', self.system.GetColor('black'), XMARGIN, 200)
            self.system.write(self.system.GetBigFont(), 'Press S!', self.system.GetColor('black'), XMARGIN, 350)
            pygame.display.update()
        
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()

                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_s):
                        return False
                    elif (event.type == pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
    
    def GameGuide(self):
        '''
        게임 가이드를 보여주는 메서드
        '''
        while True:
            self.system.GetScreen().fill(self.system.GetColor('white'))
            self.system.write(self.system.GetSmallFont(), 'MANUAL', self.system.GetColor('black'), XMARGIN, 30)
            self.system.write(self.system.GetSmallFont(), '<-, -> : LEFT, RIGHT MOVE', self.system.GetColor('black'), XMARGIN, 80)
            self.system.write(self.system.GetSmallFont(), '^ : JUMP', self.system.GetColor('black'), XMARGIN, 110)
            self.system.write(self.system.GetSmallFont(), 'x : ATTACK', self.system.GetColor('black'), XMARGIN, 140)
            self.system.write(self.system.GetSmallFont(), 'z : GETITEM', self.system.GetColor('black'), XMARGIN, 170)
            self.system.write(self.system.GetSmallFont(), 'ESC : GAME TERMINATE', self.system.GetColor('black'), XMARGIN, 200)
        
            self.system.GetScreen().blit(ICEICON, (XMARGIN, 240))
            self.system.write(self.system.GetSmallFont(), ': REINFORCE ATK', self.system.GetColor('black'), XMARGIN + 35, 240)
            self.system.GetScreen().blit(ARMORICON, (XMARGIN, 270))
            self.system.write(self.system.GetSmallFont(), ': REINFORCE DEF', self.system.GetColor('black'), XMARGIN + 35, 270)
            self.system.GetScreen().blit(HASTEICON, (XMARGIN, 300))
            self.system.write(self.system.GetSmallFont(), ': REINFORCE SPEED', self.system.GetColor('black'), XMARGIN + 35, 300)
            self.system.GetScreen().blit(ATTACKSPEEDICON, (XMARGIN, 330))
            self.system.write(self.system.GetSmallFont(), ': REINFORCE ATTACKSPEED', self.system.GetColor('black'), XMARGIN + 35, 330)
            self.system.GetScreen().blit(HPRECOVERYICON, (XMARGIN, 360))
            self.system.write(self.system.GetSmallFont(), ': RECOVERY HP', self.system.GetColor('black'), XMARGIN + 35, 360)
            self.system.GetScreen().blit(MAXHPUPICON, (XMARGIN, 390))
            self.system.write(self.system.GetSmallFont(), ': IMPROVE MAXHP AND RECOVERY HP', self.system.GetColor('black'), XMARGIN + 35, 390)
            
            self.system.write(self.system.GetSmallFont(), 'PRESS S!', self.system.GetColor('black'), XMARGIN, 500)
            pygame.draw.rect(self.system.GetScreen(), self.system.GetColor('black'), (0, 0, self.system.GetXSize(), self.system.GetYSize()), 5)
            pygame.display.update()
        
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_s):
                        return False
    
    def ClearScreen(self):
        '''
        스테이지 클리어시 나오는 화면
        '''
        self.clearCounts += 1
        self.system.write(self.system.GetBigFont(), 'Stage Clear!!!', self.system.GetColor('black'), XMARGIN, 200)
        if (len(self.mapImages) == self.clearCounts):
            self.system.write(self.system.GetBigFont(), 'Total Sclre: ' + str(self.totalScore + self.curScore), self.system.GetColor('black'), XMARGIN, 270)
        pygame.display.update()
        pygame.time.wait(1000)
            
    def GameoverScreen(self):
        '''
        플레이어의 HP가 전부 소진되고 적이 전원 사망하지 않을 시 나오는 화면
        '''
        self.system.write(self.system.GetBigFont(), 'GameOver!!!', self.system.GetColor('blue'), XMARGIN, 200)
        self.system.write(self.system.GetBigFont(), 'Try Again?', self.system.GetColor('blue'), XMARGIN, 280)
        self.system.write(self.system.GetBigFont(), 'Y / N', self.system.GetColor('blue'), XMARGIN, 360)
        pygame.display.update()
        pygame.time.wait(2000)
    
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_y):
                    self.ResetStage()
                    self.SetStage()
                elif (event.key == pygame.K_n):
                    pygame.quit()
                    sys.exit()
                elif (event.key is None):
                    pygame.quit()
                    sys.exit()
                    
    def ResultScreen(self):
        self.system.GetScreen().fill(self.system.GetColor('white'))
        self.system.write(self.system.GetBigFont(), 'Congratulation!!! Stage All Clear!!', self.system.GetColor('blue'), 20, 200)
        self.system.write(self.system.GetBigFont(), 'Total Score: ' + str(self.curScore + self.totalScore), self.system.GetColor('blue'), XMARGIN, 300)
        pygame.display.update()
        pygame.time.wait(1000)
                    
    def SetEnemy(self, EnemyList):
        for enemy in EnemyList:
            if (enemy.GetName() == 'Seal'):
                enemy.SetStat(*self.EnemyStatdic['Seal'])
            elif (enemy.GetName() == 'SnowMan'):
                enemy.SetStat(*self.EnemyStatdic['SnowMan'])
            self.Deadboollist.append(enemy.GetCondition('dead'))
              
    def SetStage(self):
        '''
        스테이지를 설정시켜주는 메서드
        주로 main()함수에서 쓰임
        '''
        if (self.stage == 1):
            self.PLAYER = PlayerObject.PlayerObject(self.system, 100)
            self.PLAYER.SetStat(*self.PlayerStat)
            
            self.Enemylist.append(SnowMan.SnowMan('Normal', self.system, 800))
            self.Enemylist.append(Seal.Seal('Normal', self.system, 500))
            self.Enemylist.append(Seal.Seal('Normal', self.system, 1500))
            self.Enemylist.append(SnowMan.SnowMan('Normal', self.system, 1800))
            self.SetEnemy(self.Enemylist)
                
        elif (self.stage == 2):
            self.PLAYER = PlayerObject.PlayerObject(self.system, 100)
            self.PLAYER.SetStat(*self.PlayerStat)
            
            self.Enemylist.append(Seal.Seal('Normal', self.system, 800))
            self.SetEnemy(self.Enemylist)
                
    def ResetStage(self):
        '''
        스테이지 재시도시 또는 스테이지 클리어 시 호출되는 메서드
        '''
        self.Enemylist.clear()
        self.Itemlist.clear()
        self.Deadboollist.clear()
        self.PLAYER.GetProjectiles().clear()
        self.EnemyProjectileList.clear()
        for enemy in self.Enemylist:
            self.Deadboollist.append(enemy.GetCondition('dead'))
        self.ClearStage = False
        self.GameOver = False
    
    def DrawStage(self):
        '''
        스테이지를 그려주는 메서드
        '''
        self.system.GetScreen().blit(self.mapImages[self.stage - 1], (0, self.system.GetYSize() - self.map_y_size), (self.CameraPos[0], self.CameraPos[1], self.map_x_size, self.map_y_size))
        self.system.write(self.system.GetSmallFont(), 'Scroe: ' + str(self.totalScore + self.curScore), self.system.GetColor('black'), 650, 25)
        
    def UpdateEnemy(self):
        '''
        적들이
        '''
        self.Deadboollist.clear()
        self.curDeadbool.clear()
        for enemy in self.Enemylist:
            self.Deadboollist.append(enemy.GetCondition('dead'))
            if (enemy.GetPos('x') >= 0 and enemy.GetPos('x') + enemy.GetSize('width') <= self.system.GetXSize()):
                self.curDeadbool.append(enemy.GetCondition('dead'))
                
        if (all(self.Deadboollist)):
            self.ClearStage = True
            
    def UpdateScore(self):
        '''
        스코어를 업데이트시켜주는 메서드
        스코어는 스테이지가 클리어 될수록 누적이 됨
        '''
        coinCoefficient = 50
        itemCoefficient = 100
        killCoefficient = 400
        bosskillCoefficient = 800
        stageclearCofficient = 1500
        
        coinscore = self.PLAYER.coincounts * coinCoefficient
        itemscore = self.PLAYER.itemcounts * itemCoefficient
        killscore = self.Deadboollist.count(True) * killCoefficient
        stageclearscore = self.clearCounts * stageclearCofficient
        
        self.curScore = coinscore + itemscore + killscore + stageclearscore
        
    def GetScore(self):
        return self.curScore
        
    def CameraXMovement(self, dx=0):
        '''
        카메라 이동을 관리하는 메서드
        '''
        self.CameraPos[0] += dx

    def CameraYMovement(self, dy=0):
        self.CameraPos[1] += dy
                
    def UpdateCamera(self):
        '''
        카메라의 위치를 업데이트시켜주는 메서드
        '''
        PlayerCenterX = self.PLAYER.GetPos('x') + self.PLAYER.GetSize('width') / 2
        PlayerCenterY = self.PLAYER.GetPos('y') + self.PLAYER.GetSize('height') / 2
        self.CameraDirection = self.PLAYER.GetCondition('direction')
            
        if (self.CameraPos[0] + self.system.GetXSize() >= self.map_x_size):
            self.CameraPos[0] = self.map_x_size - self.system.GetXSize()
            self.XCameraMoveable = False
            self.isXCameraMove = False
        elif (PlayerCenterX <= self.CAMERAXMARGIN and self.CameraPos[0] <= 0):
            self.CameraPos[0] = 0
            self.XCameraMoveable = False
            self.isXCameraMove = False
            
        for enemy in self.Enemylist:
            if (enemy.GetPos('x') <= self.system.GetXSize() - enemy.GetSize('width') and enemy.GetPos('x') >= 0):
                if (not all(self.curDeadbool)):
                    self.isXCameraMove = False
                    self.XCameraMoveable = False
                elif (all(self.curDeadbool) and (self.CameraPos[0] > 0 and self.CameraPos[0] < self.map_x_size - self.system.GetXSize())):
                    self.XCameraMoveable = True
                if (self.XCameraMoveable):
                    if (self.CameraDirection == 'left'):
                        if (PlayerCenterX - 10 > self.CAMERAXMARGIN):
                            self.forceXMove = True
                        else:
                            self.forceXMove = False
                    else:
                        if (PlayerCenterX > self.CAMERAXMARGIN):
                            self.forceXMove = True
                        else:
                            self.forceXMove = False
                else:
                    self.forceXMove = False
        if (self.XCameraMoveable or self.forceXMove):
            if (self.CameraDirection == 'left'):
                if (PlayerCenterX - 10 > self.CAMERAXMARGIN):
                    self.isXCameraMove = True
                else:
                    if (self.PLAYER.GetCondition('walk')):
                        self.isXCameraMove = True
                    else:
                        self.isXCameraMove = False
            else:
                if (PlayerCenterX > self.CAMERAXMARGIN):
                    self.isXCameraMove = True
                else:
                    if (self.PLAYER.GetCondition('walk')):
                        self.isXCameraMove = True
                    else:
                        self.isXCameraMove = False
        
        if (not self.XCameraMoveable):
            if (self.CameraPos[0] >= self.map_x_size - self.system.GetXSize()):
                if (PlayerCenterX < self.CAMERAXMARGIN):
                    self.XCameraMoveable = True
            elif (self.CameraPos[0] <= 0):
                if (PlayerCenterX > self.CAMERAXMARGIN):
                    self.XCameraMoveable = True
                    
        if (self.PLAYER.GetCondition('onground')):
            self.CameraPos[1] = 0
            
    def UpdateProjectile(self):
        '''
        투사체가 맵 밖으로 나갈 때 지우는 메서드
        '''
        PlayerProjectile = self.PLAYER.GetProjectiles()
        
        for projectile in PlayerProjectile:
            if (projectile.GetPos('x') <= self.MAP_LIMIT_LEFT or projectile.GetPos('x') + projectile.GetSize('width') >= self.MAP_LIMIT_RIGHT):
                PlayerProjectile.remove(projectile)
                
        for enemy in self.GetEnemylist():
            for projectile in enemy.GetProjectiles():
                if ((projectile.GetPos('x') <= self.MAP_LIMIT_LEFT or projectile.GetPos('x') + projectile.GetSize('width') >= self.MAP_LIMIT_RIGHT) or
                    abs(projectile.GetPos('x') - projectile.GetInitPos('x')) > SNOWBALLRANGE):
                    enemy.GetProjectiles().remove(projectile)
                    
    def UpdateStage(self):
        '''
        통합 업데이트 메서드
        '''
        self.UpdateCamera()
        self.UpdateEnemy()
        self.UpdateProjectile()
        self.UpdateScore()