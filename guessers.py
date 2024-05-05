import random
from wordset import WordSet
from wordlegame import WordleGame
from typing import List, Dict, Iterable, Tuple
import string
import logging


class MisterRando:
    def __init__(self):
        pass

    def guess(possible_words: List[str], game_state: dict = None) -> str:
        return random.choice(possible_words)


class GoodGuesser:
    def __init__(self, word_set: WordSet):
        self.possible_words = word_set
        self.letter_stats = {}
        self.initialize_stats()

    def initialize_stats(self):
        for letter in string.ascii_lowercase:
            self.letter_stats[letter] = [0, 0, 0, 0, 0]
        for word in self.possible_words.all_words:
            for i in range(0, len(word)):
                self.letter_stats[word[i]][i] += 1

    def guess(self, possible_words: List[str], game_state: WordleGame = None) -> str:
        word_scores = self.score_words()
        total_score = sum(word_scores.values())
        weighted_random = random.randint(0, total_score)
        sorted_words = sorted(word_scores, key=word_scores.get, reverse=True)
        for word in sorted_words:
            weighted_random -= word_scores[word]
            if weighted_random <= 0:
                logging.debug(f"Guessing {word}")
                return word
        logging.debug(
            f"Error: No word found with filter down to {len(sorted_words)} words"
        )
        return random.choice(possible_words)

    def score_words(self) -> Dict[str, int]:
        word_scores = {}
        words = self.possible_words.get_filtered_words()
        for word in words:
            word_scores[word] = self.score_word(word)
        return word_scores

    def score_word(self, word: str) -> int:
        score = 0
        for i in range(0, len(word)):
            score += self.letter_stats[word[i]][i]
        return score
