import pygame
from os.path import join

pygame.init()
pygame.mixer.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Borris the Bunny")

swoosh_sound = pygame.mixer.Sound(join("FarmGame/audio/universfield-swoosh-015-383769.mp3"))
walk_sound = pygame.mixer.Sound(join("FarmGame/audio/joentnt-walk-on-grass-1-291984.mp3"))
claw_sound = pygame.mixer.Sound(join("FarmGame/audio/daviddumaisaudio-small-monster-attack-195712.mp3"))
game_over_sound = pygame.mixer.Sound(join("FarmGame/audio/lesiakower-8-bit-game-over-sound-effect-331435.mp3"))
victory_sound = pygame.mixer.Sound(join("FarmGame/audio/Fortnite Victory Royale - QuickSounds.com.mp3"))
walk_channel = pygame.mixer.Channel(0)

pygame.mixer.music.load(join("FarmGame/audio/1-03. Subwoofer Lullaby.mp3"))
pygame.mixer.music.set_volume(3)
pygame.mixer.music.play(-1)

background = pygame.image.load(join("FarmGame/images/level2.png")).convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))


class Player(pygame.sprite.Sprite):
    FRAME_COORDS = [
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        (0, 2), (1, 2),
    ]
    FRAME_SIZE = 64
    DISPLAY_SIZE = (100, 100)

    def __init__(self, x, y):
        super().__init__()

        sheet = pygame.image.load(
            join("FarmGame/images/rabbitSprite.png")
        ).convert_alpha()

        self.frames_right = []

        for col, row in self.FRAME_COORDS:
            rect = pygame.Rect(
                col * self.FRAME_SIZE,
                row * self.FRAME_SIZE,
                self.FRAME_SIZE,
                self.FRAME_SIZE
            )

            frame = sheet.subsurface(rect).copy()
            frame = pygame.transform.scale(frame, self.DISPLAY_SIZE)
            self.frames_right.append(frame)

        self.frames_left = [
            pygame.transform.flip(frame, True, False)
            for frame in self.frames_right
        ]

        self.facing_right = True
        self.is_moving = False
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 6

        self.image = self.frames_right[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 5
        self.dodge_speed = 18

        self.max_health = 100
        self.health = 100
        self.carrots_collected = 0

        self.damage_cooldown = 0

        self.knockback = pygame.math.Vector2(0, 0)
        self.knockback_friction = 0.75

        self.dodging = False
        self.dodge_timer = 0
        self.dodge_cooldown = 0

        self.attack_damage = 15
        self.attack_range = 55
        self.attack_size = (55, 70)
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 12
        self.attack_cooldown = 0
        self.attack_cooldown_max = 30
        self.enemies_hit = []

    def move(self):
        keys = pygame.key.get_pressed()

        direction = pygame.math.Vector2(0, 0)

        if keys[pygame.K_a]:
            direction.x -= 1
            self.facing_right = False

        if keys[pygame.K_d]:
            direction.x += 1
            self.facing_right = True

        if keys[pygame.K_w]:
            direction.y -= 1

        if keys[pygame.K_s]:
            direction.y += 1

        self.is_moving = direction.length() > 0

        if self.is_moving:
            direction = direction.normalize()

        speed = self.dodge_speed if self.dodging else self.speed

        self.rect.x += direction.x * speed
        self.rect.y += direction.y * speed

        self.rect.x = max(
            0,
            min(self.rect.x, WINDOW_WIDTH - self.rect.width)
        )

        self.rect.y = max(
            0,
            min(self.rect.y, WINDOW_HEIGHT - self.rect.height)
        )

    def dodge(self):
        if self.dodge_cooldown <= 0:
            self.dodging = True
            self.dodge_timer = 15
            self.dodge_cooldown = 60

    def attack(self):
        if self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_timer = self.attack_duration
            self.attack_cooldown = self.attack_cooldown_max
            self.enemies_hit = []

    def get_attack_rect(self):
        width, height = self.attack_size

        if self.facing_right:
            x = self.rect.right + self.attack_range - width
        else:
            x = self.rect.left - self.attack_range

        y = self.rect.centery - height // 2

        return pygame.Rect(x, y, width, height)

    def take_damage(self, amount, source_rect=None):
        if self.damage_cooldown <= 0 and not self.dodging:
            self.health -= amount
            self.damage_cooldown = 30
            claw_sound.play()

            if source_rect:
                direction = pygame.math.Vector2(
                    self.rect.centerx - source_rect.centerx,
                    self.rect.centery - source_rect.centery
                )
                if direction.length() > 0:
                    self.knockback = direction.normalize() * 12

    def update(self):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        if self.knockback.length() > 0.5:
            self.rect.x += int(self.knockback.x)
            self.rect.y += int(self.knockback.y)
            self.rect.x = max(0, min(self.rect.x, WINDOW_WIDTH - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, WINDOW_HEIGHT - self.rect.height))
            self.knockback *= self.knockback_friction
        else:
            self.knockback = pygame.math.Vector2(0, 0)

        if self.dodge_timer > 0:
            self.dodge_timer -= 1
        else:
            self.dodging = False

        if self.dodge_cooldown > 0:
            self.dodge_cooldown -= 1

        if self.attack_timer > 0:
            self.attack_timer -= 1

            if self.attack_timer <= 0:
                self.attacking = False
        else:
            self.attacking = False

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        frames = self.frames_right if self.facing_right else self.frames_left

        if self.is_moving or self.dodging:
            self.animation_timer += 1

            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(frames)
        else:
            self.frame_index = 0
            self.animation_timer = 0

        self.image = frames[self.frame_index]


class Enemy:
    FRAME_COUNT = 4
    CELL_SIZE = 340
    DISPLAY_SIZE = (200, 200)

    def __init__(self, x, y, spawn_delay=0):
        sheet = pygame.image.load(
            join("FarmGame/images/fox-sheet.png")
        ).convert_alpha()

        self.frames_left = []

        for i in range(self.FRAME_COUNT):
            rect = pygame.Rect(
                i * self.CELL_SIZE,
                0,
                self.CELL_SIZE,
                self.CELL_SIZE
            )

            frame = sheet.subsurface(rect).copy()
            frame = pygame.transform.scale(frame, self.DISPLAY_SIZE)
            self.frames_left.append(frame)

        self.frames_right = [
            pygame.transform.flip(frame, True, False)
            for frame in self.frames_left
        ]

        self.facing_right = True
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8  # lower = faster bob

        self.image = self.frames_right[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3

        self.max_health = 100
        self.health = 100
        self.hit_flash_timer = 0
        self.spawn_delay = spawn_delay * 60

    def take_damage(self, amount):
        self.health -= amount
        self.hit_flash_timer = 8

    def update(self, player, enemies):
        if self.spawn_delay > 0:
            self.spawn_delay -= 1
            return

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
        is_moving = movement.length() > 0

        if is_moving:
            movement = movement.normalize()

            if movement.x > 0.1:
                self.facing_right = True
            elif movement.x < -0.1:
                self.facing_right = False

            self.rect.x += movement.x * self.speed
            self.rect.y += movement.y * self.speed

        frames = self.frames_right if self.facing_right else self.frames_left

        if is_moving:
            self.animation_timer += 1

            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(frames)
        else:
            self.frame_index = 0
            self.animation_timer = 0

        self.image = frames[self.frame_index]

        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1

    def draw(self, surface):
        if self.hit_flash_timer > 0:
            flash = self.image.copy()
            flash.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(flash, self.rect)
        else:
            surface.blit(self.image, self.rect)

        if self.health < self.max_health:
            bar_width = 50
            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.top - 12

            pygame.draw.rect(
                surface,
                (60, 0, 0),
                (bar_x, bar_y, bar_width, 6),
                border_radius=3
            )

            health_width = max(0, (self.health / self.max_health) * bar_width)

            pygame.draw.rect(
                surface,
                (220, 40, 40),
                (bar_x, bar_y, health_width, 6),
                border_radius=3
            )


class Carrot:
    def __init__(self, x, y):
        self.image = pygame.image.load(
            join("FarmGame/images/carrot.png")
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (65, 65)
        )

        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        glow = pygame.Surface((80, 80), pygame.SRCALPHA)

        pygame.draw.circle(
            glow,
            (255, 200, 0, 80),
            (40, 40),
            35
        )

        surface.blit(
            glow,
            (self.rect.x - 8, self.rect.y - 8)
        )

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

    health_width = (health / max_health) * width

    pygame.draw.rect(
        surface,
        (50, 220, 50),
        (x, y, health_width, height),
        border_radius=8
    )

    pygame.draw.rect(
        surface,
        (255, 255, 255),
    pygame.draw.rect(
        surface,
        (255, 255, 255),
        (x, y, width, height),
        2,
        border_radius=8
    )

    surface.blit(ui_border, (x - 20, y - 15))raw_carrot_counter(surface, amount):
    font = pygame.font.Font(None, 36)

    carrot = pygame.image.load(
        join("FarmGame/images/carrot.png")
    ).convert_alpha()

    carrot = pygame.transform.scale(
        carrot,
        (35, 35)
    )

    surface.blit(carrot, (20, 80))

    text = font.render(
        f"x {amount}/7",
        True,
        (255, 255, 255)
    )

    surface.blit(text, (60, 85))


def draw_timer(surface, seconds):
    font = pygame.font.Font(None, 36)
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    text = font.render(f"{mins:02}:{secs:02}", True, (255, 255, 255))
    rect = text.get_rect(topright=(WINDOW_WIDTH - 20, 20))
    surface.blit(text, rect)


def draw_pause_screen(surface):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    surface.blit(overlay, (0, 0))

    title_font = pygame.font.Font(None, 96)
    info_font = pygame.font.Font(None, 40)

    title_text = title_font.render("PAUSED", True, (255, 255, 255))
    title_rect = title_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
    )
    surface.blit(title_text, title_rect)

    prompt_text = info_font.render(
        "Press ESC to Resume or R to Restart",
        True,
        (200, 200, 200)
    )
    prompt_rect = prompt_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)
    )
    surface.blit(prompt_text, prompt_rect)


