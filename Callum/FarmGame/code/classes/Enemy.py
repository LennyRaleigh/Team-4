import pygame
from creature import Creature


class Enemies(Creature): #placeholder replace with fully made enemy class
    def __init__(self, groups,image,scale,pos):
        super().__init__(groups,image)
        self.right_image = pygame.transform.scale_by(self.right_image,scale)
        self.image = self.right_image
        self.rect = self.image.get_frect(center = pos)
        self.speed = 300
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
        self.rect.center += self.direction * self.speed * dt
    def anti_cramming(self):
        for sprite1 in creature_sprites:
            for sprite2 in creature_sprites:
                if sprite1 != sprite2:
                    if pygame.sprite.collide_mask(sprite1, sprite2,):
                        sprite1.rect.centerx += (sprite1.rect.centerx-sprite2.rect.centerx)**-1
                        sprite1.rect.centery += (sprite1.rect.centery-sprite2.rect.centery)**-1