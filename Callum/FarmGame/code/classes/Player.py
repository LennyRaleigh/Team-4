import pygame
from creature import Creature

class Player(Creature):
    def __init__(self, groups,image,pos):
        super().__init__(groups,image)
        self.right_image = pygame.transform.scale_by(self.right_image,2)
        self.image = self.right_image
        self.base_image = self. right_image
        self.rect = self.image.get_frect(center = (pos))
        self.speed = 600
        self.hop = False
    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        if pygame.key.get_just_pressed()[pygame.K_SPACE] and not self.hop:
            self.hop = True
            self.hop_start_time = pygame.time.get_ticks()
            self.right_image =pygame.image.load("FarmGame/images/rabbit hop.png").convert_alpha()
            self.right_image = pygame.transform.scale_by(self.right_image,2)
        if self.hop == True:
            self.speed = 900
            if self.hop_start_time +500 <  pygame.time.get_ticks():
                self.hop = False
                self.right_image = self.base_image
                self.speed = 300
        self.rect.center += self.direction * self.speed * dt
        self.surf_direction()

        if pygame.mouse.get_just_pressed()[0]:
            print("attack")