import pygame

class LifeObject(object):
    '''
    해당 클래스는 가독성을 위해 enemy class, player class의 부모 클래스로, 이 클래스 기반으로 상속 및 오버라이딩을 함
    '''
    def __init__(self, System, x_pos, y_pos=None):
        '''
        해당 생성자는 부모 생성자로, 자식 클래스들이 이를 오버라이딩을 함!
        '''
        
        '''
        오브젝트의 스텟 및 위치
        '''
        self.system = System
        self.x_pos = x_pos
        if (y_pos is None):
            self.y_pos = 465
        else:
            self.y_pos = y_pos
        self.MAXHP = 0
        self.HP = 0
        self.ATK = 0
        self.DEF = 0
        self.SPEED = 0
        self.KNOCKBACK = 80 #피격당할 시 넉백되는 거리를 설정
        
        '''
        오브젝트의 전체적인 상태를 나타내는 변수들
        '''
        self.direction = 'right'
        self.isDead = False
        self.isAttack = False
        self.isWalk = False
        self.isOnGround = True
        self.isGetattack = False
        self.isHitbox = True # 사망 시에 히트박스 없는 것으로 처리
        self.attackHitbox = False # 공격 시의 히트박스(근접 타입의 적 및 캐릭터만 쓰이는 변수)
        self.isChangeStat = False # 스텟 변경이 되는지에 대한 불값
        self.isChangeCondition = False # 컨디션이 뒤바뀌었는지 검사하는 불값->이 값이 참이 될시에 current_time과 index가 0으로 초기화가 됨(기존에는 전환시에도 index와 current_time이 그대로라 스프라이트 업데이트가 잘 안됨)
        self.Condition = 'static' # 오브젝트의 컨디션
        self.projectilelist = []
        
        self.gravity = 0 # 중력 계수
        self.airSpace = -10 # 점프 계수
        
        self.ChangeDelay = 0.1 # 컨디션 전환 딜레이
        self.delayStart = 0 # 딜레이 시작 시간
        self.delayElapsed = 0 # 딜레이 경과 시간
        
        self.effectTime = 1.5 # 이펙트 표기 시간
        self.effectStart = 0 # 이펙트 표기 시작 시간
        self.effectElapsed = 0 # 이펙트 표기 경과 시간
        
        self.atkcool = 0 # 공격 쿨타임
        self.coolStart = 0 # 쿨타임 시작 시간
        self.coolElapsed = 0 # 쿨타임 경과 시간
        
        self.index = 0 # 각 스프라이트 리스트의 인덱스
        self.cur = 0 #각 스프라이트 덩어리의 인덱스
                
        self.animation_time = 0 # 스프라이트 업데이트 총 주기
        self.current_time = 0 # 경과 시간
    
    def SetStat(self, MAXHP, HP, ATK, DEF, SPEED):
        '''
        오브젝트의 스텟을 설정하는 메서드
        '''
        self.MAXHP = MAXHP
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.SPEED = SPEED
        
    def ChangeStat(self, MAXHP=0, HP=0 ,ATK=0, DEF=0, SPEED=0, ATTACKSPEED=1):
        '''
        오브젝트의 스텟의 변화를 주는 메서드
        주로 아이템이나 적의 공격을 받을 때 쓰인다
        '''
        self.MAXHP += MAXHP
        self.HP += HP
        self.ATK += ATK
        self.DEF += DEF
        self.SPEED += SPEED
        self.atkcool /= ATTACKSPEED
        
    def GetProjectiles(self):
        return self.projectilelist
    
    def GetStat(self, stat):
        '''
        오브젝트의 스텟 반환
        '''
        try:
            if (stat == 'maxhp'):
                return self.MAXHP
            elif (stat == 'hp'):
                return self.HP
            elif (stat == 'atk'):
                return self.ATK
            elif (stat == 'def'):
                return self.DEF
            elif (stat == 'speed'):
                return self.SPEED
            else:
                raise ValueError
        except ValueError:
            print(stat, 'is not Stat!!')
    
    def GetCondition(self, condition):
        '''
        오브젝트의 상태 불값에 대해 반환함
        '''
        try:
            if (condition == 'direction'):
                return self.direction
            elif (condition == 'onground'):
                return self.isOnGround
            elif (condition == 'walk'):
                return self.isWalk
            elif (condition == 'attack'):
                return self.isAttack
            elif (condition == 'getattack'):
                return self.isGetattack
            elif (condition == 'dead'):
                return self.isDead
            elif (condition == 'hitbox'):
                return self.isHitbox
            elif (condition == 'atkhitbox'):
                return self.attackHitbox
            else:
                raise ValueError
        except ValueError:
            print(condition, 'is not Condition!!')
    
    def GetPos(self, pos):
        '''
        오브젝트의 위치 반환
        '''
        pass
    
    def GetSize(self, length):
        '''
        오브젝트의 크기 반환
        '''
        pass
        
    def checkcollision(self, Anathor):
        '''
        히트박스간에 충돌을 검사하는 함수
        주로 클래스 내에서만 쓰이는 함수이다
        '''
        if (pygame.Rect.colliderect(self.hitbox, Anathor.hitbox)):
            return True
        else:
            return False
        
    def static(self):
        '''
        오브젝트의 모든 상태 불값이 False인 경우 static으로 반환함
        '''
        if (self.Condition != 'static'):
            self.isChangeCondition = True
            self.delayStart = pygame.time.get_ticks()
        else:
            self.isChangeCondition = False
            
        self.isWalk = False
        self.isAttack = False
        self.isGetattack = False
        self.isDead = False
        
    def left(self):
        '''
        왼쪽 방향
        '''
        self.direction = 'left'
    
    def right(self):
        '''
        오른쪽 방향
        '''
        self.direction = 'right'
        
    def walk(self):
        '''
        걷는 상태를 설정하는 메서드
        '''
        if (self.Condition != 'walk'):
            self.isChangeCondition = True
            self.delayStart = pygame.time.get_ticks()
        else:
            self.isChangeCondition = False
        
        if (self.isGetattack is False): # 만일 이 조건문이 없을 시 죽은 후에도 방향전환이 됨. 아래도 동일
            self.isWalk = True
            self.isAttack = False
            self.isGetattack = False
        else:
            self.isWalk = False
            
    def leftwalk(self):
        '''
        왼쪽방향으로 걷게 해주는 메서드
        사망시 방향전환 및 걷기가 안되도록 설정
        '''
        if (self.isDead is False):
            self.left()
            self.walk()
            
    def rightwalk(self):
        '''
        오른쪽방향으로 걷게 해주는 메서드
        사망시 방향전환 및 걷기가 안되도록 설정
        '''
        if (self.isDead is False):
            self.right()
            self.walk()
        
    def jump(self):
        '''
        오브젝트의 점프 상태를 설정하는 메서드
        오브젝트가 지면으로부터 붕 떠져있는 경우 더 이상 위로 올라가지 않게 수정
        '''
        if (self.isDead is False):
            self.isOnGround = False
                
    def attack(self):
        '''
        오브젝트의 공격 상태를 설정하는 메서드
        공격 함수 호출 시 쿨타임이 돌아가도록 설정함
        '''
        if (self.Condition != 'attack'):
            self.isChangeCondition = True
            self.delayStart = pygame.time.get_ticks()
        else:
            self.isChangeCondition = False
        
        if (self.isGetattack is False and self.isDead is False and self.coolElapsed == 0):
            self.isWalk = False
            self.isAttack = True
            self.attackHitbox = True
            self.coolStart = pygame.time.get_ticks()
        else:
            self.isAttack = False
            
    def getattack(self, Another):
        '''
        플레이어의 피격 상태를 표현해주는 메서드
        적의 위치상태에 따라 방향, 밀려나는 거리를 설정
        '''
        if (self.Condition != 'getattack'):
            self.isChangeCondition = True
            self.delayStart = pygame.time.get_ticks()
        else:
            self.isChangeCondition = False
            
        self.isGetattack = True
        self.isWalk = False
        self.isAttack = False
        self.HP -= (Another.GetStat('atk') - self.DEF)
        if (self.x_pos + self.hitbox.width / 2 > Another.GetPos('x') + Another.GetSize('width') / 2):
            self.direction = 'left'
            self.x_pos += self.KNOCKBACK
        else:
            self.direction = 'right'
            self.x_pos -= self.KNOCKBACK

    def dead(self):
        '''
        오브젝트가 죽었음을 나타내는 메서드
        '''
        if (self.isDead is False):
            self.isChangeCondition = True
        else:
            self.isChangeCondition = False
            
        self.isDead = True
        self.KNOCKBACK = 0
        self.isHitbox = False
        self.isWalk = False
        self.isAttack = False
        self.isGetattack = False
        self.flipPosible = False
    
    def drawPos(self):
        '''
        오브젝트의 위치에 따라 화면에 그려주는 메서드
        flipPosible 이 거짓일 경우 방향전환이 안되도록 함
        '''
        if (self.direction == 'left'):
            self.system.GetScreen().blit(pygame.transform.flip(self.cursprite, True, False), (self.hitbox.x, self.hitbox.y))
        else:
            self.system.GetScreen().blit(self.cursprite, (self.hitbox.x, self.hitbox.y))

    def drawStat(self):
        '''
        오브젝트의 스텟을 화면에 그려주는 메서드
        이 메서드는 자식 클래스에서 오버라이딩하게끔 수정
        '''
        pass
    
    def drawEffect(self):
        '''
        각종 이펙트를 그려주는 함수
        '''
        pass
        
    def draw(self):
        '''
        통합 draw 메서드
        가독성을 위해서
        '''
        self.drawPos()
        self.drawStat()
        self.drawEffect()

    def updateCooldown(self):
        '''
        공격 쿨타임을 업데이트 시켜주는 함수
        updateCondition내부에서만 쓰이는 함수임
        '''
        self.attackHitbox = False
        self.coolElapsed = (pygame.time.get_ticks() - self.coolStart) / 1000
        if (self.coolElapsed >= self.atkcool):
            self.coolElapsed = 0
            self.coolStart = 0
        
    def updateCycle(self):
        '''
        컨디션 전환시 스프라이트 업데이트 주기를 계산시켜주는 메서드
        클래스 내부에서만 쓰이는 메서드
        '''
        self.delayElapsed = (pygame.time.get_ticks() - self.delayStart) / 1000
        if (self.delayElapsed >= self.ChangeDelay):
            self.isChangeCondition = False
            self.delayElapsed = 0
            if (self.Condition == 'getattack'):
                self.isGetattack = False
        
    def updateCondition(self):
        '''
        오브젝트의 컨디션을 업데이트 시켜주는 함수
        불값을 기반으로 업데이트 시켜줌
        '''
        if (self.HP <= 0):
            self.dead()
            
        if (self.isWalk):
            self.Condition = 'walk'
        elif (self.isAttack):
            self.Condition = 'attack'
        elif (self.isGetattack):
            self.Condition = 'getattack'
        elif (self.isDead):
            self.Condition = 'dead'
        elif (self.isWalk is False and self.isAttack is False and
              self.isGetattack is False and self.isDead is False):
            self.Condition = 'static'
            
        if (self.Condition != 'attack'):
            self.updateCooldown()
        
    def updatePos(self, Stage):
        '''
        오브젝트의 위치를 업데이트 시키는 메서드
        '''
        pass
    
    def updateSprite(self, dt):# 추후 아이템 획득시에도 스프라이트 관련 업데이트를 추가할 것
        '''
        적의 스프라이트를 업데이트 시켜주는 함수
        스프라이트 업데이트 지연까지 추가함
        '''  
        self.current_time += dt
        
        if (self.Condition == 'static'):
            self.cur = 0
            self.updateCycle()
        if (self.Condition == 'walk'):
            self.cur = 1
            self.updateCycle()
        if (self.Condition == 'attack'):
            self.cur = 2
            self.updateCycle()
        if (self.Condition == 'getattack'):
            self.cur = 3
            self.updateCycle()
            self.isGetattack = False
        if (self.Condition == 'dead'):
            self.cur = 4
            self.isChangeCondition = False
        
        if (self.current_time >= self.animation_time or self.isChangeCondition):
            self.current_time = 0
            
            self.index += 1
            if (self.index >= len(self.spritelist[self.cur]) or self.isChangeCondition):
                self.index = 0
        
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
    def update(self, dt, Stage):
        '''
        통합 update 메서드
        가독성을 위해
        '''
        self.updateCondition()
        self.updatePos(Stage)
        self.updateSprite(dt)