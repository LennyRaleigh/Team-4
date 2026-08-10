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


Player.health = 100
Player.max_health = 100
Player.carrots_collected = 0

running = True
farmer_speed = 100

player = Player(pygame.sprite.Group())
# starting position
player.rect.centerx = 400
player.rect.centery = 500

farmer_rect = farmer.get_rect(center=(1000, 420))

class Carrot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load(
            join('FarmGame', 'images', 'carrot.png')
        ).convert_alpha()

        self.image = pygame.transform.scale(self.image, (65, 65))

        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        # Create glow
        glow = pygame.Surface((80, 80), pygame.SRCALPHA)

        pygame.draw.circle(
            glow,
            (255, 255, 0, 100),
            (40, 40),
            35
        )

        # Draw glow
        surface.blit(
            glow,
            (self.rect.centerx - 40, self.rect.centery - 40)
        )

        # Draw carrot
        surface.blit(self.image, self.rect)

def draw_health_bar(surface, health, max_health):
    x = 20
    y = 20
    width = 250
    height = 30

    pygame.draw.rect(
        surface,
        (40, 40, 40),
        (x - 5, y - 5, width + 10, height + 10),
        border_radius=10
    )

    pygame.draw.rect(
        surface,
        (150, 0, 0),
        (x, y, width, height),
        border_radius=8
    )

    health_width = int((health / max_health) * width)

    pygame.draw.rect(
        surface,
        (50, 220, 50),
        (x, y, health_width, height),
        border_radius=8
    )

    pygame.draw.rect(
        surface,
        (255, 255, 255),
        (x, y, width, height),
        2,
        border_radius=8
    )


def draw_carrot_counter(surface, amount):
    font = pygame.font.Font(None, 36)

    carrot = pygame.image.load(
        join('FarmGame', 'images', 'carrot.png')
        ).convert_alpha()

    carrot = pygame.transform.scale(
        carrot, 
        (35, 35)
    )

    surface.blit(carrot, (20, 80))

    text = font.render(
        f"x {amount}/10", 
        True, 
        (255, 255, 255)

    )

    surface.blit(text, (60, 85))


carrots = [

Carrot(600, 400),
Carrot(300, 600),
Carrot(800, 100),
Carrot(1000, 500),
Carrot(200, 300),
Carrot(500, 100),
Carrot(700, 600),
Carrot(400, 300),
Carrot(900, 400),
Carrot(1100, 200),
]

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
    for carrot in carrots[:]:
        if player.rect.colliderect(carrot.rect):
            carrots.remove(carrot)
            Player.carrots_collected += 1

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

    draw_health_bar(
        screen,
        Player.health,
        Player.max_health
    )

    draw_carrot_counter(
        screen,
        player.carrots_collected
    )


    for carrot in carrots:
        carrot.draw(screen)

    pygame.display.update()

    print(farmer_rect.center, player.rect.center)

pygame.quit()