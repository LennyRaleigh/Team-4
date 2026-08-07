import pygame
from os.path import join
from player_bg import Player
import math

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()

# load the background image
background = pygame.image.load(join('FarmGame', 'images', 'background.png'))

# resize it to fit the window
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))


farmer = pygame.image.load(join('FarmGame', 'images', 'farmer.png'))
farmer = pygame.transform.scale(farmer, (300, 300))

player_x = 400
player_y = 477

player_width = 25
player_height = 25

player_x = max(0, min(player_x, WINDOW_WIDTH - player_width))
player_y = max(0, min(player_y, WINDOW_HEIGHT - player_height))


farmer_x = 1000
farmer_y = 275
running = True
farmer_speed = 0.5


player = Player(pygame.sprite.Group())
# starting position
player.rect.centerx = 400
player.rect.centery = 500


while running:
    dt = clock.tick()/1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update the player
    player.update(dt)

    #Keep the player within the window boundaries
    player.rect.clamp_ip(screen.get_rect())

    screen.fill((30, 30 ,30))


    # draw the background image
    screen.blit(background, (0,0))

    # draw the player image
    screen.blit(player.image, (player.rect))
    screen.blit(farmer, (farmer_x, farmer_y))

    pygame.display.update()

pygame.quit()