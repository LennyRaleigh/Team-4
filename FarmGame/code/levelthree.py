print("FILE STARTED")
import pygame
from os.path import join
from player_bg import Player

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


running = True
farmer_speed = 100

player = Player(pygame.sprite.Group())
# starting position
player.rect.centerx = 400
player.rect.centery = 500

farmer_rect = farmer.get_rect(center=(1000, 275))


print("Starting Game")
while running:
    dt = clock.tick(60) / 1000
    print("loop running")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   

    # Update player first
    player.update(dt)
    print(player.rect.center)

    # Keep player inside the window
    player.rect.clamp_ip(screen.get_rect())
    # Make farmer follow player
    direction = pygame.Vector2(player.rect.center) - farmer_rect.center

    if direction.length() > 0:
        direction = direction.normalize()
        farmer_rect.center += direction * farmer_speed * dt

    # Draw
    screen.fill((30, 30, 30))
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)
    screen.blit(farmer, farmer_rect)

    pygame.display.update()

    print(farmer_rect.center, player.rect.center)

pygame.quit()