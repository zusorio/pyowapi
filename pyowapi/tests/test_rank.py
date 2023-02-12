from unittest import TestCase
import pyowapi


class TestRank(TestCase):
    def test_greater_than(self):
        rank1 = pyowapi.Rank("Gold", 1)
        rank2 = pyowapi.Rank("Gold", 5)
        self.assertGreater(rank1, rank2)

        rank3 = pyowapi.Rank("Diamond", 5)
        rank4 = pyowapi.Rank("Platinum", 1)
        self.assertGreater(rank3, rank4)

    def test_less_than(self):
        rank1 = pyowapi.Rank("Bronze", 1)
        rank2 = pyowapi.Rank("Bronze", 2)
        self.assertLess(rank2, rank1)

        rank3 = pyowapi.Rank("Grandmaster", 5)
        rank4 = pyowapi.Rank("Master", 1)
        self.assertLess(rank4, rank3)

    def test_equal(self):
        rank1 = pyowapi.Rank("Gold", 1)
        rank2 = pyowapi.Rank("Gold", 1)
        self.assertEqual(rank1, rank2)

        rank3 = pyowapi.Rank("Grandmaster", 5)
        rank4 = pyowapi.Rank("Grandmaster", 5)
        self.assertEqual(rank3, rank4)
