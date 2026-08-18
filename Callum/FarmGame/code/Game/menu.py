import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()


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


#Text
text_sprites = pygame.sprite.Group()

menu_font = pygame.font.Font(None,60)
button_font= pygame.font.Font(None,40)
title = Text(menu_font,(WINDOW_WIDTH/2,150),"Borris The Bunny",text_sprites)
play_button = Text(button_font,(WINDOW_WIDTH/2,300),"Play Game",text_sprites,True)
settings_button = Text(button_font,(WINDOW_WIDTH/2,400),"Settings",text_sprites,True)
quit_button = Text(button_font,(WINDOW_WIDTH/2,500),"Exit Game",text_sprites,True)
