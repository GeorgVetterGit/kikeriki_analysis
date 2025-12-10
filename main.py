import random
import pygame
import kikeriki_game as kg

# Initialize Pygame
pygame.init()

CLOCK = pygame.time.Clock()
FPS = 30

CHANGE_TIME = 500  # milliseconds (3000)

WIDTH, HEIGHT = 1200, 600
COLORS = {
    "background": (90, 90, 90),
    "text": (255, 255, 255),
    "highlight": (255, 100, 100)
}

CARD_SIZE = 250
SMALL_CARD_SIZE = 90
dice_size = 100
smiley_size = 70
dot_size = 50
dice_color_size = 70
guy_size = 70
hit_size = (100,50)
miss_size = (100,50)

dot_dict = {}
dice_dict = {}
guy_dict = {}

class card():
    def __init__(self, card, no):
        self.card = card
        self.no = no
        self.image = pygame.image.load(f"assets/{self.card}_card.png")

        self.big_size = CARD_SIZE
        self.small_size = SMALL_CARD_SIZE

        self.w = self.big_size
        self.h = self.big_size
        self.x_pos = WIDTH // 2 - self.big_size // 2
        self.y_pos = 180
        self.animation_speed = 0.1

    def update(self, event, kids):
        if self.no in kids[0].won_cards:
            target_x = 360
            target_w = self.small_size
            target_h = self.small_size
        elif self.no in kids[1].won_cards:
            target_x = 750
            target_w = self.small_size
            target_h = self.small_size
        else:
            target_x = self.x_pos
            target_w = self.big_size
            target_h = self.big_size


        #self.y_pos  += (target_y - self.y_pos)  * self.animation_speed
        self.x_pos  += (target_x - self.x_pos)  * self.animation_speed
        self.w  += (target_w - self.w)  * self.animation_speed
        self.h  += (target_h - self.h)  * self.animation_speed
            

    def draw(self, screen):
        img = pygame.transform.scale(self.image, (self.w, self.h))
        screen.blit(img, (self.x_pos, self.y_pos))
        
card_names = ['cat', 'dog', 'chicken', 'cow', 'horse', 'sheep']
card_list = [card(name, i) for i, name in enumerate(card_names)]

card_idx = 0
complete = False

# load dice image
dice_image = pygame.image.load("assets/dice.png")
dice_image = pygame.transform.scale(dice_image, (dice_size, dice_size))

# load color images
red_image = pygame.image.load("assets/red.png")
green_image = pygame.image.load("assets/green.png")
blue_image = pygame.image.load("assets/blue.png")
yellow_image = pygame.image.load("assets/yellow.png")
purple_image = pygame.image.load("assets/purple.png")

dot_dict['purple'] = pygame.transform.scale(purple_image, (dot_size, dot_size))
dot_dict['yellow'] = pygame.transform.scale(yellow_image, (dot_size, dot_size))
dot_dict['blue'] = pygame.transform.scale(blue_image, (dot_size, dot_size))
dot_dict['green'] = pygame.transform.scale(green_image, (dot_size, dot_size))
dot_dict['red'] = pygame.transform.scale(red_image, (dot_size, dot_size))

# load smiley image
smiley_image = pygame.image.load("assets/smiley.png")

dice_dict['purple'] = pygame.transform.scale(purple_image, (dice_color_size, dice_color_size))
dice_dict['yellow'] = pygame.transform.scale(yellow_image, (dice_color_size, dice_color_size))
dice_dict['blue'] = pygame.transform.scale(blue_image, (dice_color_size, dice_color_size))
dice_dict['green'] = pygame.transform.scale(green_image, (dice_color_size, dice_color_size))
dice_dict['red'] = pygame.transform.scale(red_image, (dice_color_size, dice_color_size))
dice_dict['smiley'] = pygame.transform.scale(smiley_image, (smiley_size, smiley_size))

# load guy images
blue_guy_image = pygame.image.load("assets/blue_guy.png")
green_guy_image = pygame.image.load("assets/green_guy.png")
red_guy_image = pygame.image.load("assets/red_guy.png")
yellow_guy_image = pygame.image.load("assets/yellow_guy.png")
purple_guy_image = pygame.image.load("assets/purple_guy.png")

