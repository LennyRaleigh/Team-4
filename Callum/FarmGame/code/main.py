import pygame
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("Callum/FarmGame/images/rabbit-pixilart.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image,2)
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2()
        self.speed = 600
    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

class Background(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
    def move_bg(self,player,dt):
        for spr in all_sprites:
            if spr != player:
                if hasattr(spr, "rect"):
                    if player.rect.centerx < 250:
                        spr.rect.centerx += player.speed * dt
                    if player.rect.centerx > WINDOW_WIDTH - 250:
                        spr.rect.centerx -= player.speed * dt
                    if player.rect.centery < 250:
                        spr.rect.centery += player.speed * dt
                    if player.rect.centery > WINDOW_HEIGHT - 250:
                        spr.rect.centery -= player.speed * dt
        if player.rect.centerx < 250:
            player.rect.centerx += player.speed * dt
        if player.rect.centerx > WINDOW_WIDTH - 250:
            player.rect.centerx -= player.speed * dt
        if player.rect.centery < 250:
            player.rect.centery += player.speed * dt
        if player.rect.centery > WINDOW_HEIGHT - 250:
            player.rect.centery -= player.speed * dt


class YAwareGroup(pygame.sprite.Group):
    def by_y(self, spr):
        return spr.rect.centery

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_y):
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []

class Enemies(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("Callum/FarmGame/images/rabbit-pixilart.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image,2)
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))


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
placehold = Enemies(all_sprites)
sprites = YAwareGroup((player,placehold))


while running:
    dt = clock.tick()/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill("#2FC66B")
    display_surface.blit(background.image,background.rect)
    #all_sprites.draw(display_surface)
    #display_surface.blit(player.image,player.rect)
    background.move_bg(player,dt)
    sprites.draw(display_surface)
    all_sprites.update(dt)
    pygame.display.update()
pygame.quit()

