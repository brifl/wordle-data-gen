from typing import Set, List
import json


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


class WordleGame:
    def __init__(self, winning_word: str):
        self.guessed_words: List[str] = []
        self.guessed_letters = set()
        self.right_spot = "?????"
        self.wrong_spot = set()
        self.state = "new"
        self.word = winning_word

    def guess(self, guess: str) -> bool:
        if self.game_state == "won" or self.game_state == "lost":
            raise ValueError("This game is completed. Please start a new game.")
        self.update_game_state(guess)
        if guess == self.word:
            self.game_state = "won"
            return True
        if len(self.guessed_words) >= 6:
            self.game_state = "lost"
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
            elif letter in self.word:
                self.wrong_spot.add(letter)
        self.guessed_letters.add(guess)

    def game_state_string(self) -> str:
        return json.dumps(self.game_state())

    def game_state(self) -> str:
        return {
            "state": self.state,
            "right_spot": self.right_spot,
            "wrong_spot": sorted(list(self.wrong_spot)),
            "guessed_letters": sorted(list(self.guessed_letters)),
            "guessed_words": self.guessed_words,
        }


class Generator:
    def __init__(self, words: WordSet):
        self.words = words
