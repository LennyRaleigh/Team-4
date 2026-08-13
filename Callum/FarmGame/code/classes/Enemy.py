import pygame


def give_variables(play, group):
    global player, creature_sprites
    player = play
    creature_sprites = group


from creature import Creature


class Enemies(Creature):
    def __init__(self, groups, image, scale, pos):
        super().__init__(groups, image)
        self.right_image = pygame.transform.scale_by(self.right_image, scale)
        self.image = self.right_image
        self.rect = self.image.get_frect(center=pos)
        self.speed = 150
        self.max_health = 100
        self.health = 100
        self.hit_flash_timer = 0
        self.knockback = pygame.Vector2()
        self.knockback_timer = 0

    def update(self, dt):
        self.direction.x = player.rect.centerx - self.rect.centerx
        self.direction.y = player.rect.centery - self.rect.centery
        if abs(self.direction.x) < 50:
            self.direction.x = 0
        if abs(self.direction.y) < 50:
            self.direction.y = 0
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.anti_cramming()
        if self.knockback_timer > 0:
            self.knockback_timer -= 1 * dt * 100
        else:
            self.knockback *= 0
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1 * dt * 100
            flash = self.right_image.copy()
            flash.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGBA_MULT)
            self.image = flash
        else:
            self.surf_direction()
        self.rect.center += self.direction * self.speed * dt 
        self.rect.center += self.knockback * self.speed * 5 * dt

    def anti_cramming(self):
        for sprite1 in creature_sprites:
            for sprite2 in creature_sprites:
                if sprite1 != sprite2:
                    if pygame.sprite.collide_mask(sprite1, sprite2):
                        diff_x = sprite1.rect.centerx - sprite2.rect.centerx
                        diff_y = sprite1.rect.centery - sprite2.rect.centery
                        #if diff_x != 0:
                        #    sprite1.rect.centerx += 1 if diff_x > 0 else -1
                        #if diff_y != 0:
                        #    sprite1.rect.centery += 1 if diff_y > 0 else -1
                        sprite1.rect.centerx += (diff_x)**-1
                        sprite1.rect.centery += (diff_y)**-1
    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash_timer = 8
        
        self.knockback.x = self.rect.centerx-player.rect.centerx
        self.knockback.y = self.rect.centery-player.rect.centery
        self.knockback = self.knockback.normalize()
        self.knockback_timer = 10

    def draw_health_bar(self, surface):
        if self.health < self.max_health:
            bar_width = 50
            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.top - 12
            pygame.draw.rect(surface, (60, 0, 0), (bar_x, bar_y, bar_width, 6), border_radius=3)
            health_width = max(0, (self.health / self.max_health) * bar_width)
            pygame.draw.rect(surface, (220, 40, 40), (bar_x, bar_y, health_width, 6), border_radius=3)
