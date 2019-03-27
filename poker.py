from typing import NamedTuple
from collections import namedtuple


# Card = collections.namedtuple('Card', ['rank', 'suit'])


class Card:
    rank: str
    suit: str
    def __init__(self, rank_suit: str):
        if (len(rank_suit)==2
                and rank_suit.startswith(tuple('123456789TJQKA'),0)
                and rank_suit.endswith(tuple('CSHD'), 1)):
            self.rank = rank_suit[0]
            self.suit = rank_suit[1]
        else:
            raise ValueError("Must be 'RS', "
                             "where R in '123456789TJQKA' and S in 'CSHD'")
    def __str__(self):
        return '{}{}'.format(self.rank, self.suit)

    def __repr__(self):
        return "'{}{}'".format(self.rank, self.suit)

    # def __repr__(self):
    #     return "Card(rank='{}', suit='{}')".format(self.rank, self.suit)


class CardDeck:
    ranks = '123456789TJQKA'
    suits = 'CSHD'

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)


class Hand:
    def __init__(self, str_hand):
        hand_list = str_hand.split()
        if len(hand_list) == 7:
            self._hand = [Card(rang_suit) for rang_suit in hand_list]
        else:
            raise ValueError("In the poker hand must be 7 cards")

    def __len__(self):
        return len(self._hand)

    def __str__(self):
        # return "Hand: '{}'".format(', '.join(self._hand))
        return 'hand: {}'.format(str(self._hand))

    def __repr__(self):
        return "Card(rank='{}', suit='{}')".format(self.rank, self.suit)



def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    return


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    return


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    return


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    return


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    return


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    return


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    return


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


if __name__ == '__main__':
    c1 = Card("AS")
    print(c1)

    hand1 = Hand("6C 7C 8C 9C TC 5C JS")
    print(hand1)


    # test_best_hand()
    # test_best_wild_hand()
