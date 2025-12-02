import random

class KikerikiGame:

    def __init__(self, no_players=2, n_cards=6):
        self.no_players = no_players
        self.n_cards = n_cards
        self.dice = ['red', 'green', 'blue', 'yellow', 'purple', 'smiley']
        self.colors = ['red', 'green', 'blue', 'yellow', 'purple']

        self.deck = self.create_card_deck()
        self.player = random.randint(0, no_players - 1)
        self.scores = [0] * no_players

        self.event_calendar = self.play_game()

    def roll_dice(self):
        return random.choice(self.dice)

    def create_card_deck(self):
        """Erzeugt das Deck mit n_cards, jede Karte enthält 3 zufällige Farben."""
        deck = []
        for _ in range(self.n_cards):
            random.shuffle(self.colors)
            deck.append(self.colors[:3].copy())
        return deck

    def next_player(self):
        """Wechselt reihum zum nächsten Spieler."""
        self.player = (self.player + 1) % self.no_players

    def record_event(self, event_calendar, event_type, deck, throw):
        """Speichert ein Event ab."""
        event_calendar.append({
            'event': event_type,
            'player': self.player,
            'deck': [card.copy() for card in deck],  # tiefe Kopie
            'scores': self.scores.copy(),
            'throw': throw
        })

    def play_game(self):
        deck = [card.copy() for card in self.deck]  # Arbeitskopie
        event_calendar = []

        # Start-Event
        self.record_event(event_calendar, 'start', deck, None)

        while deck:
            throw = self.roll_dice()
            self.record_event(event_calendar, 'roll_dice', deck, throw)

            # Smiley → Farbe der Karte übernehmen
            if throw == 'smiley':
                throw = deck[0][0]

            # Treffer?
            if throw in deck[0]:
                deck[0].remove(throw)
                self.record_event(event_calendar, 'hit', deck, throw)

            else:
                self.record_event(event_calendar, 'miss', deck, throw)
                self.next_player()

            # Karte vollständig?
            if len(deck[0]) == 0:
                deck.pop(0)
                self.scores[self.player] += 1
                self.record_event(event_calendar, 'complete_card', deck, throw)

        # Spielende
        self.record_event(event_calendar, 'end_game', deck, throw)

        return event_calendar
