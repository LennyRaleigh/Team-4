import pygame
from os.path import join
import random

all_sprites = pygame.sprite.Group()

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
class Player(Creature):
    def __init__(self, groups,image):
        super().__init__(groups,image)
        self.right_image = pygame.transform.scale_by(self.right_image,2)
        self.image = self.right_image
        self.base_image = self. right_image
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
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

class Background(pygame.sprite.Sprite): #makes backround and moves everything when player moves too far
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
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
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []

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

class Text(pygame.sprite.Sprite):
    def __init__(self, font, pos, text, groups, is_button=False):
        super().__init__(groups)
        self.image = font.render(text,True,("#111314"))
        self.rect = self.image.get_frect(midbottom = pos)
        self.is_button = is_button

        self.font =font
        self.text = text
    def highlight(self,hover):
        self.image = self.font.render(self.text,True,"#111314","#FFFCFC" if hover else None)


pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT =1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Farm Game")
clock = pygame.time.Clock()
running = True
main_menu = True

creature_sprites = pygame.sprite.Group()
text_sprites = pygame.sprite.Group()
background_surf = pygame.image.load("FarmGame/images/barn.png").convert_alpha()

#Text
menu_font = pygame.font.Font(None,60)
button_font= pygame.font.Font(None,40)
title = Text(menu_font,(WINDOW_WIDTH/2,150),"Borris The Bunny",text_sprites)
play_button = Text(button_font,(WINDOW_WIDTH/2,300),"Play Game",text_sprites,True)
settings_button = Text(button_font,(WINDOW_WIDTH/2,400),"Settings",text_sprites,True)
quit_button = Text(button_font,(WINDOW_WIDTH/2,500),"Exit Game",text_sprites,True)

player = Player((all_sprites,creature_sprites),pygame.image.load("FarmGame/images/rabbit.png").convert_alpha())
background = Background(background_surf,all_sprites) #replace background_surf with current level background
for x in range(3):
    Enemies((all_sprites,creature_sprites),pygame.image.load("FarmGame/images/Angry Pig.png").convert_alpha(),5,(random.randint(0, WINDOW_WIDTH),random.randint(0, WINDOW_HEIGHT)))
sprites = YAwareGroup((creature_sprites)) # place any class of object into here EXCEPT background

pygame.mouse.set_visible(False)
cursor_img = pygame.image.load("FarmGame/images/cursor.png").convert_alpha()
cursor_img = pygame.transform.scale_by(cursor_img,3)
cursor_rect = cursor_img.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))



while running:
    dt = clock.tick()/1000

    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
                    main_menu = True
    if main_menu:
        display_surface.fill("#A6D6EB")
        text_sprites.draw(display_surface)

        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_just_pressed()

        display_surface.blit(cursor_img,mouse_pos)

        for button in text_sprites:
            if button.is_button:
                if button.rect.collidepoint(mouse_pos):
                    button.highlight(True)
                else:
                    button.highlight(False)
                
        if play_button.rect.collidepoint(mouse_pos) and mouse_button[0] :
            main_menu = False
        
        if quit_button.rect.collidepoint(mouse_pos) and mouse_button[0] :
            running = False
    
    else:

        display_surface.fill("#2FC66B")
        display_surface.blit(background.image,background.rect)
        background.move_bg(player,dt)
        sprites.draw(display_surface)
        all_sprites.update(dt)
    pygame.display.update()
pygame.quit()

