import pygame
import sys
import GameStage
import GameSystem

'''
맵 관련 변수
'''
MAP_GROUND = 465
MAP_HEIGHT = 0
MAP_LIMIT_LEFT = 0
MAP_LIMIT_RIGHT = 800

def rungame(System, Stage):
    while True:
        dt = System.GetClock().tick(System.GetFPS()) / 1000 # 스프라이트 업데이트 주기 함수
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    Stage.GetPlayer().leftwalk()
                elif (event.key == pygame.K_RIGHT):
                    Stage.GetPlayer().rightwalk()
                elif (event.key == pygame.K_UP):
                    Stage.GetPlayer().jump()
                elif (event.key == pygame.K_x):
                    Stage.GetPlayer().attack()
                elif (event.key == pygame.K_z): #아이템 획득 키
                    Stage.GetPlayer().getItem(Stage)
                elif (event.key == pygame.K_g):
                    pass
                elif (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            elif (event.type == pygame.KEYUP):
                if (event.key == pygame.K_LEFT or
                    event.key == pygame.K_RIGHT or
                    event.key == pygame.K_x):
                    if (not Stage.GetPlayer().GetCondition('dead')):
                        Stage.GetPlayer().static()
                    else:
                        Stage.GetPlayer().dead()
        
        Stage.UpdateStage()
        Stage.DrawStage() #?
        Stage.GetPlayer().update(1, Stage) #?
        Stage.GetPlayer().draw() #? #?
        if (len(Stage.GetPlayer().GetProjectiles()) != 0):
            for projectile in Stage.GetPlayer().GetProjectiles():
                projectile.updatePos(Stage)
                projectile.draw(System)
            
        for enemy in Stage.GetEnemylist():
            if (len(Stage.GetEnemylist()) != 0):
                if (len(enemy.GetProjectiles()) != 0):
                    for projectile in enemy.GetProjectiles():
                        projectile.updatePos(Stage)
                        projectile.draw(System)
                enemy.update(dt * 15, Stage)
                enemy.draw()
                
        for item in Stage.GetItemlist():
            if (len(Stage.GetItemlist()) != 0):
                item.updatePos(Stage)
                item.draw(System)
        
        if (Stage.GetPlayer().GetCondition('dead')):
            Stage.GameOver = True
            return False
        
        if (Stage.GetStageCondition('clear')):
            Stage.ClearScreen()
            return False

        System.write(System.GetSmallFont(), str(Stage.GetPlayer().isGetattack) + '   ' + 
                     str(Stage.GetEnemylist()[1].Attackable), System.GetColor('black'), 350, 20)
        pygame.display.update()
        System.GetClock().tick(System.GetFPS())
        
def main():
    pygame.init()
    
    System = GameSystem.GameSystem()
    pygame.display.set_caption("Adventure")
    
    level = 1
    score = 0
    while True:
        Stage = GameStage.GameStage(System, level, score)
        Stage.SetStage()
        if (level == 1):
            Stage.OpeningScreen()
            Stage.GameGuide()
        while True:
            rungame(System, Stage)
            if (Stage.GetStageCondition('clear')): ## change
                if (level == Stage.GetStageCount()): ## change
                    Stage.ResultScreen()
                    level = 1
                    break
                level += 1
                score += Stage.GetScore()
                Stage.ResetStage()
                break
            if (Stage.GetStageCondition('gameover')):
                Stage.GameoverScreen()
                
            
    
if (__name__ == '__main__'):
    main()