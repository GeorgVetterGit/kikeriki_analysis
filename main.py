import random
import pygame
import asyncio
import kikeriki_game as kg

# Initialize Pygame
pygame.init()

CLOCK = pygame.time.Clock()
FPS = 30

CHANGE_TIME = 1000  # milliseconds (3000)

WIDTH, HEIGHT = 1200, 600
COLORS = {
    "background": (90, 90, 90),
    "text": (255, 255, 255),
    "highlight": (255, 100, 100)
}

CARD_SIZE = 250
SMALL_CARD_SIZE = 90
SCS = SMALL_CARD_SIZE
dice_size = 100
smiley_size = 70
dot_size = 50
dice_color_size = 70
GUY_SIZE = 70

CARD_NAMES = ['cat', 'dog', 'chicken', 'cow', 'horse', 'sheep']
COLOR_NAMES = ['red', 'green', 'blue', 'yellow', 'purple']
GUY_POS = [(445, 20), (505, 20), (565, 20), (625, 20), (685, 20)]

OFFSET_Y = 10
MID_ODD = HEIGHT // 2 - SCS // 2
MID_EVEN = HEIGHT // 2 - SCS - OFFSET_Y // 2

Y_POS_CARDS = {
    1:[MID_ODD],
    2:[MID_EVEN, 
       MID_EVEN + OFFSET_Y + SCS],
    3:[MID_ODD - OFFSET_Y - SCS, 
       MID_ODD, 
       MID_ODD + OFFSET_Y + SCS],
    4:[MID_EVEN - OFFSET_Y - SCS, 
       MID_EVEN, 
       MID_EVEN + OFFSET_Y + SCS, 
       MID_EVEN + 2*OFFSET_Y + 2*SCS],
    5:[MID_ODD - 2*OFFSET_Y - 2*SCS, 
       MID_ODD - OFFSET_Y - SCS, 
       MID_ODD, 
       MID_ODD + OFFSET_Y + SCS,
       MID_ODD + 2*OFFSET_Y + 2*SCS],
    6:[MID_EVEN - 2*OFFSET_Y - 2*SCS,
       MID_EVEN - OFFSET_Y - SCS, 
       MID_EVEN, 
       MID_EVEN + OFFSET_Y + SCS, 
       MID_EVEN + 2*OFFSET_Y + 2*SCS,
       MID_EVEN + 3*OFFSET_Y + 3*SCS]
}

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
        self.bounce_speed = 0.3

    def update(self, kids):
        if self.no in kids[0].won_cards:
            target_x = 360
            target_w = self.small_size
            target_h = self.small_size
            target_y = Y_POS_CARDS[len(kids[0].won_cards)][kids[0].won_cards.index(self.no)]
        elif self.no in kids[1].won_cards:
            target_x = 750
            target_w = self.small_size
            target_h = self.small_size
            target_y = Y_POS_CARDS[len(kids[1].won_cards)][kids[1].won_cards.index(self.no)]
        else:
            target_x = self.x_pos
            target_w = self.big_size
            target_h = self.big_size
            target_y = self.y_pos

        self.y_pos  += (target_y - self.y_pos)  * self.animation_speed
        self.x_pos  += (target_x - self.x_pos)  * self.animation_speed
        self.w  += (target_w - self.w)  * self.animation_speed
        self.h  += (target_h - self.h)  * self.animation_speed
            
    def draw(self, screen):
        img = pygame.transform.scale(self.image, (self.w, self.h))
        screen.blit(img, (self.x_pos, self.y_pos))
        

card_list = [card(name, i) for i, name in enumerate(CARD_NAMES)]

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

class guy():
    def __init__(self, color, pos):
        self.color = color
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.pos = pos
        self.image = pygame.image.load(f"assets/{self.color}_guy.png")
        self.size = GUY_SIZE
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.animation_speed = 0.3

    def update(self, event, card_colors):
        target_x = self.x_pos
        target_y = self.y_pos
        if event['event'] == 'hits' and event['throw'] == self.color:
            target_x = WIDTH // 2 - CARD_SIZE // 2 + 25 + card_colors.index(event['throw']) * 65
            target_y = 350
        elif event['event'] == 'completed card':
            target_x = self.pos[0]
            target_y = self.pos[1]

        self.x_pos  += (target_x - self.x_pos)  * self.animation_speed
        self.y_pos  += (target_y - self.y_pos)  * self.animation_speed

    def draw(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))
        
for color, pos in zip(COLOR_NAMES, GUY_POS):
    guy_dict[color] = guy(color, pos)


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

    def draw(self, screen):
        if self.marked:
            img = self.marked_image
        else:
            img = self.image
        
        scaled = pygame.transform.smoothscale(img, (int(self.width), int(self.height)))
        screen.blit(scaled, (self.x_pos, self.y_pos))


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
max_reached = False
d_size = dot_size
dice_size_t = dice_size
dice_color_size_n = dice_color_size

# Main loop
running = True

