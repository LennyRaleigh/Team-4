import pygame

# Start Pygame
pygame.init()

# Create a display window and a clock
screen = pygame.display.set_mode((128, 128))
clock = pygame.time.Clock()

# Create a timer event that occurs every second
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Counter starts at 10
counter = 10

# Convert the counter to a string that takes up 3 characters
text = str(counter).rjust(3)

# Create a font
font = pygame.font.SysFont("Consolas", 30)

# Main game loop
run = True
while run:

    # Check all events
    for event in pygame.event.get():

        # Close the window if the X button is pressed
        if event.type == pygame.QUIT:
            run = False

        # Runs every second because of the timer
        if event.type == pygame.USEREVENT:

            # Decrease the counter by 1
            counter -= 1

            # Update the displayed text while the counter is 0 or greater
            if counter >= 0:
                text = str(counter).rjust(3)

            # Stop the program after displaying 0
            else:
                print("stop file")
                run = False

    # Clear the screen and draw the countdown text
    screen.fill((255, 255, 255))
    screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))

    # Update the display
    pygame.display.flip()

    # Limit the game to 60 frames per second
    clock.tick(60)

# Close Pygame
pygame.quit()