def draw_level_complete_screen(surface, elapsed_seconds):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    title_font = pygame.font.Font(None, 96)
    info_font = pygame.font.Font(None, 40)

    title_text = title_font.render("LEVEL COMPLETE!", True, (80, 220, 80))
    title_rect = title_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60)
    )
    surface.blit(title_text, title_rect)

    mins = int(elapsed_seconds) // 60
    secs = int(elapsed_seconds) % 60
    time_text = info_font.render(
        f"Time: {mins:02}:{secs:02}",
        True,
        (255, 255, 255)
    )
    time_rect = time_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)
    )
    surface.blit(time_text, time_rect)

    prompt_text = info_font.render(
        "Press ENTER to Continue or ESC to Quit",
        True,
        (200, 200, 200)
    )
    prompt_rect = prompt_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 65)
    )
    surface.blit(prompt_text, prompt_rect)


def draw_game_over_screen(surface, carrots_collected, elapsed_seconds):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    title_font = pygame.font.Font(None, 96)
    info_font = pygame.font.Font(None, 40)

    title_text = title_font.render("GAME OVER", True, (220, 40, 40))
    title_rect = title_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60)
    )
    surface.blit(title_text, title_rect)

    carrots_text = info_font.render(
        f"Carrots collected: {carrots_collected}/7",
        True,
        (255, 255, 255)
    )
    carrots_rect = carrots_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10)
    )
    surface.blit(carrots_text, carrots_rect)

    mins = int(elapsed_seconds) // 60
    secs = int(elapsed_seconds) % 60
    time_text = info_font.render(
        f"Time survived: {mins:02}:{secs:02}",
        True,
        (255, 255, 255)
    )
    time_rect = time_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 55)
    )
    surface.blit(time_text, time_rect)

    prompt_text = info_font.render(
        "Press R to Restart or ESC to Quit",
        True,
        (200, 200, 200)
    )
    prompt_rect = prompt_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
    )
    surface.blit(prompt_text, prompt_rect)


