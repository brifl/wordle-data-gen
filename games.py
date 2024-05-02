from typing import Set

class WordSet:
    all_words: Set[str] = set()
    filtered_words: Set[str] = set()

    def __init__(self, words:str):
        self.init(words)
        self.reset_filter()

    def init(self, words:str) -> None:
        lines = words.split('\n')
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
    
    def apply_length_filter(self, length:int) -> None:
        self.filtered_words = {word for word in self.filtered_words if len(word) == length}

