print("FILE STARTED")
import pygame
from os.path import join

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()

swoosh_sound    = pygame.mixer.Sound(join("FarmGame/audio/universfield-swoosh-015-383769.mp3"))
walk_sound      = pygame.mixer.Sound(join("FarmGame/audio/joentnt-walk-on-grass-1-291984.mp3"))
game_over_sound = pygame.mixer.Sound(join("FarmGame/audio/lesiakower-8-bit-game-over-sound-effect-331435.mp3"))
victory_sound   = pygame.mixer.Sound(join("FarmGame/audio/Fortnite Victory Royale - QuickSounds.com.mp3"))
walk_channel    = pygame.mixer.Channel(0)
farm_attack_sound = pygame.mixer.Sound(join("FarmGame/audio/farmer-attack.mp3"))

# load the background image
background = pygame.image.load(join('FarmGame', 'images', 'background.png'))
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

carrot_icon = pygame.image.load(join('FarmGame', 'images', 'carrot.png')).convert_alpha()
carrot_icon = pygame.transform.scale(carrot_icon, (35, 35))


class Player(pygame.sprite.Sprite):
    FRAME_COORDS = [
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        (0, 2), (1, 2),
    ]
    FRAME_SIZE   = 64
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

        self.frames_left = [
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
        self.rect  = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.dodge_direction = pygame.Vector2(1, 0)

        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.dodge_speed = 800
        self.going_right = True
        self.health = 100
        self.max_health = 100
        self.carrots_collected = 0

    def attack(self):
        if self.attack_cooldown <= 0:
            self.attacking       = True
            self.attack_timer    = self.attack_duration
            self.attack_cooldown = self.attack_cooldown_max
            self.enemies_hit     = []

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

    def dodge(self):
        if self.dodge_cooldown <= 0:

            if self.direction.length() > 0:
                self.dodge_direction = self.direction.copy()

            self.dodging        = True
            self.dodge_timer    = 0.25          
            self.dodge_cooldown = 1.0           

    def update(self, dt, enemies):             
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        if self.dodging:
            current_speed = self.dodge_speed
            move_direction = self.dodge_direction
        else:
            current_speed = self.speed
            move_direction = self.direction
        
        self.rect.center += move_direction * current_speed * dt 

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
            self.attacking = False              

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
            for enemy in enemies:
                if enemy not in self.enemies_hit:
                    if attack_rect.colliderect(enemy.rect):
                        enemy.take_damage(10)   
                        self.enemies_hit.append(enemy)

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

        self.walk_sheet = pygame.image.load(
            join("FarmGame", "images", "farmer.sprite.sheet.png")
        ).convert_alpha()

        self.attack_sheet = pygame.image.load(
            join("FarmGame", "images", "farmer.attack.sprite.sheet3.png")
        ).convert_alpha()

        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.1

        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 0.6
        self.attack_cooldown = 0
        self.attack_cooldown_max = 1.0

        self.damage_cooldown = 0
        self.damage_cooldown_max = 1.0

        self.dead   = False
        self.player = player
        self.speed  = 100

        self.health = 200
        self.max_health = 200

        self.hit_flash_timer = 0

        self.walk_frames = self.get_frames(self.walk_sheet,   6, 6)
        self.attack_frames = self.get_frames(self.attack_sheet, 5, 5)

        self.image = self.walk_frames[0]
        self.rect  = self.image.get_frect(center=(1000, 470))

    def get_frames(self, sheet, columns, rows):
        sheet_width, sheet_height = sheet.get_size()
        frame_width  = sheet_width  // columns
        frame_height = sheet_height // rows

        frames = []
        print("Sheet size:", sheet_width, sheet_height)
        print("Frame size:", frame_width, frame_height)

        for row in range(rows):
            for col in range(columns):
                rect = pygame.Rect(
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height
                )
                frame = sheet.subsurface(rect).copy()
                frame = pygame.transform.scale(frame, Farmer.DISPLAY_SIZE)
                frames.append(frame)

        return frames

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash_timer = 0.1

        if self.health <= 0:
            self.dead = True

    def attack(self):
        if self.attack_cooldown <= 0 and not self.attacking:

            self.attacking = True
            self.attack_timer = self.attack_duration
            self.attack_cooldown = self.attack_cooldown_max
            self.frame_index = 0
            self.animation_timer = 0

            farm_attack_sound.play()

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index += 1

            if self.attacking:
                if self.frame_index >= len(self.attack_frames):
                    self.frame_index = len(self.attack_frames) - 1
            else:
                if self.frame_index >= len(self.walk_frames):
                    self.frame_index = 0

        if self.attacking:
            self.image = self.attack_frames[self.frame_index]
        else:
            self.image = self.walk_frames[self.frame_index]

    def update(self, dt, enemies=None):          
        if self.dead:
            return

        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        if self.attacking:
            self.attack_timer -= dt

            if self.attack_timer <= 0:
                self.attacking = False
                self.frame_index = 0           
                self.animation_timer = 0

            self.animate(dt)
            return                                 

        direction = (
            pygame.Vector2(self.player.rect.center)
            - pygame.Vector2(self.rect.center)
        )
        distance = direction.length()

        if distance > 150:
            direction = direction.normalize()
            self.rect.center += direction * self.speed * dt

        elif self.attack_cooldown <= 0:
            self.attack() 
            self.player.take_damage(10)  

            
        if self.attacking:
                self.player.take_damage(10)

        self.animate(dt)

def draw_timer(surface, seconds):
    font = pygame.font.Font(None, 36)
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    text = font.render(f"{mins:02}:{secs:02}", True, (255, 255, 255))
    rect = text.get_frect(topright = (WINDOW_WIDTH - 20, 20))
    surface.blit(text, rect)


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



def reset_game():
    new_player_group = pygame.sprite.Group()
    new_player = Player(new_player_group)
    new_player.rect.center = (400, 525)
    new_player.carrots_collected = 0          

    new_enemy_group = pygame.sprite.Group()
    new_farmer = Farmer(new_enemy_group, new_player)
    new_farmer.rect.center = (1000, 470)
    new_enemies = [new_farmer]

    new_carrots = [
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

    return new_player, new_player_group, new_enemies, new_carrots



player, player_group, enemies, carrots = reset_game()
game_state = 'playing'
alive_time  = 0.0              
running     = True

print("Starting Game")
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "playing":

                alive_time =+ 1 / 60

                if event.key == pygame.K_SPACE:
                    player.dodge()

                if event.key == pygame.K_RETURN:
                    player.attack()
                    swoosh_sound.play()

                if event.key == pygame.K_ESCAPE:
                    game_state = 'paused'
                    walk_channel.stop()

            elif game_state == 'paused':

                if event.key == pygame.K_ESCAPE:
                    game_state = 'playing'

                if event.key == pygame.K_r:
                    player, player_group, enemies, carrots = reset_game()
                    game_state = 'playing'
                    alive_time = 0.0

            elif game_state == 'game_over':      
                   
                if event.key == pygame.K_r:
                    player, player_group, enemies, carrots = reset_game()
                    game_state = 'playing'
                    alive_time = 0.0

                if event.key == pygame.K_ESCAPE:
                
                    running = False

            elif game_state == 'level_complete':    

                if event.key == pygame.K_RETURN:
                    player, player_group, enemies, carrots = reset_game()
                    game_state = 'playing'
                    alive_time = 0.0

                if event.key == pygame.K_ESCAPE:
                    running = False

    
    if game_state == 'playing':
        alive_time += dt

        player.update(dt, enemies)           
        player.rect.clamp_ip(screen.get_rect())

        for enemy in enemies:
            enemy.update(dt)                   

        # collect carrots
        for carrot in carrots[:]:
            if player.rect.colliderect(carrot.rect):
                player.carrots_collected += 1
                player.health = min(player.health + 5, player.max_health)
                carrots.remove(carrot)

        
        if player.carrots_collected >= 10:
            if enemy.health <= 0: 
                game_state = 'level_complete'
            victory_sound.play()

        if player.health <= 0:
            game_state = 'game_over'         
            game_over_sound.play()

    
    screen.fill((30, 30, 30))
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)

    for enemy in enemies:
        if not enemy.dead:
            screen.blit(enemy.image, enemy.rect)
            draw_farmer_health_bar(screen, enemy)

    for carrot in carrots:
        carrot.draw(screen)

    draw_health_bar(screen, player.health, player.max_health)
    draw_carrot_counter(screen, player.carrots_collected)
    draw_timer(screen, alive_time)

    
    if game_state == 'paused':

        font = pygame.font.Font(None, 72)
        small = pygame.font.Font(None, 36)

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))

        screen.blit(overlay, (0, 0))
        screen.blit(font.render("PAUSED", True, (255, 255, 255)),  (540, 280))
        screen.blit(small.render("ESC resume   R restart", True, (200, 200, 200)), (450, 370))

    elif game_state == 'game_over':

        font = pygame.font.Font(None, 72)
        small = pygame.font.Font(None, 36)
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        overlay.fill((0, 0, 0, 160))

        screen.blit(overlay, (0, 0))
        screen.blit(font.render("GAME OVER", True, (220, 40, 40)),  (480, 280))
        screen.blit(small.render("R restart   ESC quit", True, (200, 200, 200)), (490, 370))

    elif game_state == 'level_complete':
        font = pygame.font.Font(None, 72)
        small = pygame.font.Font(None, 36)

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))

        screen.blit(overlay, (0, 0))
        screen.blit(font.render("YOU WIN!", True, (50, 220, 50)),   (520, 280))
        screen.blit(small.render("ENTER play again   ESC quit", True, (200, 200, 200)), (430, 370))

    pygame.display.update()

pygame.quit()