import pygame

if __name__ != "__main__":
    WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()
else:

    pygame.init()
    WINDOW_WIDTH, WINDOW_HEIGHT =1280, 720
    display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("Farm Game")
    clock = pygame.time.Clock()
    running = True
    main_menu = True


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


if __name__ == "__main__":






    pygame.mouse.set_visible(False)
    cursor_img = pygame.image.load("images/cursor.png").convert_alpha()
    cursor_img = pygame.transform.scale_by(cursor_img,3)
    cursor_rect = cursor_img.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

    while running:

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

        pygame.display.update()
    pygame.quit()