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
        
        self.StageScore = 0
        self.TotalScore = 0
        
    def SetStage(self, level):
        self.PLAYER = PlayerAirCraft.PlayerAirCraft(360, 700)
        self.BOSS = BossAirCraft.BossAirCraft(1000000, 3000, 10, 100)

    def Draw(self):
        pass
        
    def UpdateBullets(self):
        for bullet in self.PLAYER.ProjectileList:
            if (bullet.GetPos('y') <= 0):
                self.PLAYER.ProjectileList.remove(bullet)
            for enemy in self.EnemyList:
                if (enemy.HitBox.CheckCollision(bullet.HitBox)):
                    self.PLAYER.ProjectileList.remove(bullet)
            bullet.Update()
            bullet.Draw()
            
        for enemy in self.EnemyList:
            for bullet in enemy.ProjectileList:
                if (self.PLAYER.HitBox.CheckCollision(bullet.HitBox)):
                    enemy.ProjectileList.remove(bullet)
                bullet.Update()
                bullet.Draw()
                
            if (enemy.removeable):
                self.EnemyList.remove(enemy)
        
        for bullet in self.BOSS.ProjectileList:
            if (self.PLAYER.HitBox.CheckCollision(bullet.HitBox)):
                enemy.ProjectileList.remove(bullet)
            bullet.Update()
            bullet.Draw()
            
        if (self.BOSS.removeable):
            del self.BOSS
    
    def UpdateScore(self):
        pass
    
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
            enemy.Draw()
        
        self.BOSS.Update(self.PLAYER, dt * 50)
        self.BOSS.Draw()
    
    def Update(self, dt):
        self.UpdateBullets()
        self.UpdateScore()
        self.UpdateItem()
        self.UpdateEnemy(dt)