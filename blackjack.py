import random


class Card:
    SUITS = ['Corazones', 'Diamantes', 'Treboles', 'Picas']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  
        else:
            return int(self.rank)
 
    def __str__(self):
        return f"{self.rank} de {self.suit}"


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit)
                      for suit in Card.SUITS
                      for rank in Card.RANKS]
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            raise ValueError("La baraja esta vacia")
        return self.cards.pop()


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []

    def deal_initial_cards(self):
        self.player_hand = [self.deck.deal(), self.deck.deal()]
        self.dealer_hand = [self.deck.deal(), self.deck.deal()]

    def player_hit(self):
        self.player_hand.append(self.deck.deal())

    def dealer_hit(self):
        self.dealer_hand.append(self.deck.deal())

    def calculate_score(self, hand):
        score = sum(card.value() for card in hand)
        aces = sum(1 for card in hand if card.rank == 'A')
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def is_bust(self, hand):
        return self.calculate_score(hand) > 21

    def is_blackjack(self, hand):
        return len(hand) == 2 and self.calculate_score(hand) == 21

    def dealer_should_hit(self):
        return self.calculate_score(self.dealer_hand) < 17

    def get_winner(self):
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        if self.is_bust(self.player_hand):
            return "dealer"
        if self.is_bust(self.dealer_hand):
            return "player"
        player_bj = self.is_blackjack(self.player_hand)
        dealer_bj = self.is_blackjack(self.dealer_hand)
        if player_bj and not dealer_bj:
            return "player"
        if dealer_bj and not player_bj:
            return "dealer"
        if player_score > dealer_score:
            return "player"
        if dealer_score > player_score:
            return "dealer"
        return "tie"


def play():
    print("=== BLACKJACK ===\n")
    game = BlackjackGame()
    game.deal_initial_cards()

    print("Tu mano:")
    for card in game.player_hand:
        print(f"  {card}")
    print(f"  Puntuacion: {game.calculate_score(game.player_hand)}\n")

    print("Mano del dealer:")
    print(f"  {game.dealer_hand[0]} (carta oculta)")

    if game.is_blackjack(game.player_hand):
        print("\n¡BLACKJACK! ¡Ganaste!")
        return

    while not game.is_bust(game.player_hand):
        action = input("\n¿Pedir carta (p) o plantarse (s)? ").strip().lower()
        if action == 'p':
            game.player_hit()
            print("Tu mano:")
            for card in game.player_hand:
                print(f"  {card}")
            print(f"  Puntuacion: {game.calculate_score(game.player_hand)}")
            if game.is_bust(game.player_hand):
                print("\nTe has pasado de 21. ¡El dealer gana!")
                return
        elif action == 's':
            break

    print("\nMano del dealer:")
    for card in game.dealer_hand:
        print(f"  {card}")
    print(f"  Puntuacion: {game.calculate_score(game.dealer_hand)}")

    while game.dealer_should_hit():
        game.dealer_hit()
        print(f"  El dealer pide carta: {game.dealer_hand[-1]}")
        print(f"  Puntuacion: {game.calculate_score(game.dealer_hand)}")

    winner = game.get_winner()
    print("\n--- RESULTADO ---")
    if winner == "player":
        print("¡Ganaste!")
    elif winner == "dealer":
        print("El dealer gana.")
    else:
        print("¡Empate!")


if __name__ == "__main__":
    play()