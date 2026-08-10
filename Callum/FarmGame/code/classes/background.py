import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()

pygame.window.get_
class Background(pygame.sprite.Sprite): #makes backround and moves everything when player moves too far
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
    def move_bg(self,player,dt, all_sprites):
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