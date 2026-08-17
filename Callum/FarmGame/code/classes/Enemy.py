import pygame


def give_variables(play, group):
    global player, creature_sprites
    player = play
    creature_sprites = group


from creature import Creature


class Enemies(Creature):
    def __init__(self, groups, image, scale, pos,health,speed):
        super().__init__(groups, image)
        self.right_image = pygame.transform.scale_by(self.right_image, scale)
        self.image = self.right_image
        self.rect = self.image.get_frect(center=pos)
        self.speed = speed
        self.max_health = health
        self.health = health
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


class FarmerBoss(pygame.sprite.Sprite):
    """Boss enemy for level 3. Uses walk + attack spritesheets."""

    DISPLAY_SIZE = (200, 200)

    def __init__(self, groups, pos):
        super().__init__(groups)

        walk_sheet = pygame.image.load(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'images', 'farmer.sprite.sheet.png')
        ).convert_alpha()

        attack_sheet = pygame.image.load(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'images', 'farmer.attack.sprite.sheet3.png')
        ).convert_alpha()

        self.walk_frames   = self._get_frames(walk_sheet,   6, 6)
        self.attack_frames = self._get_frames(attack_sheet, 5, 5)

        self.frame_index      = 0
        self.animation_timer  = 0
        self.animation_speed  = 0.1

        self.attacking         = False
        self.attack_timer      = 0
        self.attack_duration   = 0.6
        self.attack_cooldown   = 0
        self.attack_cooldown_max = 1.0

        self.health     = 300
        self.max_health = 300
        self.speed      = 110
        self.hit_flash_timer = 0

        self.image = self.walk_frames[0]
        self.rect  = self.image.get_frect(center=pos)

    # ------------------------------------------------------------------ helpers
    def _get_frames(self, sheet, columns, rows):
        w, h = sheet.get_size()
        fw, fh = w // columns, h // rows
        frames = []
        for row in range(rows):
            for col in range(columns):
                frame = sheet.subsurface(
                    pygame.Rect(col * fw, row * fh, fw, fh)
                ).copy()
                frame = pygame.transform.scale(frame, self.DISPLAY_SIZE)
                frames.append(frame)
        return frames

    # ------------------------------------------------------------------ public
    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash_timer = 0.1

    def draw_health_bar(self, surface):
        bar_width = 120
        x = self.rect.centerx - bar_width // 2
        y = self.rect.top - 18
        pygame.draw.rect(surface, (50, 50, 50),   (x, y, bar_width, 10))
        hp_w = max(0, int((self.health / self.max_health) * bar_width))
        pygame.draw.rect(surface, (220, 40, 40),  (x, y, hp_w, 10))
        pygame.draw.rect(surface, (225, 225, 225), (x, y, bar_width, 10), 1)

    # ------------------------------------------------------------------ update
    def _animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index += 1
            if self.attacking:
                if self.frame_index >= len(self.attack_frames):
                    self.frame_index = len(self.attack_frames) - 1
            else:
                if self.frame_index >= len(self.walk_frames):
                    self.frame_index = 0

        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= dt
            flash = (self.attack_frames if self.attacking else self.walk_frames)[self.frame_index].copy()
            flash.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGBA_MULT)
            self.image = flash
        else:
            self.image = (self.attack_frames if self.attacking else self.walk_frames)[self.frame_index]

    def update(self, dt):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        if self.attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attacking = False
                self.frame_index = 0
                self.animation_timer = 0
            self._animate(dt)
            return

        direction = (
            pygame.Vector2(player.rect.center) - pygame.Vector2(self.rect.center)
        )
        distance = direction.length()

        if distance > 150:
            direction = direction.normalize()
            self.rect.center += direction * self.speed * dt
        elif self.attack_cooldown <= 0:
            # start an attack swing
            self.attacking         = True
            self.attack_timer      = self.attack_duration
            self.attack_cooldown   = self.attack_cooldown_max
            self.frame_index       = 0
            self.animation_timer   = 0
            try:
                farmer_attack_sound.play()
            except Exception:
                pass

        self._animate(dt)
