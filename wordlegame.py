import json
import logging
from typing import List


class WordleGame:
    def __init__(self, winning_word: str):
        self.guessed_words: List[str] = []
        self.letters_not_remaining = set()
        self.wrong_spot = set()
        self.state = "new"
        self.word = winning_word
        self.remaining_word = winning_word
        self.right_spot = ""
        self.stats = [{}, {}]
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
            logging.debug(f"Won in {len(self.guessed_words)} guesses")
            return True
        if len(self.guessed_words) >= 6:
            self.state = "lost"
            logging.debug(f"Lost. The word was {self.word}")
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
                self.remaining_word = (
                    self.remaining_word[:i] + "*" + self.remaining_word[i + 1 :]
                )
                if letter in self.wrong_spot:
                    self.wrong_spot.remove(letter)
            elif letter in self.remaining_word:
                self.wrong_spot.add(letter)
        for letter in guess:
            if letter not in self.word:
                self.letters_not_remaining.add(letter)

    def add_stat(self, key: str, value: any) -> None:
        if len(self.guessed_words) >= len(self.stats):
            logging.warning(
                f"Adding stat {key} to {len(self.guessed_words)} but only have {len(self.stats)} stats"
            )
            return
        self.stats[len(self.guessed_words)][key] = value

    def failed(self, reason: str = None):
        self.state = "failed"
        if reason:
            self.add_stat("failure_reason", reason)
            logging.warn(f"Game failed on word {self.word}: {reason}")

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
