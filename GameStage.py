import main

class GameStage(object):
    '''
    해당 클래스는 게임 스테이지를 구현시켜주는 클래스로, 여기에서 스테이지 진행, 게임오버 화면, 클리어 화면, 오프닝, 카메라 뷰 등을 모두 다룸
    '''
    def __init__(self, stage, score):
        '''
        스테이지의 기본적인 시스템
        '''
        self.stage = stage # 스테이지 설정
        self.totalScore = score
        self.curScore = 0
        self.mapImages = [stage_1_scale, stage_2_scale] # 스테이지 맵 이미지
        
        self.PLAYER = None # 스테이지 내에 그려질 플레이어
        self.ClearStage = False # 스테이지가 클리어 됬는지 아닌지 판별하는 불값
        self.GameOver = False
        self.XCameraMoveable = True # 카메라가 이동가능한 상태인지 설정시켜주는 불값
        self.isXCameraMove = False # 지금 카메라가 작동하고 있는지 판별시켜주는 불값
        self.forceXMove = False # 모든 적이 죽었르 경우 발동되는 불값
        self.isYCameraMove = False
        self.CameraDirection = LEFT # 카메라 방향
        self.Deadboollist = [] # 적 전체의 사망 판정을 관리하는 리스트
        self.Deadbooldic = {NORMAL: list(),
                            BOSS: list()} #점수 차등 부여를 위한 딕셔너리 타입, 추후에 활용할 예정
        self.curDeadbool = [] # 현재 카메라가 비추는 영역에서의 적의 사망 판정으 관리하는 리스트
        self.CameraPos = [0, 0] # 카메라 위치
        self.CameraSlack = pygame.Rect(CAMERAXMARGIN, CAMERAYMARGIN, x_size - CAMERAXMARGIN * 2, MAP_GROUND - CAMERAYMARGIN)
        
        self.clearCounts = 0
    def GetPlayer(self):
        '''
        플레이어를 리턴시켜주는 메서드
        주로 플레이어의 정보를 필요로 하는 루프나 클래스에서 쓰임
        '''
        return self.PLAYER
    
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
            print('Not Pos!!!')
            
    def OpeningScreen(self):
        '''
        게임 오프닝을 보여주는 메서드
        '''
        while True:
            Screen.fill(WHITE)
            write(BigFont, 'Adventure', BLACK, XMARGIN, 200)
            write(BigFont, 'Press S!', BLACK, XMARGIN, 350)
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
            Screen.fill(WHITE)
            write(SmallFont, 'MANUAL', BLACK, XMARGIN, 30)
            write(SmallFont, '<-, -> : LEFT, RIGHT MOVE', BLACK, XMARGIN, 80)
            write(SmallFont, '^ : JUMP', BLACK, XMARGIN, 110)
            write(SmallFont, 'x : ATTACK', BLACK, XMARGIN, 140)
            write(SmallFont, 'z : GETITEM', BLACK, XMARGIN, 170)
            write(SmallFont, 'ESC : GAME TERMINATE', BLACK, XMARGIN, 200)
        
            Screen.blit(ICEICON, (XMARGIN, 240))
            write(SmallFont, ': REINFORCE ATK', BLACK, XMARGIN + 35, 240)
            Screen.blit(ARMORICON, (XMARGIN, 270))
            write(SmallFont, ': REINFORCE DEF', BLACK, XMARGIN + 35, 270)
            Screen.blit(HASTEICON, (XMARGIN, 300))
            write(SmallFont, ': REINFORCE SPEED', BLACK, XMARGIN + 35, 300)
            Screen.blit(ATTACKSPEEDICON, (XMARGIN, 330))
            write(SmallFont, ': REINFORCE ATTACKSPEED', BLACK, XMARGIN + 35, 330)
            Screen.blit(HPRECOVERYICON, (XMARGIN, 360))
            write(SmallFont, ': RECOVERY HP', BLACK, XMARGIN + 35, 360)
            Screen.blit(MAXHPUPICON, (XMARGIN, 390))
            write(SmallFont, ': IMPROVE MAXHP AND RECOVERY HP', BLACK, XMARGIN + 35, 390)
            
            write(SmallFont, 'PRESS S!', BLACK, XMARGIN, 500)
            pygame.draw.rect(Screen, BLACK, (0, 0, x_size, y_size), 5)
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
        write(BigFont, 'Stage Clear!!!', BLACK, XMARGIN, 200)
        if (len(self.mapImages) == self.clearCounts):
            write(BigFont, 'Total Sclre: ' + str(self.totalScore + self.curScore), BLACK, XMARGIN, 270)
        pygame.display.update()
        pygame.time.wait(1000)
            
    def GameoverScreen(self):
        '''
        플레이어의 HP가 전부 소진되고 적이 전원 사망하지 않을 시 나오는 화면
        '''
        write(BigFont, 'GameOver!!!', BLUE, XMARGIN, 200)
        write(BigFont, 'Try Again?', BLUE, XMARGIN, 280)
        write(BigFont, 'Y / N', BLUE, XMARGIN, 360)
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
                    
    def SetEnemy(self, EnemyList):
        for enemy in EnemyList:
            if (enemy.GetName() == SEAL):
                enemy.SetStat(*EnemyStatdic[SEAL])
            elif (enemy.GetName() == SNOWMAN):
                enemy.SetStat(*EnemyStatdic[SNOWMAN])
            self.Deadboollist.append(enemy.GetCondition(DEAD))
              
    def SetStage(self):
        '''
        스테이지를 설정시켜주는 메서드
        주로 main()함수에서 쓰임
        '''
        if (self.stage == 1):
            self.PLAYER = PlayerObject(100)
            self.PLAYER.SetStat(*PlayerStat)
            
            Itemlist.append(ItemObject(100, MAP_GROUND, COIN))
            Enemylist.append(EnemyObject(SNOWMAN, NORMAL, 800))
            Enemylist.append(EnemyObject(SEAL, NORMAL, 500))
            Enemylist.append(EnemyObject(SEAL, NORMAL, 1500))
            Enemylist.append(EnemyObject(SNOWMAN, NORMAL, 1800))
            self.SetEnemy(Enemylist)
                
        elif (self.stage == 2):
            self.PLAYER = PlayerObject(100)
            self.PLAYER.SetStat(*PlayerStat)
            
            Enemylist.append(EnemyObject(SEAL, NORMAL, 800))
            self.SetEnemy(Enemylist)
                
    def ResetStage(self):
        '''
        스테이지 재시도시 또는 스테이지 클리어 시 호출되는 메서드
        '''
        Enemylist.clear()
        Itemlist.clear()
        self.Deadboollist.clear()
        self.PLAYER.GetProjectiles().clear()
        ProjectileList.clear()
        for enemy in Enemylist:
            self.Deadboollist.append(enemy.GetCondition(DEAD))
        self.ClearStage = False
        self.GameOver = False
    
    def DrawStage(self):
        '''
        스테이지를 그려주는 메서드
        '''
        Screen.blit(self.mapImages[self.stage - 1], (0, y_size - map_y_size), (self.CameraPos[0], self.CameraPos[1], map_x_size, map_y_size))
        write(SmallFont, 'Scroe: ' + str(self.totalScore + self.curScore), BLACK, 650, 25)
        
    def UpdateEnemy(self):
        '''
        적들이
        '''
        self.Deadboollist.clear()
        self.curDeadbool.clear()
        for enemy in Enemylist:
            self.Deadboollist.append(enemy.GetCondition(DEAD))
            if (enemy.GetPos(X) >= 0 and enemy.GetPos(X) + enemy.GetSize(WIDTH) <= x_size):
                self.curDeadbool.append(enemy.GetCondition(DEAD))
                
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
        PlayerCenterX = self.PLAYER.GetPos(X) + self.PLAYER.GetSize(WIDTH) / 2
        PlayerCenterY = self.PLAYER.GetPos(Y) + self.PLAYER.GetSize(HEIGHT) / 2
        self.CameraDirection = self.PLAYER.GetCondition(DIRECTION)
            
        if (self.CameraPos[0] + x_size >= map_x_size):
            self.CameraPos[0] = map_x_size - x_size
            self.XCameraMoveable = False
        elif (PlayerCenterX <= CAMERAXMARGIN and self.CameraPos[0] <= 0):
            self.CameraPos[0] = 0
            self.XCameraMoveable = False
            
        for enemy in Enemylist:
            if (enemy.GetPos(X) <= x_size - enemy.GetSize(WIDTH) and enemy.GetPos(X) >= 0):
                if (not all(self.curDeadbool)):
                    self.isXCameraMove = False
                    self.XCameraMoveable = False
                elif (all(self.curDeadbool) and (self.CameraPos[0] > 0 and self.CameraPos[0] < map_x_size - x_size)):
                    self.XCameraMoveable = True
                if (PlayerCenterX > CAMERAXMARGIN and self.CameraDirection == RIGHT and self.XCameraMoveable):
                    self.forceXMove = True
                else:
                    self.forceXMove = False
        if (self.PLAYER.GetCondition(WALK)):
            self.isXCameraMove = True
        else:
            self.isXCameraMove = False
        
        if (not self.XCameraMoveable):
            if (self.CameraPos[0] >= map_x_size - x_size):
                if (PlayerCenterX < CAMERAXMARGIN):
                    self.XCameraMoveable = True
            elif (self.CameraPos[0] <= 0):
                if (PlayerCenterX > CAMERAXMARGIN):
                    self.XCameraMoveable = True
                    
        if (self.PLAYER.GetCondition(ONGROUND)):
            self.CameraPos[1] = 0
            
    def removeProjectile(self):
        '''
        투사체가 맵 밖으로 나갈 때 지우는 메서드
        '''
        PlayerProjectile = self.PLAYER.GetProjectiles()
        
        for projectile in PlayerProjectile:
            if (projectile.GetPos(X) <= MAP_LIMIT_LEFT or projectile.GetPos(X) + projectile.GetSize(WIDTH) >= MAP_LIMIT_RIGHT):
                PlayerProjectile.remove(projectile)
                
        for projectile in ProjectileList:
            if ((projectile.GetPos(X) <= MAP_LIMIT_LEFT or projectile.GetPos(X) + projectile.GetSize(WIDTH) >= MAP_LIMIT_RIGHT) or
                abs(projectile.GetPos(X) - projectile.GetInitPos(X)) > SNOWBALLRANGE):
                ProjectileList.remove(projectile)
                    
    def UpdateStage(self):
        '''
        통합 업데이트 메서드
        '''
        self.UpdateCamera()
        self.UpdateEnemy()
        self.removeProjectile()
        self.UpdateScore()