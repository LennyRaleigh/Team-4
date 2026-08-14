import pygame
import os
_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(_DIR, '..', '..', 'images')

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720


class Carrot:
    def __init__(self, x, y):
        self.image = pygame.image.load(
            os.path.join(IMG_DIR, 'carrot.png')
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


def draw_carrot_counter(surface, amount,max):
    font = pygame.font.Font(None, 36)

    carrot = pygame.image.load(
        os.path.join(IMG_DIR, 'carrot.png')
    ).convert_alpha()

    carrot = pygame.transform.scale(
        carrot,
        (35, 35)
    )

    surface.blit(carrot, (20, 80))

    text = font.render(
        f"x {amount}/{max}",
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
        (x, y, width, height),
        2,
        border_radius=8
    )
