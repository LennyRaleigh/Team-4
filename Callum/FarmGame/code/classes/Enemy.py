import pygame


def give_variables(play,group):
    global player, creature_sprites
    player = play 
    creature_sprites = group
    
from creature import Creature


class Enemies(Creature): #placeholder replace with fully made enemy class
    def __init__(self, groups,image,scale,pos):
        super().__init__(groups,image)
        self.right_image = pygame.transform.scale_by(self.right_image,scale)
        self.image = self.right_image
        self.rect = self.image.get_frect(center = pos)
        self.speed = 150

        self.max_health = 100
        self.health = 100
        self.hit_flash_timer = 0

    def update(self,dt):
        self.direction.x = player.rect.centerx - self.rect.centerx
        self.direction.y = player.rect.centery - self.rect.centery
        if abs(self.direction.x) < 50:
            self.direction.x =0
        if abs(self.direction.y) < 50:
            self.direction.y =0
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.surf_direction()
        self.anti_cramming()

        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1*dt*100

            self.image = self.image.fill("#FFFFFF")
        
    
        self.rect.center += self.direction * self.speed * dt
    def anti_cramming(self):
        for sprite1 in creature_sprites:
            for sprite2 in creature_sprites:
                if sprite1 != sprite2:
                    if pygame.sprite.collide_mask(sprite1, sprite2,):
                        sprite1.rect.centerx += (sprite1.rect.centerx-sprite2.rect.centerx)**-1
                        sprite1.rect.centery += (sprite1.rect.centery-sprite2.rect.centery)**-1


    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash_timer = 8

