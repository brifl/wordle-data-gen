from typing import Set, List, Callable
import json
import random


class WordSet:
    def __init__(self, words: str):
        self.all_words: Set[str] = set()
        self.filtered_words: Set[str] = set()
        self.init(words)
        self.reset_filter()

    def init(self, words: str) -> None:
        lines = words.split("\n")
        for line in lines:
            line = line.strip()
            if line and line.isalnum():
                self.all_words.add(line.lower())

    def reset_filter(self) -> None:
        self.filtered_words.clear()
        for word in self.all_words:
            self.filtered_words.add(word)

    def get_filtered_words(self) -> Set[str]:
        return self.filtered_words

    def apply_length_filter(self, length: int) -> None:
        self.filtered_words = {
            word for word in self.filtered_words if len(word) == length
        }

    def apply_letter_position_filter(self, position: int, letter: str) -> None:
        self.filtered_words = {
            word for word in self.filtered_words if word[position] == letter
        }

    def letter_in_subword(
        self, word: str, letter: str, open_positions: List[int]
    ) -> bool:
        for position in open_positions:
            if position >= len(word):
                return False
            if word[position] == letter:
                return True
        return False

    def apply_letter_contained_filter(
        self, letter: str, open_positions: List[int] = None
    ) -> None:
        self.filtered_words = {
            word
            for word in self.filtered_words
            if self.letter_in_subword(word, letter, open_positions)
        }

    def apply_letter_not_contained_filter(
        self, letter: str, open_positions: List[int] = None
    ) -> None:
        self.filtered_words = {
            word
            for word in self.filtered_words
            if not self.letter_in_subword(word, letter, open_positions)
        }


class WordleGame:
    def __init__(self, winning_word: str):
        self.guessed_words: List[str] = []
        self.letters_not_remaining = set()
        self.wrong_spot = set()
        self.state = "new"
        self.word = winning_word
        self.right_spot = ""
        self.stats = []
        for _ in winning_word:
            self.right_spot += "?"
            self.stats.append({})

    def guess(self, guess: str) -> bool:
        if self.state in ["won", "lost", "failed"]:
            raise ValueError("This game is completed. Please start a new game.")
        if len(guess) != len(self.word):
            raise ValueError("The guess must be the same length as the winning word.")
        self.update_game_state(guess)
        if guess == self.word:
            self.state = "won"
            return True
        if len(self.guessed_words) >= 6:
            self.state = "lost"
        return False

    def update_game_state(self, guess: str) -> None:
        self.guessed_words.append(guess)
        if self.state == "new":
            self.state = "in progress"
        for i, letter in enumerate(guess):
            if letter == self.word[i]:
                self.right_spot = (
                    self.right_spot[:i] + letter + self.right_spot[i + 1 :]
                )
                if letter in self.wrong_spot:
                    self.wrong_spot.remove(letter)
            elif letter in self.word:
                self.wrong_spot.add(letter)
        self.letters_not_remaining.add(guess)

    def add_stat(self, key: str, value: any) -> None:
        self.stats[len(self.guessed_words)][key] = value

    def failed(self, reason: str = None):
        self.state = "failed"
        if reason:
            self.add_stat("failure_reason", reason)

    def summary_string(self) -> str:
        return json.dumps(self.summary())

    def summary(self) -> str:
        return {
            "state": self.state,
            "right_spot": self.right_spot,
            "wrong_spot": sorted(list(self.wrong_spot)),
            "letters_not_remaining": sorted(list(self.letters_not_remaining)),
            "guessed_words": self.guessed_words,
        }


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
            words.apply_letter_not_contained_filter(letter, open_positions)
        for letter in game.letters_not_remaining:
            words.apply_letter_contained_filter(letter, open_positions)

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
            if guess in game.guessed_words or guess not in self.words.all_words:
                allowed_bad_guesses -= 1
                continue

            try:
                game.guess(guess)
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
            self.run_game(game, guesser)
        return games
