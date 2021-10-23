import pygame
import sys
import System
import Stage

def rungame(Sys, Stage):
    while True:
        dt = Sys.FPSCLOCK.tick(Sys.FPS) / 1000
        
        Sys.GAMESCREEN.fill(Sys.COLORDIC['WHITE'])
        pygame.draw.rect(Sys.GAMESCREEN, Sys.COLORDIC['BLUE'], (700, 0, 300, 1000))
        
        KEYS = pygame.key.get_pressed()
        
        if (KEYS[pygame.K_LEFT]):
            Stage.PLAYER.Left()
            
        elif (KEYS[pygame.K_RIGHT]):
            Stage.PLAYER.Right()
            
        elif (KEYS[pygame.K_UP]):
            Stage.PLAYER.Up()
            
        elif (KEYS[pygame.K_DOWN]):
            Stage.PLAYER.Down()
        
        elif (KEYS[pygame.K_ESCAPE]):
            pygame.quit()
            sys.exit()
            
        elif (not KEYS[pygame.K_LEFT] and
              not KEYS[pygame.K_RIGHT] and
              not KEYS[pygame.K_UP] and
              not KEYS[pygame.K_DOWN]):
            Stage.PLAYER.Static()
            
        if (KEYS[pygame.K_LEFT] or
            KEYS[pygame.K_RIGHT] or
            KEYS[pygame.K_UP] or
            KEYS[pygame.K_DOWN]):
            Stage.PLAYER.Move()
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
                    
        Stage.Update(dt) # 순서에 따라 출력하는 결과가 다르다.. 왤까
        Stage.PLAYER.Update(Stage)
        Stage.Draw()
        Stage.PLAYER.Draw()
        
        Sys.InputText(Sys.SMALLFONT, str(';x') + '  '
                      + str(Stage.PLAYER.StartTwinkle) + '  ' 
                      + str(Stage.PLAYER.ElapsedTwinkle) + '  ' 
                      + str(Stage.PLAYER.TwinkleStack) + '  '
                      ,Sys.COLORDIC['BLUE'], 30, 30)
        
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