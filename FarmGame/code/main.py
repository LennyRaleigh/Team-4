import pygame
from os.path import join

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game")

background = pygame.image.load(join("images/levelTwo.png"))
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))


class Player:
    def __init__(self, x, y):

        self.original_image = pygame.image.load(join("images/rabbit.png")).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (100, 100))

        self.flipped_image = pygame.transform.flip(self.original_image, True, False)

        self.image = self.original_image

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.image = self.flipped_image

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.image = self.original_image

        if keys[pygame.K_w]:
            self.rect.y -= self.speed

        if keys[pygame.K_s]:
            self.rect.y += self.speed

        self.rect.x = max(0, min(self.rect.x, WINDOW_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, WINDOW_HEIGHT - self.rect.height))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load(join("images/fox.png"))
        self.image = pygame.transform.scale(self.image, (200, 200))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2

    def update(self, player):

        direction = pygame.math.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        )

        if direction.length() > 0:
            direction = direction.normalize()

            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


player = Player(800, 800)

enemies = [
    Enemy(1100, 50),
    Enemy(100, 50),
    Enemy(1100, 600)
]


clock = pygame.time.Clock()
running = True

while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    player.move()

    for enemy in enemies:
        enemy.update(player)

        if player.rect.colliderect(enemy.rect):
            print("Game Over!")
            running = False

    display_surface.blit(background, (0, 0))

    player.draw(display_surface)

    for enemy in enemies:
        enemy.draw(display_surface)


    pygame.display.update()
    clock.tick(60)  


pygame.quit()