def set_guy_pos():
    guy_dict['blue'] = {'image': pygame.transform.scale(blue_guy_image, (guy_size, guy_size)), 'pos': (445, 20)}
    guy_dict['green'] = {'image': pygame.transform.scale(green_guy_image, (guy_size, guy_size)), 'pos': (505, 20)}
    guy_dict['red'] = {'image': pygame.transform.scale(red_guy_image, (guy_size, guy_size)), 'pos': (565, 20)}
    guy_dict['yellow'] = {'image': pygame.transform.scale(yellow_guy_image, (guy_size, guy_size)), 'pos': (625, 20)}
    guy_dict['purple'] = {'image': pygame.transform.scale(purple_guy_image, (guy_size, guy_size)), 'pos': (685, 20)}
    return guy_dict

guy_dict = set_guy_pos()


class player():
    def __init__(self, no, x_pos, curr, size_factor = 0.2):
        self.no = no - 1
        self.sf = size_factor

        self.marked = int(curr) == self.no
        self.animation_speed = 0.5

        self.score = 0

        self.image = pygame.image.load(f"assets/kid_{no}_side.png")
        self.marked_image = pygame.image.load(f"assets/kid_{no}_marked.png")

        self.base_w = 330
        self.base_h = 400
        self.base_y = 110
        self.base_x = x_pos

        self.x_pos = self.get_target_x()
        self.y_pos = self.get_target_y()

        self.width = self.base_w * self.get_factor()
        self.height = self.base_h * self.get_factor()

        self.won_cards = []

    def get_factor(self):
        return 1 + (self.sf/2) if self.marked else 1 - (self.sf/2)

    def get_target_y(self):
        factor = 1 - (self.sf/2) if self.marked else 1 + (self.sf/2)
        return self.base_y * factor
    
    def get_target_x(self):
        if self.no == 0:
            factor = 1 - (self.sf/2) if self.marked else 1 + (self.sf/2)
        else:
            factor = 1.02 if self.marked else 1 + (self.sf/2)
        return self.base_x * factor


    def update(self, event, card_idx):
        self.marked = int(event['player']) == self.no

        target_w = self.base_w * self.get_factor()
        target_h = self.base_h * self.get_factor()
        target_y = self.get_target_y()
        target_x = self.get_target_x()

        self.width  += (target_w - self.width)  * self.animation_speed
        self.height += (target_h - self.height) * self.animation_speed
        self.y_pos  += (target_y - self.y_pos)  * self.animation_speed
        self.x_pos  += (target_x - self.x_pos)  * self.animation_speed

        if (event['event'] == 'completed card' or event['event'] == 'end_game') and event['player'] == self.no:
            if card_idx not in self.won_cards:
                self.won_cards.append(card_idx)
                print(self.won_cards)


    def draw(self, screen):
        if self.marked:
            img = self.marked_image
        else:
            img = self.image
        
        scaled = pygame.transform.smoothscale(img, (int(self.width), int(self.height)))
        screen.blit(scaled, (self.x_pos, self.y_pos))



# load hit and miss
hit_image = pygame.image.load("assets/hit.png")
hit_image = pygame.transform.scale(hit_image, hit_size)
miss_image = pygame.image.load("assets/miss.png")
miss_image = pygame.transform.scale(miss_image, miss_size)

