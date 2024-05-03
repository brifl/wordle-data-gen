import random
from games import WordleGame, WordSet
from typing import List
import string


class MisterRando:
    def __init__(self):
        pass

    def guess(possible_words: List[str], game_state: dict = None) -> str:
        return random.choice(possible_words)


class GoodGuesser:
    def __init__(self, word_set: WordSet):
        self.word_set = word_set
        self.letter_stats = {}
        self.initialize_stats()

    def initialize_stats(self):
        for letter in string.ascii_lowercase:
            self.letter_stats[letter] = [0, 0, 0, 0, 0]
        for word in self.word_set.all_words:
            for i in range(0, len(word)):
                self.letter_stats[word[i]][i] += 1

    def guess(self, possible_words: List[str], game_state: WordleGame = None) -> str:
        filtered = self.sorted_words()
        score_sum = 0
        for score in filtered.values():
            score_sum += score
        rando = random.randint(0, score_sum)
        for word in filtered:
            rando -= filtered[word]
            if rando <= 0:
                return word
        print("Error: No word found")
        return random.choice(possible_words)

    def sorted_words(self):
        word_scores = {}
        for word in self.word_set.filtered_words():
            word_scores[word] = self.score_word(word)

        return sorted(word_scores, key=word_scores.get, reverse=True)

    def score_word(self, word: str) -> int:
        score = 0
        for i in range(0, len(word)):
            score += self.letter_stats[word[i]][i]
        return score
