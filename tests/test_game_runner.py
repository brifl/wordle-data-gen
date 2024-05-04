import unittest
from wordset import WordSet
from wordlegame import WordleGame
from gamerunner import GameRunner


class TestGameRunner(unittest.TestCase):
    def setUp(self):
        words = WordSet("apple\ngrape\nberry")
        self.runner = GameRunner(words)
        self.guess_index = 0

    def test_generate_games(self):
        games = self.runner.generate_games(2)
        self.assertEqual(len(games), 2)
        for game in games:
            self.assertIsInstance(game, WordleGame)
            self.assertIn(game.word, ["apple", "grape", "berry"])

    def test_clone_games_fresh(self):
        games = [WordleGame("apple"), WordleGame("grape")]
        cloned_games = self.runner.clone_games_fresh(games)
        self.assertEqual(len(cloned_games), 2)
        for game in cloned_games:
            self.assertIsInstance(game, WordleGame)
            self.assertIn(game.word, ["apple", "grape"])

    def test_run_games(self):
        games = [WordleGame("apple"), WordleGame("grape")]
        result_games = self.runner.run_games(games, self.guess_first_word)
        self.assertIsNotNone(result_games)
        self.assertEqual(len(result_games), 2)
        for game in result_games:
            self.assertNotEqual(game.state, "new")
            self.assertNotEqual(game.state, "failed")

    def guess_first_word(self, word_options, game_state):
        if self.guess_index == 3:
            self.guess_index = 0
        self.assertIsNotNone(game_state)
        self.assertEqual(3, len(word_options))
        option = word_options[self.guess_index]
        self.guess_index += 1
        return option


if __name__ == "__main__":
    unittest.main()
