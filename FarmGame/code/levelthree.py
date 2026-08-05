import pygame
from os.path import join

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Game')

# load the background image
background = pygame.image.load(join('FarmGame', 'images', 'background.png'))

# resize it to fit the window
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

player = pygame.image.load(join('FarmGame', 'images', 'rabbit.png'))
player = pygame.transform.scale(player, (100, 100))

# starting position
player_x = 400
player_y = 480

running = True

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the background image
    display_surface.blit(background, (0,0))

    # draw the player image
    display_surface.blit(player, (player_x, player_y))

    pygame.display.update()

pygame.quit()