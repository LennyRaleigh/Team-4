import pygame
from creature import Creature
from os.path import join

class Player(Creature):

    FRAME_COORDS = [
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        (0, 2), (1, 2),
    ]
    FRAME_SIZE = 64
    DISPLAY_SIZE = (100, 100)

    def __init__(self, groups,image,pos):
        super().__init__(groups,image)
        sheet = pygame.image.load(
        join("FarmGame\images\sprite-64x64px-8f-sheet.png")
        ).convert_alpha()

        self.frames_right = []

        for col, row in self.FRAME_COORDS:
            rect = pygame.Rect(
                col * self.FRAME_SIZE,
                row * self.FRAME_SIZE,
                self.FRAME_SIZE,
                self.FRAME_SIZE
            )

            frame = sheet.subsurface(rect).copy()
            frame = pygame.transform.scale(frame, self.DISPLAY_SIZE)
            self.frames_right.append(frame)
        

        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 6

        self.right_image = self.frames_right[self.frame_index]
        #self.right_image = pygame.transform.scale_by(self.right_image,2)
        self.image = self.right_image
        self.base_image = self. right_image
        self.rect = self.image.get_frect(center = (pos))
        self.speed = 300
        self.dodge_speed = 1000

        self.max_health = 100
        self.health = 100
        self.carrots_collected = 0

        self.damage_cooldown = 0

        self.dodging = False
        self.dodge_timer = 0
        self.dodge_cooldown = 0

        self.attack_damage = 15
        self.attack_range = 55
        self.attack_size = (55, 70)
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 12
        self.attack_cooldown = 0
        self.attack_cooldown_max = 30
        self.enemies_hit = []

        
    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            self.dodge()
    
        if pygame.mouse.get_just_pressed()[0]:
            print("attack")

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1*dt*100

        if self.dodge_timer > 0:
            self.dodge_timer -= 1*dt*100
        else:
            self.dodging = False

        if self.dodge_cooldown > 0:
            self.dodge_cooldown -= 1*dt*100

        if self.attack_timer > 0:
            self.attack_timer -= 1*dt*100

            if self.attack_timer <= 0:
                self.attacking = False
        else:
            self.attacking = False

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1*dt*100


        if self.direction != (0,0):
            self.animation_timer += 1 * dt *100
            if self.animation_timer  >= self.animation_speed :
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames_right)
        else:
            self.frame_index = 0
            self.animation_timer = 0

        self.right_image = self.frames_right[self.frame_index]

        self.surf_direction()
        if self.dodging:
            self.rect.center += self.direction * self.dodge_speed * dt
        else:
            self.rect.center += self.direction * self.speed * dt

    def dodge(self):
        if self.dodge_cooldown <= 0:
            self.dodging = True
            self.dodge_timer = 15
            self.dodge_cooldown = 60

    def take_damage(self, amount):
        if self.damage_cooldown <= 0 and not self.dodging:
            self.health -= amount
            self.damage_cooldown = 30
