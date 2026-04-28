import unittest
from blackjack import Card, Deck, BlackjackGame


class TestCard(unittest.TestCase):

    def test_card_value_number(self):
        card = Card('7', 'Corazones')
        self.assertEqual(card.value(), 7)

    def test_card_value_face(self):
        card = Card('K', 'Picas')
        self.assertEqual(card.value(), 10)

    def test_card_value_ace(self):
        card = Card('A', 'Diamantes')
        self.assertEqual(card.value(), 11)


class TestDeck(unittest.TestCase):

    def test_deck_has_52_cards(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_deal_removes_card(self):
        deck = Deck()
        deck.deal()
        self.assertEqual(len(deck.cards), 51)


class TestBlackjackGame(unittest.TestCase):

    def setUp(self):
        self.game = BlackjackGame()

    def _make_hand(self, cards):
        return [Card(rank, 'Corazones') for rank in cards]

    def test_calculate_score_ace_adjusts_to_avoid_bust(self):
        hand = self._make_hand(['A', '9', '5'])
        self.assertEqual(self.game.calculate_score(hand), 15)

    def test_is_bust(self):
        hand = self._make_hand(['K', 'Q', '5'])
        self.assertTrue(self.game.is_bust(hand))

    def test_is_blackjack(self):
        hand = self._make_hand(['A', 'K'])
        self.assertTrue(self.game.is_blackjack(hand))

    def test_dealer_should_hit_below_17(self):
        self.game.dealer_hand = self._make_hand(['9', '6'])
        self.assertTrue(self.game.dealer_should_hit())

    def test_get_winner_player_bust(self):
        self.game.player_hand = self._make_hand(['K', 'Q', '5'])
        self.game.dealer_hand = self._make_hand(['10', '7'])
        self.assertEqual(self.game.get_winner(), 'dealer')

    def test_get_winner_tie(self):
        self.game.player_hand = self._make_hand(['10', '8'])
        self.game.dealer_hand = self._make_hand(['10', '8'])
        self.assertEqual(self.game.get_winner(), 'tie')

    def test_deal_initial_cards(self):
        self.game.deal_initial_cards()
        self.assertEqual(len(self.game.player_hand), 2)
        self.assertEqual(len(self.game.dealer_hand), 2)


if __name__ == '__main__':
    unittest.main()