import pygame
import os
import random
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, '..', '..', 'audio')
IMG_DIR = os.path.join(BASE_DIR, '..', '..', 'images')
CUT_DIR = os.path.join(BASE_DIR, '..', '..', 'Cutscene')


pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Farm Game")
clock = pygame.time.Clock()
running = True
game_state = "main_menu"
alive_time = 0.0
level = 0

from background import Background
from draw_order import YAwareGroup
import menu
from Enemy import Enemies, give_variables
from Player import Player
from ui import Carrot, draw_health_bar, draw_carrot_counter, draw_game_over_screen, draw_timer, draw_level_complete_screen#, draw_game_complete_screen
from cutscene import play_cutscene


pygame.mixer.init()
swoosh_sound = pygame.mixer.Sound(os.path.join(AUDIO_DIR, 'universfield-swoosh-015-383769.mp3'))
walk_sound = pygame.mixer.Sound(os.path.join(AUDIO_DIR, 'joentnt-walk-on-grass-1-291984.mp3'))
game_over_sound = pygame.mixer.Sound(os.path.join(AUDIO_DIR, 'lesiakower-8-bit-game-over-sound-effect-331435.mp3'))
victory_sound = pygame.mixer.Sound(os.path.join(AUDIO_DIR, 'Fortnite Victory Royale - QuickSounds.com.mp3'))
fox_attack = pygame.mixer.Sound(os.path.join(AUDIO_DIR,'daviddumaisaudio-small-monster-attack-195712.mp3'))
walk_channel = pygame.mixer.Channel(0)

# Level definitions — add new levels by extending this list
LEVELS = [
    {
        'background': 'barn.png',
        'enemy_image': 'Angry Pig.png',
        'enemy_count': 3,
        'enemy_scale': 5,
        'enemy_health': 60,
        'enemy_damage': 3,
        'enemy_speed': 100,
        'enemy_sound': None,
        'background_music': None,
        'carrots': [(200, 200), (400, 100), (600, 300), (900, 200), (300, 500)],
        'cutscene': 'cutscene-1',
    },
    {
        'background': 'level2.png',
        'enemy_image': 'fox.png',
        'enemy_count': 3,
        'enemy_scale': 0.2,
        'enemy_health': 100,
        'enemy_damage': 5,
        'enemy_speed': 150,
        'enemy_sound': fox_attack,
        'background_music': None,
        'carrots': [(100, 150), (500, 200), (700, 400), (300, 600), (1000, 300), (600, 500),(1100, 400)],
        'cutscene': 'cutscene-2',
    },
]

# Sprite groups
all_sprites = pygame.sprite.Group()
creature_sprites = pygame.sprite.Group()

background_surf = pygame.image.load(os.path.join(IMG_DIR, LEVELS[0]['background'])).convert_alpha()
ui_border = pygame.image.load(os.path.join(IMG_DIR,'ui border.png')).convert_alpha()

