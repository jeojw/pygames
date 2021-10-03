import pygame
import sys
import System
import Stage

def rungame(Sys, Stage):
    while True:
        dt = Sys.FPSCLOCK.tick(Sys.FPS) / 1000
        
        Sys.GAMESCREEN.fill(Sys.COLORDIC['WHITE'])
        pygame.draw.rect(Sys.GAMESCREEN, Sys.COLORDIC['BLUE'], (700, 0, 300, 1000))
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    Stage.PLAYER.Left()
                    Stage.PLAYER.Move()
                elif (event.key == pygame.K_RIGHT):
                    Stage.PLAYER.Right()
                    Stage.PLAYER.Move()
                elif (event.key == pygame.K_UP):
                    Stage.PLAYER.Up()
                    Stage.PLAYER.Move()
                elif (event.key == pygame.K_DOWN):
                    Stage.PLAYER.Down()
                    Stage.PLAYER.Move()
                elif (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                    
            elif (event.type == pygame.KEYUP):
                if (event.key == pygame.K_LEFT or
                    event.key == pygame.K_RIGHT or
                    event.key == pygame.K_UP or
                    event.key == pygame.K_DOWN):
                    Stage.PLAYER.Static()
                    
        Stage.Update(dt) # 순서에 따라 출력하는 결과가 다르다.. 왤까
        Stage.PLAYER.Update(Stage)
        Stage.Draw()
        Stage.PLAYER.Draw()
        
        Sys.InputText(Sys.SMALLFONT, str(Stage.BOSS.SCElapsed) + '  ' 
                      + str(Stage.BOSS.CoolElapsed) + '  ' 
                      + str(Stage.BOSS.LaserElapsed) + '  ' 
                      + str(Stage.PLAYER.pos) + '  '
                      + str('xx') + '  '
                      + str(Stage.EnemyList[0].MissileShoot), Sys.COLORDIC['BLUE'], 30, 30)
        pygame.display.flip()
        Sys.FPSCLOCK.tick(Sys.FPS)

def main():
    pygame.init()
    
    Sys = System.System()
    pygame.display.set_caption("Shooting Game")
    
    St = Stage.Stage(0, 0)
    St.SetStage(0)
    
    rungame(Sys, St)

if (__name__ == '__main__'):
    main()