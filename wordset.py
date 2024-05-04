import logging
from typing import List, Set


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
        logging.debug(
            f"Applying letter position filter: {position} {letter} with {len(self.filtered_words)} words."
        )
        self.filtered_words = {
            word for word in self.filtered_words if word[position] == letter
        }
        logging.debug(f"Filtered down to {len(self.filtered_words)} words.")

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
        logging.debug(
            f"Applying letter contained filter: {letter} with {len(self.filtered_words)} words."
        )
        self.filtered_words = {
            word
            for word in self.filtered_words
            if self.letter_in_subword(word, letter, open_positions)
        }
        logging.debug(f"Filtered down to {len(self.filtered_words)} words.")

    def apply_letter_not_contained_filter(
        self, letter: str, open_positions: List[int] = None
    ) -> None:
        logging.debug(
            f"Applying letter not contained filter: {letter} with {len(self.filtered_words)} words."
        )
        self.filtered_words = {
            word
            for word in self.filtered_words
            if not self.letter_in_subword(word, letter, open_positions)
        }
        logging.debug(f"Filtered down to {len(self.filtered_words)} words.")
