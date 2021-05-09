import main
import LifeObject
import Projectile

class PlayerObject(LifeObject):
    def __init__(self, x_pos, y_pos=None):
        '''
        플레이어의 기본적인 정보를 설정하는 생성자
        여기에서 스프라이트 및 쿨타임 등을 관리함
        '''
        super().__init__(x_pos, y_pos)
        
        self.direction = RIGHT
        self.getitem = False
        self.itemcounts = 0 #누적으로 획득한 아이템 개수
        self.coincounts = 0 #코인 개수
        self.itemType = None
        self.projectileimage = BASIC
        self.ammunition = 30 # 강화 공격 제한 개수
        self.duration = 20 # 아이템 지속 시간
        self.itemStart = 0 # 아이템 시작 시간
        self.itemElapsed = 0 # 아이템 획득 후 경과시간
        self.atkcool = PLAYERATKCOOL
        
        static = [pygame.image.load('char_sprite/char_static.png')]
        dead = [pygame.image.load('char_sprite/char_dead.png')]
        walk = [pygame.image.load('char_sprite/char_walk_' + str(i) + '.png') for i in range(1, 4)]
        attack = [pygame.image.load('char_sprite/char_attack.png')]
        getattack = [pygame.image.load('char_sprite/char_get_attack.png')]

        self.spritelist = [static, walk, attack, getattack ,dead]
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
        self.animation_time = round(100 / len(self.spritelist[self.cur] * 100), 2)
        
    def ResetCondition(self):
        '''
        플레이어의 체력을 제외한 모든 스텟 및 시간을 초기화시키는 메서드
        주로 아이템을 중복으로 먹었을 시에 활성화 됨
        '''
        self.MAXHP = PlayerStat[0]
        self.ATK = PlayerStat[2]
        self.DEF = PlayerStat[3]
        self.SPEED = PlayerStat[4]
        self.projectileimage = BASIC
        
        self.duration = DURATION
        self.itemStart = 0
        self.itemElapsed = 0
        self.atkcool = PLAYERATKCOOL
        self.ammunition = AMMUNITION
        
    def GetPos(self, pos):
        '''
        오브젝트의 위치 반환
        '''
        try:
            if (pos == 'x'):
                return self.hitbox.x
            elif (pos == 'y'):
                return self.hitbox.y
            else:
                raise ValueError
        except ValueError:
            print('Not Pos!!!!')
        
    def GetSize(self, length):
        '''
        오브젝트의 크기 반환
        '''
        try:
            if (length == 'width'):
                return self.hitbox.width
            elif (length == 'height'):
                return self.hitbox.height
            else:
                raise ValueError
        except ValueError:
            print('Not Lenght!!!')
                
    def attack(self):
        '''
        플레이어의 공격 상태를 설정하는 메서드
        플레이어는 원거리 공격을 주로 하므로 공격판정마다 projectilelist 내에 방향을 추가
        (overriding)
        '''
        super().attack()
        if (self.itemType == ICE and self.coolElapsed == 0):
            self.ammunition -= 1
        if (self.isDead is False and self.isGetattack is False and self.coolElapsed == 0):
            if (self.direction == LEFT):
                self.projectilelist.append(Projectile(self.projectileimage, self.hitbox.left, self.hitbox.y, self.ATK, LEFT))
            else:
                self.projectilelist.append(Projectile(self.projectileimage, self.hitbox.right, self.hitbox.y, self.ATK, RIGHT))
                 
    def getItem(self):
        '''
        아이템을 얻게 해주는 메서드 아이템 종류에 따라 효과가 다르게 발동되도록 변경
        '''
        for item in Itemlist:
            if (self.checkcollision(item)):
                Itemlist.remove(item)
                self.getitem = True
                if (item.GetImage() != COIN):
                    self.isChangeStat = True
                    self.itemcounts += 1
                    if (item.GetImage() == ICE):
                        self.itemType = ICE
                        self.ResetCondition()
                        self.ChangeStat(*ICEStat)
                        self.projectileimage = REINFORCE
                        self.getitem = False
                    elif (item.GetImage() == ARMOR):
                        self.itemType = ARMOR
                        self.ResetCondition()
                        self.ChangeStat(*ARMORStat)
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == HASTE):
                        self.itemType = HASTE
                        self.ResetCondition()
                        self.ChangeStat(*HASTEStat)
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == ATTACKSPEED):
                        self.itemType = ATTACKSPEED
                        self.ResetCondition()
                        self.ChangeStat(*ATTACKSPEEDStat)
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == MAXHPUP):
                        self.itemType = MAXHPUP
                        self.ResetCondition()
                        self.ChangeStat(*MAXHPUPStat)
                        self.HP = self.MAXHP
                        self.itemStart = pygame.time.get_ticks()
                        self.getitem = False
                    elif (item.GetImage() == HPRECOVERY):
                        self.HP = self.MAXHP
                        self.getitem = False
                else:
                    self.coincounts += 1
                    self.getitem = False
                
    def ItemReset(self):
        '''
        아이템 효과가 다할 시에 관련 변수들을 리셋시켜주는 메서드
        복잡하길래 그냥 하나로 묶어버림
        '''
        self.itemType = None
        self.ResetCondition()
        self.isChangeStat = False
        if (self.itemType == ICE):
            self.projectileimage = BASIC
            self.ammunition = AMMUNITION
        else:
            self.itemElapsed = 0
            self.itemStart = 0

    def drawStat(self):
        '''
        플레이어의 스텟을 그려주는 메서드
        '''
        Length = 200
        convertCoefficient = Length / self.MAXHP
        pygame.draw.rect(Screen, VIRGINRED, (10, 10, Length, 30), 2)
        if (self.HP >= 0):
            pygame.draw.rect(Screen, RED, (10, 10, self.HP * convertCoefficient , 30))
            
        if (self.itemType == ICE):
            Screen.blit(ICEICON, (Length + 20, 15))
            write(SmallFont, ' X ' + str(self.ammunition), BLACK, Length + 40, 15)
        elif (self.itemType == ARMOR):
            Screen.blit(ARMORICON, (Length + 20, 15))
            write(SmallFont, ' : ' + str(self.duration - self.itemElapsed) + ' sec ', BLACK, Length + 40, 15)
        elif (self.itemType == HASTE):
            Screen.blit(HASTEICON, (Length + 20, 15))
            write(SmallFont, ' : ' + str(self.duration - self.itemElapsed) + ' sec ', BLACK, Length + 40, 15)
        elif (self.itemType == ATTACKSPEED):
            Screen.blit(ATTACKSPEEDICON, (Length + 20, 15))
            write(SmallFont, ' : ' + str(self.duration - self.itemElapsed) + ' sec ', BLACK, Length + 40, 15)
            
    def updateCondition(self):
        '''
        플레어어의 컨디션을 업데이트 시켜주는 함수
        불값을 기반으로 업데이트 시켜줌
        
        아이템 관련 및 피격까지 관리함
        '''
        super().updateCondition()
        for enemy in Enemylist:
            if (self.isHitbox):
                if (self.checkcollision(enemy) and enemy.GetCondition(ATKHITBOX)):
                    self.getattack(enemy)
                    
        for projectile in ProjectileList:
            if (len(ProjectileList) != 0):
                if (self.isHitbox):
                    if (self.checkcollision(projectile)):
                        self.getattack(enemy)
                        ProjectileList.remove(projectile)
                    
        if (self.isChangeStat):
            if (self.itemType == ICE):
                if (self.ammunition == 0):
                    self.ItemReset()
            elif (self.itemType == ARMOR):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
            elif (self.itemType == HASTE):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
            elif (self.itemType == ATTACKSPEED):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
            elif (self.itemType == MAXHP):
                self.itemElapsed = int((pygame.time.get_ticks() - self.itemStart) / 1000)
                if (self.itemElapsed > DURATION):
                    self.ItemReset()
                    if (self.HP > self.MAXHP):
                        self.HP = self.MAXHP
                        
    def updatePos(self, Stage):
        '''
        오브젝트의 위치를 업데이트 시키는 메서드
        플레이어는 카메라의 위치에 따라 위치가 보정되도록 변경됨
        '''
        self.hitbox.x = self.x_pos
        self.hitbox.bottom = self.y_pos

        if (Stage.GetCameraView(X) <= map_x_size - x_size or Stage.GetCameraView(X) >= 0):
            if (self.hitbox.centerx > CAMERAXMARGIN and self.direction == RIGHT):
                if (Stage.XCameraMoveable):
                    Stage.CameraXMovement(self.SPEED)
                    self.x_pos -= self.SPEED
            elif (self.hitbox.centerx <= CAMERAXMARGIN and Stage.GetCameraView(X) > 0 and self.direction == LEFT):
                if (Stage.XCameraMoveable):
                    Stage.CameraXMovement(-self.SPEED)
                    self.x_pos += self.SPEED
                
        if (Stage.XCameraMoveable is False):
            if (self.hitbox.left <= MAP_LIMIT_LEFT):
                self.x_pos = MAP_LIMIT_LEFT
            if (self.hitbox.right >= MAP_LIMIT_RIGHT):
                self.x_pos = MAP_LIMIT_RIGHT - self.hitbox.width
                
        if (self.isOnGround is False):
            self.y_pos += self.airSpace
            Stage.CameraYMovement(self.airSpace)
            if (self.y_pos <= MAP_GROUND - JUMPDISTANCE):
                self.airSpace = 0
                self.gravity = GRAVITY
            self.y_pos += self.gravity
            Stage.CameraYMovement(self.gravity)
        if (self.y_pos >= MAP_GROUND):
            self.y_pos = MAP_GROUND
            self.isOnGround = True
            self.gravity = 0
            self.airSpace = AIRSPACE
                
        if (self.isWalk and self.isAttack is False):
            if (self.direction == LEFT):
                self.x_pos += -self.SPEED
            elif (self.direction == RIGHT):
                self.x_pos += self.SPEED