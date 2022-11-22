from unittest import TestCase, main
from game import get_score, generate_game
import random

class GetScoreTest(TestCase):
    def setUp(self):
        self.test_list = generate_game()
        self.list_offsets = [i["offset"] for i in self.test_list]

    def test_binary_search(self):
        for i in self.test_list:
            get_score_result = get_score(self.test_list, i["offset"])
            true_result = (i["score"]["home"], i["score"]["away"])
            with self.subTest(i=i):
                self.assertEqual(get_score_result, true_result,
                                 "The value found by the get_score function does not correspond to the real one")

    def test_empty_list(self):
        empty_list = list()
        random_existing_offset = self.list_offsets[random.randint(0, len(self.list_offsets))]
        with self.assertRaises(ValueError):
            get_score(empty_list, random_existing_offset)

    def test_score_not_integer(self):
        random_float_number = random.uniform(0, len(self.list_offsets))
        with self.assertRaises(ValueError):
            get_score(self.test_list, random_float_number)

    def test_not_list_in_offset(self):
        with self.assertRaises(ValueError):
            get_score("string", self.list_offsets[random.randint(0, len(self.list_offsets))])

    def test_offset_not_in_game(self):
        missing_value = self.list_offsets[-1] + random.randint(0, 15)
        self.assertEqual(get_score(self.test_list, missing_value), None,
                         "returns an offset that definitely doesn't exist")


if __name__ == "__main__":
    main()
