import unittest
from games import WordSet


class TestWordSet(unittest.TestCase):
    def setUp(self):
        self.word_set = WordSet("word1\nword2\nword3")
        self.word_set2 = WordSet("word1\nword2\nword3\nsixlet")

    def test_init(self):
        self.assertEqual(self.word_set.all_words, {"word1", "word2", "word3"})

    def test_reset_filter(self):
        self.word_set.reset_filter()
        self.assertEqual(self.word_set.filtered_words, {"word1", "word2", "word3"})

    def test_get_filtered_words(self):
        self.word_set.reset_filter()
        self.assertEqual(
            self.word_set.get_filtered_words(), {"word1", "word2", "word3"}
        )

    def test_apply_length_filter(self):
        self.assertEqual(4, len(self.word_set2.get_filtered_words()))

        self.word_set2.apply_length_filter(5)
        self.assertEqual(
            self.word_set2.get_filtered_words(), {"word1", "word2", "word3"}
        )

        self.word_set2.reset_filter()
        self.word_set2.apply_length_filter(6)
        self.assertEqual(self.word_set2.get_filtered_words(), {"sixlet"})


if __name__ == "__main__":
    unittest.main()
