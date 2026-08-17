import pygame
from os.path import join

def give_variables(play):
    global player
    player = play


from creature import Creature

class Farmer(Creature):
    DISPLAY_SIZE = (200, 200)

    def __init__(self, groups,image, walk, attack,sound):
        super().__init__(groups,image)

        self.walk_sheet = walk

        self.attack_sheet = attack

        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1

        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 0.6
        self.attack_cooldown = 0
        self.attack_cooldown_max = 1.0

        self.damage_cooldown = 0
        self.damage_cooldown_max = 1.0

        self.dead   = False
        self.speed  = 100

        self.health = 200
        self.max_health = 200

        self.hit_flash_timer = 0

        self.walk_frames = self.get_frames(self.walk_sheet,   6, 6)
        self.attack_frames = self.get_frames(self.attack_sheet, 5, 5)

        self.image = self.walk_frames[0]
        self.rect  = self.image.get_frect(center=(1000, 470))

        self.sound = sound

    def get_frames(self, sheet, columns, rows):
        sheet_width, sheet_height = sheet.get_size()
        frame_width  = sheet_width  // columns
        frame_height = sheet_height // rows

        frames = []
        #print("Sheet size:", sheet_width, sheet_height)
        #print("Frame size:", frame_width, frame_height)

        for row in range(rows):
            for col in range(columns):
                rect = pygame.Rect(
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height
                )
                frame = sheet.subsurface(rect).copy()
                frame = pygame.transform.scale(frame, Farmer.DISPLAY_SIZE)
                frames.append(frame)

        return frames

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash_timer = 0.1

        if self.health <= 0:
            self.dead = True
        

    def attack(self):
        if self.attack_cooldown <= 0 and not self.attacking:

            self.attacking = True
            self.attack_timer = self.attack_duration
            self.attack_cooldown = self.attack_cooldown_max
            self.frame_index = 0
            self.animation_timer = 0

            self.sound.play()

    def animate(self, dt):
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

        if self.attacking:
            self.image = self.attack_frames[self.frame_index]
        else:
            self.image = self.walk_frames[self.frame_index]

    def update(self, dt):          
        self.direction.x = player.rect.centerx - self.rect.centerx
        self.direction.y = player.rect.centery - self.rect.centery

        if self.dead:
            return

        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        if self.attacking:
            self.attack_timer -= dt

            if self.attack_timer <= 0:
                self.attacking = False
                self.frame_index = 0           
                self.animation_timer = 0

            self.animate(dt)
            return                                 

        if self.direction.length() > 150:
            self.direction = self.direction.normalize() if self.direction else self.direction
            self.rect.center += self.direction * self.speed * dt
        elif self.attack_cooldown <= 0:
            self.attack() 

            
        if self.attacking:
                player.take_damage(10)

        self.animate(dt)

    def draw_health_bar(self, surface):
        if self.health < self.max_health:
            bar_width = 50
            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.top - 12
            pygame.draw.rect(surface, (60, 0, 0), (bar_x, bar_y, bar_width, 6), border_radius=3)
            health_width = max(0, (self.health / self.max_health) * bar_width)
            pygame.draw.rect(surface, (220, 40, 40), (bar_x, bar_y, health_width, 6), border_radius=3)