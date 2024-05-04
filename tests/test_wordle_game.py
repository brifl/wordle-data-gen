import unittest
from wordlegame import WordleGame


class TestWordleGame(unittest.TestCase):
    def setUp(self):
        self.game = WordleGame("apple")

    def test_init(self):
        self.assertEqual(self.game.word, "apple")
        self.assertEqual(self.game.guessed_words, [])
        self.assertEqual(self.game.letters_not_remaining, set())
        self.assertEqual(self.game.right_spot, "?????")
        self.assertEqual(self.game.wrong_spot, set())
        self.assertEqual(self.game.state, "new")

    def test_guess_correct(self):
        result = self.game.guess("apple")
        self.assertEqual(result, True)
        self.assertEqual(self.game.state, "won")

    def test_guess_incorrect(self):
        result = self.game.guess("grape")
        self.assertEqual(result, False)
        self.assertNotEqual(self.game.state, "won")
        self.assertEqual(self.game.state, "in progress")

    def test_game_completed(self):
        self.game.guess("apple")
        with self.assertRaises(ValueError):
            self.game.guess("grape")


if __name__ == "__main__":
    unittest.main()
