import pygame
import sys
import System
import Stage

sprite = pygame.image.load('ShootingGame/Sprite/AIRCRAFT_SAMPLE.png')

def rungame(Sys, Stage):
    while True:
        dt = Sys.FPSCLOCK.tick(Sys.FPS) / 1000
        
        Sys.GAMESCREEN.fill(Sys.COLORDIC['WHITE'])
        pygame.draw.rect(Sys.GAMESCREEN, Sys.COLORDIC['BLUE'], (700, 0, 300, 1000))
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN):
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
                    
            if (event.type == pygame.KEYUP):
                if (event.key == pygame.K_LEFT or
                    event.key == pygame.K_RIGHT or
                    event.key == pygame.K_UP or
                    event.key == pygame.K_DOWN):
                    Stage.PLAYER.Static()
                    
        Stage.PLAYER.Update(Stage)
        Stage.PLAYER.Draw()
        Stage.Update(dt)
        Stage.Draw()
        
        Sys.InputText(Sys.SMALLFONT, str(Stage.BOSS.LaserElapsed) + '  ' 
                      + str(Stage.BOSS.PatternQueue.size()) + '  ' 
                      + str(Stage.BOSS.NextPattern) + '  ' 
                      + str(Stage.BOSS.LCElapsed), Sys.COLORDIC['BLUE'], 30, 30)
        pygame.display.update()
        Sys.FPSCLOCK.tick(60)

def main():
    pygame.init()
    
    Sys = System.System()
    pygame.display.set_caption("Shooting Game")
    
    St = Stage.Stage(0, 0)
    St.SetStage(0)
    
    rungame(Sys, St)

if (__name__ == '__main__'):
    main()