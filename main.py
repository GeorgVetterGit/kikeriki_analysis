import pygame
import sys
import kikeriki_game as kg

# Initialize Pygame
pygame.init()

CLOCK = pygame.time.Clock()
FPS = 30

CHANGE_TIME = 1000  # milliseconds

WIDTH, HEIGHT = 1200, 600
COLORS = {
    "background": (30, 30, 30),
    "text": (200, 200, 200),
    "highlight": (255, 100, 100)
}

game = kg.KikerikiGame(no_players=2, n_cards=6)
event_idx = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kikeriki!")

log_font = pygame.font.Font(None, 18)
font = pygame.font.Font(None, 55)

# Main loop
running = True
while running:
    CLOCK.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))  # Fill the screen with black

    # Update event index based on time
    event_idx = min((pygame.time.get_ticks() // CHANGE_TIME), len(game.event_calendar) - 1)

    event = game.event_calendar[event_idx]
    pygame.draw.rect(screen, COLORS["background"], (0, 0, WIDTH, HEIGHT))

    #Score display
    player_1_score = font.render(str(event['scores'][0]), True, COLORS["text"])
    screen.blit(player_1_score, (100, 20))
    player_2_score = font.render(str(event['scores'][1]), True, COLORS["text"])
    screen.blit(player_2_score, (1100, 20))


    # Display event details
    y_offset = 570
    text = log_font.render(f"Event: {event['event']} | Player: {event['player']} | Throw: {event['throw']} | Scores: {event['scores']}", True, COLORS["text"])
    screen.blit(text, (20, y_offset))

    pygame.display.flip()  # Update the display
pygame.quit()