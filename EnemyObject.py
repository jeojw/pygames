import main
import random
import LifeObject

class EnemyObject(LifeObject):
    def __init__(self, Name, Type, x_pos, y_pos=None):
        '''
        적의 기본적인 정보를 저장하는 생성자
        '''
        super().__init__(x_pos, y_pos)
        
        self.direction = RIGHT
        self.Name = Name
        self.Type = Type
        self.isDrop = False # 아이템 드랍 관련 불값
        self.isDetect = False # 플레이어 발견 관련 불값
        self.atkcool = ENEMYATKCOOL
        
        if (self.Name == SEAL):
            self.attackRange = 75 # 공격 범위
            static = [pygame.image.load('enemy_sprite/Seal_sprite/seal_static.png')]
            dead = [pygame.image.load('enemy_sprite/Seal_sprite/seal_dead.png')]
            walk = [pygame.image.load('enemy_sprite/Seal_sprite/seal_walk_' + str(i) + '.png') for i in range(1, 3)]
            attack = [pygame.image.load('enemy_sprite/Seal_sprite/seal_attack_' + str(i) + '.png') for i in range(1, 3)]
            getattack = [pygame.image.load('enemy_sprite/Seal_sprite/seal_get_attack.png')]
            
        elif (self.Name == SNOWMAN):
            self.projectileimage = SNOWBALL
            self.attackDistance = 200
            static = [pygame.image.load('enemy_sprite/SnowMan_sprite/snowman_static.png')]
            dead = [pygame.image.load('enemy_sprite/SnowMan_sprite/snowman_dead.png')]
            walk = [pygame.image.load('enemy_sprite/SnowMan_sprite/snowman_walk_' + str(i) + '.png') for i in range(1, 3)]
            attack = [pygame.image.load('enemy_sprite/Seal_sprite/seal_attack_' + str(i) + '.png') for i in range(1, 3)]
            getattack = [pygame.image.load('enemy_sprite/SnowMan_sprite/snowman_get_attack.png')]
            
        elif (self.Name == POLARBEAR):
            static = [pygame.image.load('enemy_sprite/Seal_sprite/snowman_static.png')]
            dead = [pygame.image.load('enemy_sprite/Seal_sprite/seal_dead.png')]
            walk = [pygame.image.load('enemy_sprite/Seal_sprite/seal_walk_' + str(i) + '.png') for i in range(1, 3)]
            attack = [pygame.image.load('enemy_sprite/Seal_sprite/seal_attack_' + str(i) + '.png') for i in range(1, 3)]
            getattack = [pygame.image.load('enemy_sprite/Seal_sprite0/seal_get_attack.png')]

        self.spritelist = [static, walk, attack, getattack, dead]
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
        self.animation_time = round(100 / len(self.spritelist[self.cur] * 100), 2)
        
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
            
    def GetName(self):
        return self.Name
    
    def GetType(self):
        return self.Type
            
    def attack(self):
        super().attack()
        if (self.Name == SNOWMAN):
            if (self.isDead is False and self.isGetattack is False and self.coolElapsed == 0):
                if (self.direction == LEFT):
                    ProjectileList.append(Projectile(self.projectileimage, self.hitbox.left, MAP_GROUND - 50, self.ATK, LEFT))
                else:
                    ProjectileList.append(Projectile(self.projectileimage, self.hitbox.right, MAP_GROUND - 50, self.ATK, RIGHT))
            

    def dropItem(self):
        '''
        아이템을 드롭시키는 함수, 나중에 확률에 따라 드랍시킬 생각
        '''
        trueDrop = random.choices(range(1, len(ItemTypes)), weights = [1, 1, 1, 1, 1])
        if (trueDrop.pop() >= 4):
            image = random.choice(ItemTypes)
            Itemlist.append(ItemObject(self.x_pos, self.y_pos, image))
        
        if (self.Type == NORMAL):
            coindrops = random.randrange(1,3)
            for i in range(-coindrops, coindrops):
                Itemlist.append(ItemObject(self.x_pos + i * 20, self.y_pos, COIN))
        elif (self.Type == BOSS):
            coindrops = random.randrange(3,9)
            for i in range(-coindrops, coindrops):
                Itemlist.append(ItemObject(self.x_pos + i * 12, self.y_pos, COIN))
    
    def detectPlayer(self):
        '''
        플레이어를 감지하는 함수
        '''
        if (self.isDetect is False):
            self.effectStart = pygame.time.get_ticks()
        self.isDetect = True
        self.effectElapsed = (pygame.time.get_ticks() - self.effectStart) / 1000
        if (self.effectElapsed >= self.effectTime):
            self.effectStart = 0
            self.effectElapsed = 0
            
    def AI(self, player):
        '''
        기본적의 적의 AI
        플레이어에 상태에 따라서 업데이트가 된다
        '''
        distance = self.hitbox.centerx - (player.GetPos(X) + player.GetSize(WIDTH) / 2) #플레이어와 적과의 거리를 계산함
        if (abs(distance) <= 400 or self.HP != self.MAXHP):
            self.detectPlayer()
            
        if (self.isDetect):
            if (distance > 0):
                self.leftwalk()
            else:
                self.rightwalk()
                
        if (abs(distance) <= self.attackRange):
            if (player.GetCondition(HITBOX)):
                if (self.coolElapsed != 0 and self.checkcollision(player)):
                    self.static()
                self.attack()

        for projectile in player.GetProjectiles():
            if (len(player.GetProjectiles()) != 0):
                if (self.isHitbox):
                    if (self.checkcollision(projectile)):
                        self.index = 0
                        self.getattack(player)
                        player.GetProjectiles().remove(projectile)
                        
        if (player.GetCondition(DEAD)):
            self.static()

        if (self.isDead and self.isDrop is False):
            self.dropItem()
            self.isDrop = True
    
    def AI_2(self, player):
        distance = self.hitbox.centerx - (player.GetPos(X) + player.GetSize(WIDTH) / 2) #플레이어와 적과의 거리를 계산함
        if (abs(distance) <= 400 or self.HP != self.MAXHP):
            self.detectPlayer()
            
        if (self.isDetect):
            if (distance > 0):
                self.leftwalk()
            else:
                self.rightwalk()
                
        if (abs(distance) <= self.attackDistance):
            if (player.GetCondition(HITBOX)):
                if (self.coolElapsed != 0):
                    self.static()
                self.attack()

        for projectile in player.GetProjectiles():
            if (len(player.GetProjectiles()) != 0):
                if (self.isHitbox):
                    if (self.checkcollision(projectile)):
                        self.index = 0
                        self.getattack(player)
                        player.GetProjectiles().remove(projectile)
                        
        if (player.GetCondition(DEAD)):
            self.static()

        if (self.isDead and self.isDrop is False):
            self.dropItem()
            self.isDrop = True
            
        return distance
    
    def drawEffect(self):
        if (self.isDetect):
            if (self.effectElapsed != 0):
                Screen.blit(DETECTICON, (self.x_pos - 30, self.hitbox.top - 30))

    def drawStat(self):
        if (self.Type == NORMAL):
            Length = 125
            convertCoefficient = Length / self.MAXHP
            pygame.draw.rect(Screen, VIRGINRED, (self.hitbox.centerx - Length / 2,
                                             self.hitbox.bottom + 18, Length, 12), 3)
            if (self.HP >= 0):
                pygame.draw.rect(Screen, RED, (self.hitbox.centerx - Length / 2,
                                               self.hitbox.bottom + 19, self.HP * convertCoefficient, 9))
        elif (self.Type == BOSS):
            Length = 300
            convertCoefficient = Length / self.MAXHP
            
    def updatePos(self, Stage):
        '''
        오브젝트의 위치를 업데이트 시키는 메서드
        '''
        PlayerDirection = Stage.GetPlayer().GetCondition(DIRECTION)
        PlayerSpeed = Stage.GetPlayer().GetStat(SPEED)
        
        self.hitbox.x = self.x_pos
        self.hitbox.bottom = self.y_pos

        if (self.isWalk and self.isAttack is False):
            if (self.direction == LEFT):
                self.x_pos += -self.SPEED
            elif (self.direction == RIGHT):
                self.x_pos += self.SPEED
        
        if (Stage.XCameraMoveable and (Stage.isXCameraMove or Stage.forceXMove)):
            if (PlayerDirection == LEFT):
                self.x_pos += PlayerSpeed
            elif (PlayerDirection == RIGHT):
                self.x_pos -= PlayerSpeed
        
        elif (not Stage.isXCameraMove and (self.x_pos <= x_size and self.x_pos >= 0)):
            if (self.hitbox.left <= MAP_LIMIT_LEFT):
                self.x_pos = MAP_LIMIT_LEFT #좌표 보정인데.... 오류라서
            if (self.hitbox.right >= MAP_LIMIT_RIGHT):
                self.x_pos = MAP_LIMIT_RIGHT - self.hitbox.width
                    
        if (not Stage.GetPlayer().GetCondition(ONGROUND)):
            if (Stage.GetPlayer().airSpace != 0):
                self.y_pos -= Stage.GetPlayer().airSpace
            else:
                self.y_pos -= Stage.GetPlayer().gravity
        else:
            self.y_pos = MAP_GROUND
            
    def updateSprite(self, dt):# 추후 아이템 획득시에도 스프라이트 관련 업데이트를 추가할 것
        '''
        적의 스프라이트를 업데이트 시켜주는 함수
        스프라이트 업데이트 지연까지 추가함
        '''
        super().updateSprite(dt)
        if (self.direction == LEFT):
            self.hitbox = self.cursprite.get_rect(bottomright=(self.x_pos + 70, self.y_pos)) #방향전환시 좌표오류를 잡아줌
        else:
            self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
            
    def update(self, dt, Stage):
        '''
        적의 업데이트 메서드
        첫번째 변수는 스프라이트 업데이트 주기 설정, 두번째 변수는 AI가 작동될 목표
        '''
        if (self.Name == SEAL):
            self.AI(Stage.GetPlayer())
        elif (self.Name == SNOWMAN):
            self.AI_2(Stage.GetPlayer())
        super().update(dt, Stage)