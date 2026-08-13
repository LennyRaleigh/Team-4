print("FILE STARTED")
import pygame
from os.path import join

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

class Player(pygame.sprite.Sprite):
    FRAME_COORDS = [
     (0,0), (1,0), (2,0),
     (0,1), (1,1), (2,1),
     (0,2), (1,2),

    ]
    FRAME_SIZE = 64
    DISPLAY_SIZE = (100, 100)
   
    def __init__(self, groups):
        super().__init__(groups)
        self.right_image = pygame.image.load(
            join("FarmGame", "images", "sprite-64x64px-8f-sheet.png")
        ).convert_alpha()

        self.frames_right = []

        for col, row in Player.FRAME_COORDS:
            rect = pygame.Rect(
                col * Player.FRAME_SIZE,
                row * Player.FRAME_SIZE,
                Player.FRAME_SIZE,
                Player.FRAME_SIZE
            )

            frame = self.right_image.subsurface(rect).copy()
            frame = pygame.transform.scale(frame, Player.DISPLAY_SIZE)

            self.frames_right.append(frame)

        self.frames_left =[
                pygame.transform.flip(frame, True, False) 
                for frame in self.frames_right
            ]

        self.frame_index = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.damage_cooldown = 0
        self.damage_cooldown_max = 1.0

        self.dodge_timer = 0
        self.dodging = False
        self.dodge_cooldown = 0

        self.attack_timer = 0
        self.attacking = False
        self.enemies_hit = []
        self.attack_cooldown = 0
        self.attack_duration = 0.2
        self.attack_cooldown_max = 0.5
        self.attack_range = 40
        self.attack_size = (100, 60)

        self.facing_right = True

        self.image = self.frames_right[0]

        self.rect = self.image.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )

        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.going_right = True
        self.health = 100
        self.max_health = 100
        self.carrots_collected = 0

    def attack(self):
        if self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_timer = self.attack_duration
            self.attack_cooldown = self.attack_cooldown_max
            self.enemies_hit = []

    def get_attack_rect(self):
        width, height = self.attack_size

        if self.facing_right:
            x = self.rect.right + self.attack_range
        else:
            x = self.rect.left - self.attack_range - width

        y = self.rect.centery - height // 2

        return pygame.Rect(x, y, width, height)

    def take_damage(self, amount):
        if self.damage_cooldown <= 0:
            self.health -= amount
            self.damage_cooldown = self.damage_cooldown_max

            print("Player health", self.health)

            if self.health <= 0:
                print("Game Over")

    def update(self,dt):
            keys = pygame.key.get_pressed()

            self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

            if self.damage_cooldown > 0:
                self.damage_cooldown -= dt

            if self.dodge_timer > 0:
                self.dodge_timer -= dt
            else:
                self.dodging = False

            if self.dodge_cooldown > 0:
                self.dodge_cooldown -= dt
            
            if self.attack_timer > 0:
                self.attack_timer -= dt

                if self.attack_timer <= 0: 
                    self.attacking = False 
            else:
                    self.attacking = 0

            if self.attack_cooldown > 0:
                self.attack_cooldown -= dt

            if self.health <= 0:
                print("Game Over")
                pygame.quit()
                exit()
                
            self.direction = (
            self.direction.normalize() 
            if self.direction
            else self.direction
            )

            if self.attacking:
                attack_rect = self.get_attack_rect()

                if farmer not in self.enemies_hit:
                    if attack_rect.colliderect(farmer.rect):
                        farmer.take_damage(10)
                        self.enemies_hit.append(farmer)

            if self.attack_timer <= 0:
                self.attacking = False

                    

            self.rect.center += self.direction * self.speed * dt

            self.animate(dt)
            self.surf_direction()

    def surf_direction(self):
        if self.direction.x < 0:
            self.going_right = False
            self.facing_right = False

        elif self.direction.x > 0:
            self.going_right = True
            self.facing_right = True

    def animate(self, dt):
        if self.direction.length() > 0:

            self.animation_timer += dt

            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0

                self.frame_index += 1

                if self.frame_index >= len(self.frames_right):
                    self.frame_index = 0

        else:
            self.frame_index = 0

        if self.going_right:
            self.image = self.frames_right[self.frame_index]
        else:
            self.image = self.frames_left[self.frame_index]

class Farmer(pygame.sprite.Sprite):

    DISPLAY_SIZE = (200, 200)

    def __init__(self, groups, player):
        super().__init__(groups)

        self.sprite_sheet = pygame.image.load(
            join("FarmGame", "images", "farmer.sprite.sheet.png")
        ).convert_alpha()

        # The sheet has 6 columns and 6 rows
        sheet_width, sheet_height = self.sprite_sheet.get_size()

        frame_width = sheet_width // 6
        frame_height = sheet_height // 6

        print("Sheet size:", sheet_width, sheet_height)
        print("Frame size:", frame_width, frame_height)

        self.frames = []

        for row in range(6):
            for col in range(6):

                rect = pygame.Rect(
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height
                )

                frame = self.sprite_sheet.subsurface(rect).copy()

                frame = pygame.transform.scale(
                    frame,
                    Farmer.DISPLAY_SIZE
                )

                self.frames.append(frame)

        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.damage_cooldown = 0
        self.damage_cooldown_max = 1.0

        self.image = self.frames[0]
        self.dead = False

        self.rect = self.image.get_frect(
            center=(1000, 470)
        )

        self.player = player
        self.speed = 100

        self.health = 120
        self.max_health = 120

        self.hit_flash_timer = 0

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash_timer = 0.1

        if self.health <= 0:
            self.dead = True

    def animate(self, dt):
        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

        self.image = self.frames[self.frame_index]

    def update(self, dt):

        if self.dead:
            return
        
        direction = (
            pygame.Vector2(self.player.rect.center)
            - pygame.Vector2(self.rect.center)
        )

        if direction.length() > 0:
            direction = direction.normalize()

            self.rect.center += (
                direction * self.speed * dt
            )

        if self.rect.colliderect(self.player.rect):
            self.player.take_damage(10)

        self.animate(dt)

running = True

player = Player(pygame.sprite.Group())

# starting position
player.rect.centerx = 400
player.rect.centery = 525

farmer = Farmer(pygame.sprite.Group(), player)

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

def draw_farmer_health_bar(surface, farmer):
    width = 100
    height = 10

    x = farmer.rect.centerx - width // 2
    y = farmer.rect.top - 20

    pygame.draw.rect(
        surface,
        (50, 50, 50),
        (x, y, width, height)
    )

    health_width = int(
        (farmer.health / farmer.max_health) * width
    )

    pygame.draw.rect(
        surface,
        (220, 40, 40),
        (x, y, health_width, height)
    )

    pygame.draw.rect(
        surface,
        (225, 225, 225),
        (x, y, width, height),
        1
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.attack()
   

    # Update player first
    player.update(dt)
    print(player.rect.center)

    # Keep player inside the window
    player.rect.clamp_ip(screen.get_rect())
    for carrot in carrots[:]:
        if player.rect.colliderect(carrot.rect):
            carrots.remove(carrot)
            player.carrots_collected += 1


    farmer.update(dt)

    # Draw
    screen.fill((30, 30, 30))
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)

    if not farmer.dead:
        screen.blit(farmer.image, farmer.rect)
        draw_farmer_health_bar(screen, farmer)

    draw_health_bar(
        screen,
        player.health,
        player.max_health
    )

    draw_carrot_counter(
        screen,
        player.carrots_collected
    )


    for carrot in carrots:
        carrot.draw(screen)

    pygame.display.update()

    print(farmer.rect.center, player.rect.center)

pygame.quit()

