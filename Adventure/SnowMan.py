import pygame
import EnemyObject
import Projectile

COIN = 'Adventure/items/coin.png'

class SnowMan(EnemyObject.EnemyObject):
    def __init__(self, System, x_pos, y_pos):
        super().__init__(System, x_pos, y_pos)
        
        self.distance = 0
        self.isThrow = False
        self.Name = 'SnowMan'
        self.projectileimage = 'Adventure/enemy_sprite/SnowMan_sprite/snowball.png'
        self.attackDistance = 280
        static = [pygame.image.load('Adventure/enemy_sprite/SnowMan_sprite/snowman_static.png')]
        dead = [pygame.image.load('Adventure/enemy_sprite/SnowMan_sprite/snowman_dead.png')]
        walk = [pygame.image.load('Adventure/enemy_sprite/SnowMan_sprite/snowman_walk_' + str(i) + '.png') for i in range(1, 3)]
        attack = [pygame.image.load('Adventure/enemy_sprite/SnowMan_sprite/snowman_attack_' + str(i) + '.png') for i in range(1, 3)]
        getattack = [pygame.image.load('Adventure/enemy_sprite/SnowMan_sprite/snowman_get_attack.png')]
        
        self.spritelist = [static, walk, attack, getattack, dead]
        self.cursprite = self.spritelist[self.cur][self.index]
        self.hitbox = self.cursprite.get_rect(bottomleft=(self.x_pos, self.y_pos))
        
        self.animation_time = round(100 / len(self.spritelist[self.cur] * 100), 2)
        
    def attack(self, Stage):
        super().attack()
        if (self.isDead is False and self.isGetattack is False 
            and self.isThrow is False and self.index == 1):
            self.coolStart = pygame.time.get_ticks() # 여기에서 쿨다운 시전
            self.isThrow = True
            if (self.direction == 'left'):
                Stage.appendProjectile(Projectile.Projectile(self.projectileimage, self.hitbox.left, Stage.GetMapLimit('onground') - 50, self.ATK, 'left'))
            else:
                Stage.appendProjectile(Projectile.Projectile(self.projectileimage, self.hitbox.right, Stage.GetMapLimit('onground') - 50, self.ATK, 'right'))
                
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
            self.isThrow = False
            
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
            
        if (self.isThrow):
            self.updateCooldown()
                
    def AI(self, Stage):
        distance = self.hitbox.centerx - (Stage.GetPlayer().GetPos('x') + Stage.GetPlayer().GetSize('width') / 2) #플레이어와 적과의 거리를 계산함
        self.distance = distance
        
        if (abs(distance) <= 400 or self.HP != self.MAXHP):
            self.detectPlayer()
            
        if (self.isDetect):
            if (distance > 0):
                self.leftwalk()
            else:
                self.rightwalk()
                
        if (abs(distance) <= self.attackDistance and abs(distance) > 150):
            if (Stage.GetPlayer().GetCondition('hitbox')):
                if (self.coolElapsed != 0):
                    self.static()
                else:
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
