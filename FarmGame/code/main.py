import pygame
from os.path import join

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Borris the Bunny")

background = pygame.image.load(join("images/level-2.png"))
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))


class Player:
    def __init__(self, x, y):
        self.original_image = pygame.image.load(join("images/rabbit.png")).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (100, 100))

        self.flipped_image = pygame.transform.flip(self.original_image, True, False)
        self.image = self.original_image

        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 5
        self.dodge_speed = 18

        self.max_health = 100
        self.health = 100
        self.carrots_collected = 0

        self.damage_cooldown = 0

        self.dodging = False
        self.dodge_timer = 0
        self.dodge_cooldown = 0


    def move(self):
        keys = pygame.key.get_pressed()

        direction = pygame.math.Vector2(0, 0)

        if keys[pygame.K_a]:
            direction.x -= 1
            self.image = self.flipped_image

        if keys[pygame.K_d]:
            direction.x += 1
            self.image = self.original_image

        if keys[pygame.K_w]:
            direction.y -= 1

        if keys[pygame.K_s]:
            direction.y += 1


        if direction.length() > 0:
            direction = direction.normalize()

        speed = self.dodge_speed if self.dodging else self.speed

        self.rect.x += direction.x * speed
        self.rect.y += direction.y * speed

        self.rect.x = max(0, min(self.rect.x, WINDOW_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, WINDOW_HEIGHT - self.rect.height))


    def dodge(self):
        if self.dodge_cooldown <= 0:
            self.dodging = True
            self.dodge_timer = 15
            self.dodge_cooldown = 60


    def take_damage(self, amount):
        if self.damage_cooldown <= 0 and not self.dodging:
            self.health -= amount
            self.damage_cooldown = 30


    def update(self):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        if self.dodge_timer > 0:
            self.dodge_timer -= 1
        else:
            self.dodging = False

        if self.dodge_cooldown > 0:
            self.dodge_cooldown -= 1


    def draw(self, surface):
        surface.blit(self.image, self.rect)



class Enemy:
    def __init__(self, x, y):
        self.image = pygame.image.load(join("images/fox.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3


    def update(self, player, enemies):

        direction = pygame.math.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        )

        if direction.length() > 0:
            direction = direction.normalize()


        separation = pygame.math.Vector2(0, 0)

        for enemy in enemies:
            if enemy != self:

                distance = pygame.math.Vector2(
                    self.rect.centerx - enemy.rect.centerx,
                    self.rect.centery - enemy.rect.centery
                )

                if 0 < distance.length() < 150:
                    separation += distance.normalize()


        movement = direction + separation * 0.8

        if movement.length() > 0:
            movement = movement.normalize()

            self.rect.x += movement.x * self.speed
            self.rect.y += movement.y * self.speed


    def draw(self, surface):
        surface.blit(self.image, self.rect)



class Carrot:
    def __init__(self, x, y):

        self.image = pygame.image.load(join("images/carrot.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (65, 65))

        self.rect = self.image.get_rect(topleft=(x, y))


    def draw(self, surface):

        glow = pygame.Surface((80, 80), pygame.SRCALPHA)

        pygame.draw.circle(
            glow,
            (255, 200, 0, 80),
            (40, 40),
            35
        )

        surface.blit(glow, (self.rect.x - 8, self.rect.y - 8))
        surface.blit(self.image, self.rect)



def draw_health_bar(surface, health, max_health):

    x = 20
    y = 20
    width = 250
    height = 30

    pygame.draw.rect(
        surface,
        (40,40,40),
        (x-5,y-5,width+10,height+10),
        border_radius=10
    )

    pygame.draw.rect(
        surface,
        (150,0,0),
        (x,y,width,height),
        border_radius=8
    )

    health_width = (health / max_health) * width

    pygame.draw.rect(
        surface,
        (50,220,50),
        (x,y,health_width,height),
        border_radius=8
    )

    pygame.draw.rect(
        surface,
        (255,255,255),
        (x,y,width,height),
        2,
        border_radius=8
    )



def draw_carrot_counter(surface, amount):

    font = pygame.font.Font(None,36)

    carrot = pygame.image.load(join("images/carrot.png")).convert_alpha()
    carrot = pygame.transform.scale(carrot,(35,35))

    surface.blit(carrot,(20,80))

    text = font.render(
        f"x {amount}/7",
        True,
        (255,255,255)
    )

    surface.blit(text,(60,85))



player = Player(800,500)


enemies = [
    Enemy(1100,50),
    Enemy(100,50),
    Enemy(1100,600)
]


carrots = [
    Carrot(200,200),
    Carrot(400,100),
    Carrot(600,300),
    Carrot(900,200),
    Carrot(300,500),
    Carrot(700,600),
    Carrot(1100,400)
]


clock = pygame.time.Clock()

running = True


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                player.dodge()


    player.move()
    player.update()


    for enemy in enemies:

        enemy.update(player,enemies)

        if player.rect.colliderect(enemy.rect):

            player.take_damage(1)

            if player.health <= 0:
                running = False



    for carrot in carrots[:]:

        if player.rect.colliderect(carrot.rect):

            player.carrots_collected += 1
            carrots.remove(carrot)



    display_surface.blit(background,(0,0))


    for carrot in carrots:
        carrot.draw(display_surface)


    player.draw(display_surface)


    for enemy in enemies:
        enemy.draw(display_surface)


    draw_health_bar(
        display_surface,
        player.health,
        player.max_health
    )


    draw_carrot_counter(
        display_surface,
        player.carrots_collected
    )


    pygame.display.update()
    clock.tick(60)


pygame.quit()