import pygame


class Creature(pygame.sprite.Sprite):
    def __init__(self, groups,image):
        super().__init__(groups)
        self.right_image = image
        #self.right_image = pygame.transform.scale_by(self.right_image,2)
        self.image = self.right_image
        self.direction = pygame.math.Vector2()
        self.going_right = True
    #def update(self,dt):
    #    self.direction = self.direction.normalize() if self.direction else self.direction
    #    self.rect.center += self.direction * self.speed * dt
    #    self.surf_direction()
    def surf_direction(self):
        if self.going_right:
            self.image = self.right_image
        else:
            self.image = pygame.transform.flip(self.right_image,True,False)
        if self.direction.x < 0:
            self.going_right = False
        elif self.direction.x > 0:
            self.going_right = True  
        self.mask = pygame.mask.from_surface(self.right_image)