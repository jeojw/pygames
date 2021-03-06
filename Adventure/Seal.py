import pygame
import EnemyObject

COIN = 'items/coin.png'

class Seal(EnemyObject.EnemyObject):
    def __init__(self, System, x_pos, y_pos):
        super().__init__(System, x_pos, y_pos)
        
        self.Name = 'Seal'
        self.Attackable = True
        self.attackRange = 75 # 공격 범위
        static = [pygame.image.load('Adventure/enemy_sprite/Seal_sprite/seal_static.png')]
        dead = [pygame.image.load('Adventure/enemy_sprite/Seal_sprite/seal_dead.png')]
        walk = [pygame.image.load('Adventure/enemy_sprite/Seal_sprite/seal_walk_' + str(i) + '.png') for i in range(1, 3)]
        attack = [pygame.image.load('Adventure/enemy_sprite/Seal_sprite/seal_attack_' + str(i) + '.png') for i in range(1, 3)]
        getattack = [pygame.image.load('Adventure/enemy_sprite/Seal_sprite/seal_get_attack.png')]
        
        self.spritelist = [static, walk, attack, getattack, dead]
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
        self.animation_time = round(100 / len(self.spritelist[self.cur] * 100), 2)
        
    def attack(self, Stage):
        super().attack()

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
            
        if (not self.Attackable):
            self.updateCooldown()
            
    def AI(self, Stage):
        '''
        기본적의 적의 AI
        플레이어에 상태에 따라서 업데이트가 된다
        '''
        distance = self.hitbox.centerx - (Stage.GetPlayer().GetPos('x') + Stage.GetPlayer().GetSize('width') / 2) #플레이어와 적과의 거리를 계산함
        if (abs(distance) <= 400 or self.HP != self.MAXHP):
            self.detectPlayer()
            
        if (self.isDetect):
            if (distance > 0):
                self.leftwalk()
            else:
                self.rightwalk()
                
        if (abs(distance) <= self.attackRange):
            if (Stage.GetPlayer().GetCondition('hitbox')):
                if (self.coolElapsed != 0 and self.checkcollision(Stage.GetPlayer())):
                    self.static()
                self.attack(Stage)

        for projectile in Stage.GetPlayer().GetProjectiles():
            if (len(Stage.GetPlayer().GetProjectiles()) != 0):
                if (self.isHitbox):
                    if (self.checkcollision(projectile)):
                        self.index = 0
                        self.getattack(Stage.GetPlayer())
                        Stage.GetPlayer().GetProjectiles().remove(projectile)
                        
        if (Stage.GetPlayer().GetCondition('dead')):
            self.static()

        if (self.isDead and self.isDrop is False):
            self.dropItem(Stage)
            self.isDrop = True