player = Player(
    (all_sprites, creature_sprites),
    None,
    (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
)
background = Background(background_surf, all_sprites)

sprites = YAwareGroup(creature_sprites)
carrots = []


def load_level(n):
    global all_sprites, creature_sprites, player, background, sprites, carrots, alive_time, background_surf
    data = LEVELS[n - 1]

    all_sprites.empty()
    creature_sprites.empty()

    background_surf = pygame.image.load(os.path.join(IMG_DIR, data['background'])).convert_alpha()

    player.__init__(
        (all_sprites, creature_sprites),
        None,
        (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    )
    background.__init__(background_surf, all_sprites)

    enemy_img = pygame.image.load(os.path.join(IMG_DIR, data['enemy_image'])).convert_alpha()
    for _ in range(data['enemy_count']):
        Enemies(
            (all_sprites, creature_sprites),
            enemy_img,
            data['enemy_scale'],
            (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)),
            LEVELS[level-1]['enemy_health'],
            LEVELS[level-1]['enemy_speed']
        )

    sprites = YAwareGroup(creature_sprites)
    carrots = [Carrot(x, y) for x, y in data['carrots']]
    alive_time = 0.0


def reset_game():
    global alive_time
    load_level(level)
    alive_time = 0.0


# Mouse setup
pygame.mouse.set_visible(False)
cursor_img = pygame.image.load(os.path.join(IMG_DIR, 'cursor.png')).convert_alpha()
cursor_img = pygame.transform.scale_by(cursor_img, 3)
in_level = False

while running:
    dt = clock.tick(60) / 1000
    give_variables(player, creature_sprites)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
            game_state = "main_menu"

        if event.type == pygame.KEYDOWN:
            if game_state == "game_over":
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "playing"
                    walk_channel.stop()
                    in_level = True
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif game_state == "level_complete":
                if event.key == pygame.K_RETURN:
                    level += 1
                    game_state = "cutscene"
                    walk_channel.stop()
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif game_state == "game_complete":
                if event.key == pygame.K_ESCAPE:
                    running = False

        if event.type == pygame.K_RETURN:
            if event.button == 1 and game_state == "playing":
                player.attack()
                swoosh_sound.play()

    if game_state == "main_menu":
        display_surface.fill("#A6D6EB")
        menu.text_sprites.draw(display_surface)

        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_just_pressed()

        display_surface.blit(cursor_img, mouse_pos)

        for button in menu.text_sprites:
            if button.is_button:
                if button.rect.collidepoint(mouse_pos):
                    button.highlight(True)
                else:
                    button.highlight(False)

        if menu.play_button.rect.collidepoint(mouse_pos) and mouse_button[0]:
            if not in_level:
                level = 1
                game_state = "cutscene"
            else: game_state = "playing"

        if menu.quit_button.rect.collidepoint(mouse_pos) and mouse_button[0]:
            running = False

    elif game_state == "cutscene":
        cutscene_dir = os.path.join(CUT_DIR, LEVELS[level - 1]['cutscene'])
        result = play_cutscene(display_surface, cutscene_dir) if level == 1 else "finished"
        clock.tick()  # discard dt that built up during cutscene
        if result == "quit":
            running = False
        elif result == "finished" or result == "skipped":
            load_level(level)
            game_state = "playing"
            in_level = True

    else:
        if game_state == "playing":
            alive_time += dt

            all_sprites.update(dt)

            # walk sound
            if player.direction.length() > 0:
                if not walk_channel.get_busy():
                    walk_channel.play(walk_sound, loops=-1)
            else:
                walk_channel.stop()

            # player-enemy collision
            for enemy in list(creature_sprites):
                if isinstance(enemy, Enemies):
                    if player.rect.colliderect(enemy.rect):
                        player.take_damage(LEVELS[level-1]['enemy_damage'])
                        if LEVELS[level-1]['enemy_sound'] != None:
                            walk_channel.play(LEVELS[level-1]['enemy_sound'])
                        if player.health <= 0:
                            game_state = "game_over"
                            walk_channel.stop()
                            game_over_sound.play()
                            in_level = False

            # player attack hits enemies
            if player.attacking:
                attack_rect = player.get_attack_rect()
                for enemy in list(creature_sprites):
                    if isinstance(enemy, Enemies):
                        if enemy not in player.enemies_hit and attack_rect.colliderect(enemy.rect):
                            enemy.take_damage(player.attack_damage)
                            player.enemies_hit.append(enemy)

            # remove dead enemies
            for enemy in list(creature_sprites):
                if isinstance(enemy, Enemies) and enemy.health <= 0:
                    enemy.kill()

            # carrot collection
            for carrot in carrots[:]:
                if player.rect.colliderect(carrot.rect):
                    player.carrots_collected += 1
                    player.health = min(player.health + 5, player.max_health)
                    carrots.remove(carrot)

            # win condition
            enemies_alive = [e for e in creature_sprites if isinstance(e, Enemies)]
            if not enemies_alive and not carrots:
                walk_channel.stop()
                victory_sound.play()
                #if level < len(LEVELS):
                game_state = "level_complete"
                in_level = False
                #else:
                #    game_state = "game_complete"

        # draw
        display_surface.fill("#2FC66B")
        display_surface.blit(background.image, background.rect)

        for carrot in carrots:
            carrot.draw(display_surface)

        sprites.draw(display_surface)

        if player.attacking:
            attack_rect = player.get_attack_rect()
            swipe = pygame.Surface(attack_rect.size, pygame.SRCALPHA)
            pygame.draw.ellipse(swipe, (255, 255, 255, 130), swipe.get_rect())
            display_surface.blit(swipe, attack_rect)

        for enemy in creature_sprites:
            if isinstance(enemy, Enemies):
                enemy.draw_health_bar(display_surface)

        draw_health_bar(display_surface, player.health, player.max_health,ui_border)
        draw_carrot_counter(display_surface, player.carrots_collected, len(LEVELS[level - 1]['carrots']))
        if level != 1:
            draw_timer(display_surface, alive_time)

        if game_state == "game_over":
            draw_game_over_screen(display_surface, player.carrots_collected, alive_time)

        if game_state == "level_complete":
            draw_level_complete_screen(display_surface, alive_time)

        #if game_state == "game_complete":
        #    draw_game_complete_screen(display_surface, alive_time)

    pygame.display.update()

pygame.quit()
