import os
import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()


def prepare_frame(img):
    """Scale down if larger than window, preserving aspect ratio. Center on screen."""
    w, h = img.get_size()
    if w > WINDOW_WIDTH or h > WINDOW_HEIGHT:
        scale = min(WINDOW_WIDTH / w, WINDOW_HEIGHT / h)
        img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
    x = (WINDOW_WIDTH - img.get_width()) // 2
    y = (WINDOW_HEIGHT - img.get_height()) // 2
    return img, x, y


def play_cutscene(surface, frames_dir, fps=10, skip_key=pygame.K_e):
    frames = sorted([
        f for f in os.listdir(frames_dir)
        if f.endswith('.png') or f.endswith('.jpg')
    ])

    clock = pygame.time.Clock()
    last_frame = None

    for frame_file in frames:
        img = pygame.image.load(os.path.join(frames_dir, frame_file)).convert()
        img, x, y = prepare_frame(img)
        last_frame = (img, x, y)
        surface.fill((0, 0, 0))
        surface.blit(img, (x, y))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == skip_key:
                return "skipped"

        clock.tick(fps)

    # hold last frame until player presses any key
    if last_frame is not None:
        img, x, y = last_frame
        surface.fill((0, 0, 0))
        surface.blit(img, (x, y))
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    waiting = False

    return "finished"
