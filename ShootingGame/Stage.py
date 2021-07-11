import Camera
import System
import PlayerAirCraft

class Stage(System.System):
    def __init__(self, Level, Score):
        super().__init__()
        self.Level = Level
        self.MAPSZIE = (600, 3200)
        self.Camera = Camera.Camera()
        
        self.PLAYER = None
        self.BulletList = []
        self.EnemyList = []
        self.ItemList = []
        
        self.StageScore = 0
        self.TotalScore = 0
        
    def SetStage(self, level):
        self.PLAYER = PlayerAirCraft.PlayerAirCraft(360, 700)
        
    def Draw(self):
        pass
        
    def UpdateBullets(self):
        for bullet in self.PLAYER.ProjectileList:
            if (bullet.GetPos('y') <= 0):
                self.PLAYER.ProjectileList.remove(bullet)
            bullet.Update()
            bullet.Draw()
            
        for bullet in self.BulletList:
            bullet.Update()
            bullet.Draw()
    
    def UpdateScore(self):
        pass
    
    def UpdateItem(self):
        pass
    
    def UpdateEnemy(self):
        pass
    
    def Update(self):
        self.UpdateBullets()
        self.UpdateScore()
        self.UpdateItem()
        self.UpdateEnemy()