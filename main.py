import pygame
import sys
import kikeriki_game as kg

# Initialize Pygame
pygame.init()

CLOCK = pygame.time.Clock()
FPS = 30

WIDTH, HEIGHT = 1200, 600
COLORS = {
    "background": (30, 30, 30),
    "text": (200, 200, 200),
    "highlight": (255, 100, 100)
}

game = kg.KikerikiGame(no_players=2, n_cards=6)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kikeriki!")

# Main loop
running = True
while running:
    CLOCK.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))  # Fill the screen with black

    font = pygame.font.Font(None, 26)
    y_offset = 20
    for event in game.event_calendar:
        text = font.render(str(event['deck']), True, COLORS["text"])
        screen.blit(text, (20, y_offset))
        y_offset += 40

    pygame.display.flip()  # Update the display
pygame.quit()