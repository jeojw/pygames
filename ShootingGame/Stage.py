import pygame
import Camera
import System
import Supply
import PlayerAirCraft
import EnemyAirCraft
import BossAirCraft

class SpriteSort(pygame.sprite.Group):
    def __init__(self):
        pass
    
    def draw(self):
        pass

class Stage(System.System):
    def __init__(self, Level, Score):
        super().__init__()
        self.Level = Level
        self.MAPSZIE = (600, 3200)
        self.Camera = Camera.Camera()
        
        self.PLAYER = None
        self.BOSS = None
        self.EnemyList = []
        self.ItemList = []
        
        self.StageScore = 0
        self.TotalScore = 0
        
    def SetStage(self, level):
        self.PLAYER = PlayerAirCraft.PlayerAirCraft(360, 700)
        self.BOSS = BossAirCraft.BossAirCraft(1000000, 3000, 0, 0)
        
    def OpeningScreen(self):
        pass
    
    def GameOverScreen(self):
        pass
    
    def ShowScoreScreen(self):
        pass

    def Draw(self):
        self.DrawObject()
    
    def DrawObject(self):
        for enemy in self.EnemyList:
            enemy.Draw()
            
        self.BOSS.Draw()
        
        for bullet in self.PLAYER.ProjectileList:
            bullet.Draw()
            
        for enemy in self.EnemyList:
            for bullet in enemy.ProjectileList:
                bullet.Draw()
    
        for bullet in self.BOSS.ProjectileList:
            bullet.Draw()
        
    def UpdateBullets(self):
        for bullet in self.PLAYER.ProjectileList:
            if (bullet.GetPos('y') <= 0):
                self.PLAYER.ProjectileList.remove(bullet)
            for enemy in self.EnemyList:
                if (enemy.HitBox.CheckCollision(bullet.HitBox)):
                    self.PLAYER.ProjectileList.remove(bullet)
            bullet.Update()
            
        for enemy in self.EnemyList:
            for bullet in enemy.ProjectileList:
                if (bullet.GetPos('y') >= self.LIMITSIZE.y or 
                    bullet.GetPos('x') <= 0 or
                    bullet.GetPos('x') + bullet.HitBox.GetSize('w') >= self.LIMITSIZE.x):
                    enemy.ProjectileList.remove(bullet)
                if (self.PLAYER.HitBox.CheckCollision(bullet.HitBox)):
                    enemy.ProjectileList.remove(bullet)
                bullet.Update()
                
            if (enemy.removeable):
                self.EnemyList.remove(enemy)
        
        if (self.BOSS.CurPattern != 'LASER'):
            for bullet in self.BOSS.ProjectileList:
                if (bullet.GetPos('y') >= self.LIMITSIZE.y or 
                    bullet.GetPos('x') <= 0 or
                    bullet.GetPos('x') + bullet.HitBox.GetSize('w') >= self.LIMITSIZE.x):
                    self.BOSS.ProjectileList.remove(bullet)
                if (self.PLAYER.HitBox.CheckCollision(bullet.HitBox)):
                    self.BOSS.ProjectileList.remove(bullet)
                bullet.Update()
        
        else:
            for bullet in self.BOSS.ProjectileList:
                bullet.Update()
    
    def UpdateScore(self):
        self.InputText(self.BIGFONT, 'Score: ', self.COLORDIC['BLACK'], 720, 20)
        self.InputText(self.BIGFONT, str(self.TotalScore), self.COLORDIC['BLACK'], 880, 20)
    
    def UpdateItem(self):
        for item in self.ItemList:
            '''
            if (item.HitBox.CheckCollision(self.PLAYER.HitBox)):
                self.ItemList.remove(item)
            '''
            item.Update()
            item.Draw()
    
    def UpdateEnemy(self, dt):
        for enemy in self.EnemyList:
            enemy.Update(self.PLAYER)
        
        self.BOSS.Update(self.PLAYER, dt * 50)
        
        if (self.BOSS.removeable):
            del self.BOSS
    
    def Update(self, dt):
        self.UpdateBullets()
        self.UpdateScore()
        self.UpdateItem()
        self.UpdateEnemy(dt)