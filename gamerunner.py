from wordlegame import WordleGame
from wordset import WordSet
import logging
import random
from typing import Callable, List


class GameRunner:
    def __init__(self, words: WordSet):
        self.words = words

    def generate_games(self, game_count: int) -> List[WordleGame]:
        games = []
        for _ in range(game_count):
            random_word = random.choice(list(self.words.get_filtered_words()))
            game = WordleGame(random_word)
            games.append(game)
        return games

    def clone_games_fresh(self, games: List[WordleGame]) -> List[WordleGame]:
        new_games = []
        for game in games:
            new_game = WordleGame(game.word)
            new_games.append(new_game)
        return new_games

    @staticmethod
    def filter_words(words: WordSet, game: WordleGame) -> None:
        open_positions = []
        for i in range(0, len(game.right_spot)):
            if game.right_spot[i] != "?":
                words.apply_letter_position_filter(i, game.right_spot[i])
            else:
                open_positions.append(i)
        for letter in game.wrong_spot:
            words.apply_letter_contained_filter(letter, open_positions)
        for letter in game.letters_not_remaining:
            words.apply_letter_not_contained_filter(letter, open_positions)

    def run_game(
        self, game: WordleGame, guesser: Callable[[List[str], dict], str]
    ) -> WordleGame:
        self.words.reset_filter()
        game.add_stat("word_count", len(self.words.all_words))
        allowed_bad_guesses = 10  # Allow some bad guesses

        while (
            game.state == "in progress" or game.state == "new"
        ) and allowed_bad_guesses > 0:
            possible_words = list(self.words.all_words)
            guess = guesser(possible_words, game.summary())
            logging.debug(f"Guess: {guess} of {len(self.words.all_words)} words")
            if guess in game.guessed_words or guess not in self.words.all_words:
                allowed_bad_guesses -= 1
                continue

            try:
                game.guess(guess)
                logging.debug("applied")
            except ValueError as e:
                allowed_bad_guesses -= 1
                continue

            allowed_bad_guesses = 10  # Reset

            self.filter_words(self.words, game)
            game.add_stat("word_count", len(self.words.get_filtered_words()))

        if allowed_bad_guesses == 0:
            game.failed("Exceeded allowed bad guesses.")

        return game

    def run_games(
        self, games: List[WordleGame], guesser: Callable[[List[str], dict], str]
    ) -> List[WordleGame]:
        for game in games:
            logging.debug(f"Running game {game.word}")
            self.run_game(game, guesser)
        return games