# load background
background_image = pygame.image.load("assets/background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

game = kg.KikerikiGame(no_players=2, n_cards=6)
event_idx = 0

event = game.event_calendar[event_idx]
card_colors = event['deck'][0]

kid_1 = player(1, 0, event['player'])
kid_2 = player(2, WIDTH - 380, event['player'])

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kikeriki!")

log_font = pygame.font.Font(None, 18)
font = pygame.font.Font(None, 85)
mid_font = pygame.font.Font(None, 30)

throw_counter = 0

last_event_change = 0

# Main loop
running = True
while running:
    CLOCK.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game = kg.KikerikiGame(no_players=2, n_cards=6)
                event_idx = 0
                event = game.event_calendar[event_idx]
                card_idx = 0
                complete = False
                card_colors = event['deck'][0]
                guy_dict = set_guy_pos()
                throw_counter = 0
                # reset game time
    

    # Update event index based on time
    if pygame.time.get_ticks() - last_event_change >= CHANGE_TIME:
        last_event_change = pygame.time.get_ticks()
        event_idx += 1
        if event_idx >= len(game.event_calendar):
            event_idx = len(game.event_calendar) - 1

    event = game.event_calendar[event_idx]

    # Update card index and colors if a card is completed
    if event['event'] == 'completed card' and not complete:
        card_idx += 1
        if card_idx > len(card_list):
            card_idx -=1
        else:
            card_colors = event['deck'][0]
            guy_dict = set_guy_pos()
        complete = True
    elif event['event'] != 'completed card':
        complete = False

    if event['event'] == 'end_game':
        kid_1.update(event, card_idx)
        kid_2.update(event, card_idx)
    else:
        kid_1.update(event, card_idx - 1)
        kid_2.update(event, card_idx - 1)

    for c in card_list:
        c.update(event, [kid_1, kid_2])

    # set guy position on card if hit
    if event['event'] == 'hits':
        guy_pos = guy_dict[event['throw']]['pos']
        guy_dict[event['throw']]['pos'] = (WIDTH // 2 - CARD_SIZE // 2 + 25 + card_colors.index(event['throw']) * 65, 350)

    #pygame.draw.rect(screen, COLORS["background"], (0, 0, WIDTH, HEIGHT))
    screen.fill(COLORS["background"])
    screen.blit(background_image, (0, 0))

    # Display kids
    kid_1.draw(screen)
    kid_2.draw(screen)

    #Score display
    player_1_score = font.render(str(event['scores'][0]), True, COLORS["text"])
    screen.blit(player_1_score, (100, 20))
    player_2_score = font.render(str(event['scores'][1]), True, COLORS["text"])
    screen.blit(player_2_score, (1100, 20))

    # Display card
    for ci in range(card_idx+1):
        card_list[ci].draw(screen)

    # Display dots on card
    for i, color in enumerate(card_colors):
        screen.blit(dot_dict[color], (WIDTH // 2 - CARD_SIZE // 2 + 35 + i * 65, 360))

    if event['event'] != 'rolls die':
        throw_counter = 0

    # Display dice
    screen.blit(dice_image, (WIDTH // 2 - dice_size // 2, 450))
    if event['event'] == 'rolls die' and throw_counter < 30:
        #show random dice color
        c = random.choice(list(dice_dict.keys()))
        screen.blit(dice_dict[c], (WIDTH // 2 - dice_size // 2 + 15, 465))
        throw_counter += 1
    elif event['throw'] is not None:
        screen.blit(dice_dict[event['throw']], (WIDTH // 2 - dice_size // 2 + 15, 465))

    # Display hit or miss
    if event['event'] == 'hits':
        screen.blit(hit_image, (WIDTH // 2 - dice_size // 2 + 150, 450))
    elif event['event'] == 'misses':
        screen.blit(miss_image, (WIDTH // 2 - dice_size // 2 + 150, 450))

    # Display guys
    for guy in guy_dict.keys():
        screen.blit(guy_dict[guy]['image'], guy_dict[guy]['pos'])

    # Display event details in the horizonatl middle of the screen
    y_offset = 560
    if event['event'] != 'end_game':
        t_str = f'Player {int(event['player']) + 1} {event['event']}{' and gets '+event['throw']+'.' if event['event'] == 'rolls die' else "."}{' He chooses '+game.event_calendar[event_idx+1]['throw']+'.' if event['throw'] == 'smiley' else ""}'
    else:
        t_str = 'Game over!'
    text = mid_font.render(t_str, True, COLORS["text"])

    #get length of text to center text
    text_width = text.get_width()
    text_x = WIDTH // 2 - text_width // 2
    screen.blit(text, (text_x, y_offset))

    # print restart in bottom right corner
    text_restart = mid_font.render(f"Press (r) to restart", True, COLORS["text"])
    screen.blit(text_restart, (WIDTH - 200, y_offset))
    

    pygame.display.flip()  # Update the display

pygame.quit()