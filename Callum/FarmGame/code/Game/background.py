import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()


class Background(pygame.sprite.Sprite): #makes backround and moves everything when player moves too far
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        w, h = self.image.get_size()
        if w > WINDOW_WIDTH or h > WINDOW_HEIGHT:
            scalex =   WINDOW_WIDTH / w
            scaley =  WINDOW_HEIGHT / h
            self.image = pygame.transform.scale(self.image, (int(w * scalex), int(h * scaley)))
        elif w < WINDOW_WIDTH or h < WINDOW_HEIGHT:
            scale = min(WINDOW_WIDTH / w, WINDOW_HEIGHT / h)
            self.image = pygame.transform.scale(self.image, (int(w * scale), int(h * scale)))

        x = (WINDOW_WIDTH - self.image.get_width()) // 2
        y = (WINDOW_HEIGHT - self.image.get_height()) // 2
        self.rect = self.image.get_frect(topleft = (x,y))
    def move_bg(self,player,dt, all_sprites): #useless right now but mimics a moving camera
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