def reset_game():
    new_player = Player(800, 500)

    new_player_group = pygame.sprite.Group()
    new_player_group.add(new_player)

    new_enemies = [
        Enemy(1100, 50),
        Enemy(100, 50, spawn_delay=4),
        Enemy(1100, 600, spawn_delay=8)
    ]

    new_carrots = [
        Carrot(200, 200),
        Carrot(400, 100),
        Carrot(600, 300),
        Carrot(900, 200),
        Carrot(300, 500),
        Carrot(700, 600),
        Carrot(1100, 400)
    ]

    return new_player, new_player_group, new_enemies, new_carrots


player, player_group, enemies, carrots = reset_game()

game_state = "playing"
alive_time = 0.0

clock = pygame.time.Clock()

running = True


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "playing":
                if event.key == pygame.K_SPACE:
                    player.dodge()

                if event.key == pygame.K_RETURN:
                    player.attack()
                    swoosh_sound.play()

                if event.key == pygame.K_ESCAPE:
                    game_state = "paused"
                    walk_channel.stop()

            elif game_state == "paused":
                if event.key == pygame.K_ESCAPE:
                    game_state = "playing"

                if event.key == pygame.K_r:
                    player, player_group, enemies, carrots = reset_game()
                    game_state = "playing"
                    alive_time = 0.0

            elif game_state == "game_over":
                if event.key == pygame.K_r:
                    player, player_group, enemies, carrots = reset_game()
                    game_state = "playing"
                    alive_time = 0.0

                if event.key == pygame.K_ESCAPE:
                    running = False

            elif game_state == "level_complete":
                if event.key == pygame.K_RETURN:
                    player, player_group, enemies, carrots = reset_game()
                    game_state = "playing"
                    alive_time = 0.0

                if event.key == pygame.K_ESCAPE:
                    running = False

    if game_state == "playing":

        alive_time += 1 / 60

        player.move()
        player.update()

        if player.is_moving:
            if not walk_channel.get_busy():
                walk_channel.play(walk_sound, loops=-1)
        else:
            walk_channel.stop()

        for enemy in enemies:

            enemy.update(player, enemies)

            if enemy.spawn_delay <= 0 and player.rect.colliderect(enemy.rect):

                player.take_damage(5, enemy.rect)

                if player.health <= 0:
                    game_state = "game_over"
                    walk_channel.stop()
                    game_over_sound.play()

        if player.attacking:
            attack_rect = player.get_attack_rect()

            for enemy in enemies:
                if enemy.spawn_delay <= 0 and enemy not in player.enemies_hit and attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(player.attack_damage)
                    player.enemies_hit.append(enemy)

        enemies = [enemy for enemy in enemies if enemy.health > 0]

        for carrot in carrots[:]:

            if player.rect.colliderect(carrot.rect):

                player.carrots_collected += 1
                player.health = min(player.health + 5, player.max_health)
                carrots.remove(carrot)

        if not enemies and not carrots:
            game_state = "level_complete"
            walk_channel.stop()
            victory_sound.play()

    display_surface.blit(background, (0, 0))

    for carrot in carrots:
        carrot.draw(display_surface)

    player_group.draw(display_surface)

    if player.attacking:
        attack_rect = player.get_attack_rect()

        swipe = pygame.Surface(attack_rect.size, pygame.SRCALPHA)

        pygame.draw.ellipse(
            swipe,
            (255, 255, 255, 130),
            swipe.get_rect()
        )

        display_surface.blit(swipe, attack_rect)

    for enemy in enemies:
        if enemy.spawn_delay <= 0:
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

    draw_timer(display_surface, alive_time)

    if game_state == "game_over":
        draw_game_over_screen(display_surface, player.carrots_collected, alive_time)

    if game_state == "level_complete":
        draw_level_complete_screen(display_surface, alive_time)

    if game_state == "paused":
        draw_pause_screen(display_surface)

    pygame.display.update()
    clock.tick(60)

pygame.quit()   