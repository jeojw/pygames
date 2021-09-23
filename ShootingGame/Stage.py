import pygame
import Camera
import System
import Supply
import PlayerAirCraft
import EnemyAirCraft
import BossAirCraft

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
        self.SupplyType = None
        
        self.StageScore = 0
        self.TotalScore = 0
        
    def SetStage(self, level):
        self.PLAYER = PlayerAirCraft.PlayerAirCraft(360, 700)
        self.BOSS = BossAirCraft.BossAirCraft(1000000, 3000, 0, 0)
        self.ItemList.append(Supply.Supply('ATK', 200, 100))
        self.ItemList.append(Supply.Supply('ATK', 200, 200))
        self.ItemList.append(Supply.Supply('ATK', 200, 300))
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
        
        if (self.BOSS.CurPattern == 'LASER'):
            for laser in self.BOSS.LaserSprite:
                laser.Draw()
        
        for bullet in self.BOSS.ProjectileList:
            bullet.Draw()
            
        for item in self.ItemList:
            item.Draw()
        
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
        
        for bullet in self.BOSS.ProjectileList:
            if (bullet.GetPos('y') >= self.LIMITSIZE.y or 
                bullet.GetPos('x') <= 0 or
                bullet.GetPos('x') + bullet.HitBox.GetSize('w') >= self.LIMITSIZE.x):
                self.BOSS.ProjectileList.remove(bullet)
            if (self.PLAYER.HitBox.CheckCollision(bullet.HitBox)):
                self.BOSS.ProjectileList.remove(bullet)
            bullet.Update()
        
        if (self.BOSS.CurPattern == 'LASER'):
            for laser in self.BOSS.LaserSprite:
                laser.Update()
    
    def UpdateScore(self):
        self.InputText(self.BIGFONT, 'Score: ', self.COLORDIC['BLACK'], 720, 20)
        self.InputText(self.BIGFONT, str(self.TotalScore), self.COLORDIC['BLACK'], 880, 20)
    
    def UpdateItem(self):
        for item in self.ItemList:
            if (item.HitBox.CheckCollision(self.PLAYER.HitBox)):
                self.SupplyType = item.GetType()
                self.ItemList.remove(item)
                
            item.Update()
    
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