async def main():
    global running, event_idx, event, card_idx, complete, card_colors
    global throw_counter, last_event_change, max_reached, d_size, dice_size_t, dice_color_size_n, game
    global kid_1, kid_2, screen, clock, FPS, WIDTH, HEIGHT, background_image, CARD_SIZE, dot_dict, dice_dict, guy_dict, CHANGE_TIME, dice_image, CARD_NAMES, COLOR_NAMES, GUY_POS, dot_size, dice_color_size, smiley_size, GUY_SIZE, SCS, OFFSET_Y, MID_ODD, MID_EVEN, Y_POS_CARDS, card_list
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
                    kid_1 = player(1, 0, event['player'])
                    kid_2 = player(2, WIDTH - 380, event['player'])
                    card_idx = 0
                    complete = False
                    card_colors = event['deck'][0]
                    throw_counter = 0
                    card_list = [card(name, i) for i, name in enumerate(CARD_NAMES)]
                    max_reached = False
                    last_event_change = 0
                    d_size = dot_size
                    dice_size_t = dice_size
                    dice_color_size_n = dice_color_size
        

        # Update event index based on time
        if pygame.time.get_ticks() - last_event_change >= CHANGE_TIME:
            last_event_change = pygame.time.get_ticks()
            event_idx += 1
            if event_idx >= len(game.event_calendar):
                event_idx = len(game.event_calendar) - 1

        event = game.event_calendar[event_idx]

        # Update card index and colors if a card is completed
        if event['event'] == 'completed card' and not complete:
            if card_idx < len(card_list) - 1:
                card_idx +=1
                card_colors = event['deck'][0]
            else:
                card_idx = len(card_list)
            complete = True
        elif event['event'] != 'completed card':
            complete = False

        kid_1.update(event, card_idx - 1)
        kid_2.update(event, card_idx - 1)

        for c in card_list:
            c.update([kid_1, kid_2])

        for guy in guy_dict.keys():
            guy_dict[guy].update(event, card_colors)

        screen.fill(COLORS["background"])
        screen.blit(background_image, (0, 0))

        # Display kids
        kid_1.draw(screen)
        kid_2.draw(screen)

        # Display card
        for ci in range(min(card_idx, len(card_list)-1),-1,-1):
            card_list[ci].draw(screen)


        # Update dot size for hits event
        if not max_reached and event['event'] == 'hits':
            target_size = (1.2 * dot_size)
            t_size_dice = dice_size * 1.2
            target_d_d_size = dice_color_size * 1.3
        else:
            target_size = dot_size
            t_size_dice = dice_size
            target_d_d_size = 70
        
        d_size += (target_size - d_size) * 0.1
        dice_size_t += (t_size_dice - dice_size_t) * 0.1
        dice_color_size_n += (target_d_d_size - dice_color_size_n) * 0.1

        if d_size >= 1.1 * dot_size:
            max_reached = True

        if event['throw'] is not None:
            dot_dict[event['throw']] = pygame.transform.scale(eval(f"{event['throw']}_image"), (int(d_size), int(d_size)))
            dice_dict[event['throw']] = pygame.transform.scale(eval(f"{event['throw']}_image"), (int(dice_color_size_n), int(dice_color_size_n)))

        dice_image = pygame.transform.scale(dice_image, (int(dice_size_t), int(dice_size_t)))

        if event['event'] != 'hits':
            max_reached = False


        # Display dots on card
        if event['event'] != 'completed card' and event['event'] != 'end_game':
            for i, color in enumerate(card_colors):
                if color == event['throw'] and event['event'] == 'hits':
                    screen.blit(dot_dict[color], (WIDTH // 2 - CARD_SIZE // 2 + 35 + i * 65 - (d_size - dot_size)//2, 360 - (d_size - dot_size)//2))
                else:
                    screen.blit(dot_dict[color], (WIDTH // 2 - CARD_SIZE // 2 + 35 + i * 65, 360))

        if event['event'] != 'rolls die':
            throw_counter = 0

        # Display dice
        screen.blit(dice_image, (WIDTH // 2 - int(dice_size_t) // 2, 450 - (dice_size_t - dice_size)//2))
        if event['event'] == 'rolls die' and throw_counter < 20:
            #show random dice color
            c = random.choice(list(dice_dict.keys()))
            screen.blit(dice_dict[c], (WIDTH // 2 - int(dice_size_t) // 2 + 15, 465))
            throw_counter += 1
        elif event['throw'] is not None:
            screen.blit(dice_dict[event['throw']], (WIDTH // 2 - int(dice_size_t) // 2 + 15, 465 - (dice_size_t - dice_size)//2))

        # Display guys
        if event['event'] != 'end_game':
            for guy in guy_dict.keys():
                guy_dict[guy].draw(screen)

        # print restart in bottom right corner
        text_restart = mid_font.render(f"Press (r) to restart", True, COLORS["text"])
        screen.blit(text_restart, (WIDTH - 200, 560))

        pygame.display.flip()  # Update the display

        await asyncio.sleep(0)

asyncio.run(main())