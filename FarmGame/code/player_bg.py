import pygame
from os.path import join


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.right_image = pygame.image.load("FarmGame/images/rabbit-pixilart.png").convert_alpha()
        self.right_image = pygame.transform.scale_by(self.right_image,2)
        self.image = self.right_image
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2) if __name__ == "__main__" else (1280/2,720/2))
        self.direction = pygame.math.Vector2()
        self.speed = 600
        self.going_right = True
    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        self.surf_direction()
    def surf_direction(self):
        if self.going_right:
            self.image = self.right_image
        else:
            self.image = pygame.transform.flip(self.right_image,True,False)
        if self.direction.x < 0:
            self.going_right = False
        elif self.direction.x > 0:
            self.going_right = True

class Background(pygame.sprite.Sprite): #makes backround and moves everything when player moves too far
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2) if __name__ == "__main__" else (1280/2,720/2))
    def move_bg(self,player,dt):
        for spr in all_sprites:
            if spr != player:
                if hasattr(spr, "rect"):
                    if player.rect.centerx < WINDOW_WIDTH* 0.33:
                        spr.rect.centerx += player.speed * dt
                    if player.rect.centerx > WINDOW_WIDTH*0.66:
                        spr.rect.centerx -= player.speed * dt
                    if player.rect.centery < WINDOW_HEIGHT *0.33:
                        spr.rect.centery += player.speed * dt
                    if player.rect.centery > WINDOW_HEIGHT * 0.66:
                        spr.rect.centery -= player.speed * dt
        if player.rect.centerx < WINDOW_WIDTH *0.33:
            player.rect.centerx += player.speed * dt
        if player.rect.centerx > WINDOW_WIDTH * 0.66:
            player.rect.centerx -= player.speed * dt
        if player.rect.centery < WINDOW_HEIGHT * 0.33:
            player.rect.centery += player.speed * dt
        if player.rect.centery > WINDOW_HEIGHT *0.66:
            player.rect.centery -= player.speed * dt


class YAwareGroup(pygame.sprite.Group): #draws sprites under or over others depending on y coord
    def by_y(self, spr):
        return spr.rect.centery

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_y):
            print("u")
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []

class Enemies(pygame.sprite.Sprite): #placeholder replace with fully made enemy class
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("Callum/FarmGame/images/Tree.png").convert_alpha()
        self.image = pygame.transform.scale_by(self.image,1)
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

if __name__ == "__main__" :
    pygame.init()
    WINDOW_WIDTH, WINDOW_HEIGHT =1280, 720
    display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("Farm Game")
    clock = pygame.time.Clock()
    running = True

    background_surf = pygame.image.load("FarmGame/images/background.png").convert_alpha()
    all_sprites = pygame.sprite.Group()
    player = Player(all_sprites)
    background = Background(background_surf,all_sprites) #replace background_surf with current level background
    placehold = Enemies(all_sprites)
    sprites = YAwareGroup((player,placehold)) # place any class of object into here EXCEPT background


    while running:
        dt = clock.tick()/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display_surface.fill("#2FC66B")
        display_surface.blit(background.image,background.rect)
        background.move_bg(player,dt)
        sprites.draw(display_surface)
        all_sprites.update(dt)
        pygame.display.update()
    pygame.quit()

