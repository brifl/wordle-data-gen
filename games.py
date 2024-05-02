from typing import Set, List


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
    guesses: List[str] = []

    def __init__(self, winning_word: str):
        self.word = winning_word

    def guess(self, guess: str) -> bool:
        if len(self.guesses) >= 6:
            raise ValueError("Exceeded max of 6 guesses")
        self.guesses.append(guess)
        if guess == self.word:
            return True
        return False
    




class Generator:
    def __init__(self, words: WordSet):
        self.words = words

    