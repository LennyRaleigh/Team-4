import pygame
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("Callum/FarmGame/images/rabbit-pixilart.png").convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2()
        self.speed = 300
    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

class Background(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
    def move_bg(self,player,dt):
        if player.rect.centerx < 150:
            player.rect.centerx += player.speed * dt
            self.rect.centerx += player.speed * dt





pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT =1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Farm Game")
clock = pygame.time.Clock()
running = True

background_surf = pygame.image.load("Callum/FarmGame/images/background.png").convert_alpha()
all_sprites = pygame.sprite.Group()
player = Player(all_sprites)
background = Background(background_surf,all_sprites)


while running:
    dt = clock.tick()/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill("#2FC66B")
    all_sprites.draw(display_surface)
    background.move_bg(player,dt)
    all_sprites.update(dt)
    pygame.display.update()
pygame.quit()
