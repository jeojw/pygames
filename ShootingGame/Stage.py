import pygame
import Camera
import System
import Supply
import PlayerAirCraft
import EnemyAirCraft
import BossAirCraft

'''
게임 스테이지를 설정해주는 클래스
주로 게임 화면 및 각 스테이지 난이도 구현을 지원하며, 각 오브젝트의 업데이트를 지원함
'''

tmpemap = pygame.image.load('ShootingGame/samplemap.png')
samplemap = pygame.transform.scale(tmpemap, (1000, 1000))
'''
BOSS = ★
MISSILE = ▼
NORMAL = ●
LASER = ▲
'''

class Stage(System.System):
    def __init__(self, Level, Score):
        super().__init__()
        self.Level = Level #게임 내 단계 설정
        self.MAPSIZE = (600, 3200) # 게임 맵 설정
        self.Camera = Camera.Camera() # 카메라, 배경에 따라 카메라가 움직이도록 설정
        
        self.PLAYER = None # 게임에 직접 참여하는 플레이어
        self.BOSS = None # 게임 보스
        self.EnemyList = [] # 보스 외의 적들을 담는 리스트
        self.ItemList = [] # 아이템을 담는 리스트
        self.SupplyType = None # 아이템 타입
        
        self.StageScore = 0 # 한 스테이지당 점수
        self.TotalScore = 0 # 총 점수
        
    def SetStage(self, level):
        '''
        레벨에 따라 난이도를 설정하는 메서드
        '''
        self.PLAYER = PlayerAirCraft.PlayerAirCraft(360, 700)
        self.BOSS = BossAirCraft.BossAirCraft(10000, 10000, 10000, -999999999999)
        self.EnemyList.append(EnemyAirCraft.MissileEnemy(1000, 1, 10, 300, 0))
        self.ItemList.append(Supply.Supply('ATK', 100, 100))
        self.ItemList.append(Supply.Supply('ATK', 100, 200))
        self.ItemList.append(Supply.Supply('ATK', 100, 300))
        
        '''
        추후 스테이지 설정할 때 이런식으로 할 예정
        if (level == 1):
            ReadStage = list()
            
            Stage_1 = open('ShootingGame/StageArray/Stage_1', 'r')
            lines = Stage_1.readlines()
            for line in lines:
                line = line.strip()
                ReadStage.append(list(line))
            Stage_1.close()
            
            for i in range(len(ReadStage)):
                for j in range(len(ReadStage[i])):
                    if (ReadStage[i][j] == '▼'):
                        self.EnemyList.append(EnemyAirCraft.MissileEnemy(1000, 1, 10, j * 20, i * 20))
                    elif (ReadStage[i][j] == '●'):
                        self.EnemyList.append(EnemyAirCraft.NormalEnemy(500, 1, 15, j * 20, i * 20))
                    elif (ReadStage[i][j] == '▲'):
                        pass
                    elif (ReadStage[i][j] == '★'):
                        self.BOSS = BossAirCraft.BossAirCraft(10000, 10000, 100, i * 20)
        '''
        
    def OpeningScreen(self):
        '''
        오프닝 화면
        '''
        pass
    
    def GameOverScreen(self):
        '''
        게임오버 화면
        '''
        pass
    
    def ShowScoreScreen(self):
        '''
        이때까지 획득한 총 점수를 확인시켜주는 화면
        '''
        pass
    
    def ShowScoreList(self):
        '''
        이때까지 기록했던 스코어들을 보여주는 메서드 추후 구현예정
        '''
        pass
    
    def RecordScore(self):
        '''
        게임 종료 시 스코어를 기록하는 메서드 추후 구현예정
        '''
        pass

    def Draw(self):
        '''
        스테이지를 그려주는 메서드
        '''
        self.DrawStage()
        self.DrawObject()
        
    def DrawStage(self):
        '''
        스테이지 배경화면을 그려주는 메서드
        '''
        self.GAMESCREEN.blit(samplemap, (0, 0))
    
    def DrawObject(self):
        '''
        오브젝트들을 그려주는 메서드
        '''
        for enemy in self.EnemyList:
            enemy.Draw()
            
        self.BOSS.Draw()
        
        for bullet in self.PLAYER.ProjectileList:
            bullet.Draw()
            if (bullet.Collide):
                bullet.DrawEffect()
            
        for enemy in self.EnemyList:
            for bullet in enemy.ProjectileList:
                bullet.Draw()
                if (bullet.Collide):
                    bullet.DrawEffect()
        
        if (self.BOSS.CurPattern == 'LASER'):
            for laser in self.BOSS.LaserSprite:
                laser.Draw()
                laser.DrawEffect()
        
        for bullet in self.BOSS.ProjectileList:
            bullet.Draw()
            if (bullet.Collide):
                bullet.DrawEffect()
            
        for item in self.ItemList:
            item.Draw()
        
    def UpdateBullets(self):
        '''
        각 오브젝트들이 생성하는 탄환을 그려주는 메서드
        '''
        for bullet in self.PLAYER.ProjectileList:
            if (bullet.GetPos('y') <= 0):
                self.PLAYER.ProjectileList.remove(bullet)
            for enemy in self.EnemyList:
                if (enemy.HitBox.CheckCollision(bullet.HitBox)):
                    enemy.GetAttack()
                    bullet.IsCollide(enemy)
                    if (not bullet.isExist):
                        self.PLAYER.ProjectileList.remove(bullet)
                    
            if (self.BOSS.HitBox.CheckCollision(bullet.HitBox)):
                self.BOSS.GetAttack()
                bullet.IsCollide(self.BOSS)
                if (not bullet.isExist):
                    self.PLAYER.ProjectileList.remove(bullet)
            bullet.Update()
            
        for enemy in self.EnemyList:
            for bullet in enemy.ProjectileList:
                if (bullet.GetPos('y') >= self.LIMITSIZE.y or 
                    bullet.GetPos('x') <= 0 or
                    bullet.GetPos('x') + bullet.HitBox.GetSize('w') >= self.LIMITSIZE.x):
                    enemy.ProjectileList.remove(bullet)
                if (self.PLAYER.HitBox.CheckCollision(bullet.HitBox)):
                    self.PLAYER.GetAttack()
                    bullet.IsCollide(self.PLAYER)
                    if (not bullet.isExist):
                        enemy.ProjectileList.remove(bullet)
                bullet.Update()
        
        for bullet in self.BOSS.ProjectileList:
            if (bullet.GetPos('y') >= self.LIMITSIZE.y or 
                bullet.GetPos('x') <= 0 or
                bullet.GetPos('x') + bullet.HitBox.GetSize('w') >= self.LIMITSIZE.x):
                self.BOSS.ProjectileList.remove(bullet)
            if (self.PLAYER.HitBox.CheckCollision(bullet.HitBox)):
                self.PLAYER.GetAttack()
                bullet.IsCollide(self.PLAYER)
                if (not bullet.isExist):
                    self.PLAYER.ProjectileList.remove(bullet)
            bullet.Update()
        
        if (self.BOSS.CurPattern == 'LASER'):
            for laser in self.BOSS.LaserSprite:
                laser.Update()
    
    def UpdateScore(self):
        '''
        점수를 업데이트시켜주는 메서드
        '''
        self.InputText(self.BIGFONT, 'Score: ', self.COLORDIC['BLACK'], 720, 20)
        self.InputText(self.BIGFONT, str(self.TotalScore), self.COLORDIC['BLACK'], 880, 20)
    
    def UpdateItem(self):
        '''
        아이템의 위치를 업데이트시켜주는 메서드
        '''
        for item in self.ItemList:
            if (item.HitBox.CheckCollision(self.PLAYER.HitBox)):
                self.SupplyType = item.GetType()
                self.ItemList.remove(item)
                
            item.Update()
    
    def UpdateEnemy(self, dt):
        '''
        일반 적 및 보스를 업데이트시켜주는 메서드
        '''
        for enemy in self.EnemyList:
            if (enemy.removeable):
                self.EnemyList.remove(enemy)
                
            enemy.Update(self.PLAYER)
        
        self.BOSS.Update(self.PLAYER, dt * 50)
        
        if (self.BOSS.removeable):
            del self.BOSS
    
    def Update(self, dt):
        '''
        총 업데이트 메서드
        '''
        self.UpdateBullets()
        self.UpdateScore()
        self.UpdateItem()
        self.UpdateEnemy(dt)