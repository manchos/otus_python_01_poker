import unittest
from poker import FiveCards


class FiveCardsTest(unittest.TestCase):
    def test_get_rank_values(self):
        self.assertEqual(
            FiveCards("TC 7C JS QC 4S").get_ranks_values(), [12, 11, 10, 7, 4]
        )
        self.assertEqual(
            FiveCards("TH TS 7C 7H 7D").get_ranks_values(), [10, 10, 7, 7, 7]
        )

    def test_straight(self):
        # five_cards = FiveCards("TC 7C JC QC 4C")
        self.assertEqual(FiveCards("TC 7C JS QC 4S").straight(), False)
        self.assertEqual(FiveCards('TS 6C 7C 8C 9C').straight(), True)
        self.assertEqual(FiveCards("TH TS 7C 7H 7D").straight(), False)

    def test_flush(self):
        self.assertEqual(FiveCards("TC 7C JC QC 4C").flush(), True)
        self.assertEqual(FiveCards('TC 6C 7H 8C 9C').flush(), False)

    def test_kind(self):
        self.assertEqual(FiveCards("JC TC 7H JC 7C").kind(2), 11)
        self.assertEqual(FiveCards('TS 6C 7C 8C 9C').kind(2), None)

    def test_two_pair(self):
        self.assertEqual(FiveCards("JC TC 7H JC 7C").two_pair(), (11, 7))
        self.assertEqual(FiveCards('TS 6C 7C 8C 9C').two_pair(), None)

    def test_hand_rank(self):
        # «Стрит Флеш» – 5 карт одной масти по порядку:
        self.assertEqual(FiveCards('TC 6C 7C 8C 9C').hand_rank(), (8, 10))
        # «Каре» – 4 карты одного ранга:
        self.assertEqual(FiveCards('TH 6C 7C 8C 9C').hand_rank(), (4, 10))
        # «Фулл Хаус» – комбинация,
        # включающая в себя «Пару» и «Тройку» одновременно:
        self.assertEqual(FiveCards('TH TS 7C 7H 7D').hand_rank(), (6, 7, 10))
        # «Флеш» – 5 одномастных карт:
        self.assertEqual(FiveCards('TC 2C 7C 8C 9C').hand_rank(),
                         (5, [10, 9, 8, 7, 2]))
        # «Стрит» – 5 собранных по порядку карт любой масти:
        self.assertEqual(FiveCards('3S 2H 5C 4D 6C').hand_rank(),
                         (4, 6))
        # «Сет» или «Тройка» – 3 карты одного ранга:
        self.assertEqual(FiveCards('3S 3H 3C 4D 6C').hand_rank(),
                         (3, 3, [6, 4, 3, 3, 3]))
        # «Две пары» – 4 карты, среди которых собраны по 2 одинаковых по рангу:
        self.assertEqual(FiveCards('3S 3H 4C 4D 6C').hand_rank(),
                         (2, (3, 4), [6, 4, 4, 3, 3]))
        # «Пара» – это 2 одинаковые карты:
        self.assertEqual(FiveCards('3S 3H 4C 5D 6C').hand_rank(),
                         (1, 3, [6, 5, 4, 3, 3]))
    # def test_sub(self):
    #     self.assertEqual(calc.sub(4, 2), 2)
    #
    # def test_mul(self):
    #     self.assertEqual(calc.mul(2, 5), 10)
    #
    # def test_div(self):
    #     self.assertEqual(calc.div(8, 4), 2)


if __name__ == '__main__':
    unittest.main()
