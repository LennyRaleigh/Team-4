import pygame
from os.path import join

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Game')


# load the background image
background = pygame.image.load(join('images', 'background.png'))

# resize it to fit the window
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

player = pygame.image.load(join('images', 'player.png'))
player = pygame.transform.scale(player, (100, 100))

farmer = pygame.image.load(join('images', 'farmer.png'))
farmer = pygame.transform.scale(farmer, (300, 300))

# starting position
player_x = 400
player_y = 477

farmer_x = 1000
farmer_y = 275
running = True

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= 2
    if keys[pygame.K_d]:
        player_x += 2
    if keys[pygame.K_w]:
        player_y -= 2
    if keys[pygame.K_s]:
        player_y += 2
    

    # draw the background image
    display_surface.blit(background, (0,0))

    # draw the player image
    display_surface.blit(player, (player_x, player_y))
    display_surface.blit(farmer, (farmer_x, farmer_y))

    pygame.display.update()

pygame.quit()