
from collections import Counter
from itertools import combinations, product


class CardDeck:
    # Масти:
    # 2,3,4,5,6,7,8,9,10(ten, T), валет(jack, J), дама(queen, Q),
    # король(king, K), туз(ace, A)
    ranks_list = list('0123456789TJQKA')
    # Ранги:
    # трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
    suits_list = list('CSHD')
    ranks = frozenset(ranks_list[2:])
    suits = frozenset(suits_list)

    @classmethod
    def get_card_rank_value(cls, card):
        return (
                cls.ranks_list.index(card.rank) *
                len(cls.suits_list) + cls.suits_list.index(card.suit)
                )

    @classmethod
    def get_rank_value(cls, rank):
        return cls.ranks_list.index(rank)

    # def __init__(self):
    #     self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    # def __len__(self):
    #     return len(self._cards)

def get_verified_card_str(card):
        rank, suit = card
        if (type(rank) == type(suit) == str and
                rank in CardDeck.ranks and suit in CardDeck.suits):
            return '{}{}'.format(rank, suit)
        else:
            raise ValueError(
                "Must be 'RS', where R is in '123456789TJQKA' and S is in 'CSHD'")


class FiveCards:
    def __init__(self, five_cards_str):
        # hand_str example: "JD TC TH 7C 7D 7S 7H"
        five_cards_list = five_cards_str.split()
        self.cards_list = []
        self.ranks = []
        self.suits = []
        if len(five_cards_list) == 5:
            for card_str in five_cards_list:
                self.cards_list.append(get_verified_card_str(card_str))
                self.ranks.append(card_str[0])
                self.suits.append(card_str[1])
            self.ranks_values = self.get_ranks_values()
            _ranks_tuple = self.hand_rank()
            self.rank = _ranks_tuple[0]
            self.aux_rank = self.get_aux_rank(_ranks_tuple[1:])
        else:
            raise ValueError("In the poker hand must be 5 cards_list")

    def get_ranks_values(self):
        """Возвращает список рангов (его числовой эквивалент),
        отсортированный от большего к меньшему"""
        rank_values = [CardDeck.get_rank_value(rank) for rank in self.ranks]
        return sorted(rank_values, reverse=True)

    def flush(self):
        """Возвращает True, если все карты одной масти"""
        return True if len(set(self.suits)) == 1 else False

    def straight(self):
        """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
        где у 5ти карт ранги идут по порядку (стрит)"""
        min_rank_value = min(self.ranks_values)
        return True if (
            set(range(min_rank_value, min_rank_value+5)).issubset(self.ranks_values)
        ) else False

    def kind(self, n):
        """Возвращает первый ранг, который n раз встречается в данной руке.
        Возвращает None, если ничего не найдено"""
        rank_counter = Counter(self.ranks)
        repeated_ranks = [rank for rank, repetition in rank_counter.items() if
             repetition == n]
        if len(repeated_ranks):
            return CardDeck.get_rank_value(repeated_ranks[0])

    def two_pair(self):
        """Если есть две пары, то возврщает два соответствующих ранга,
        иначе возвращает None"""
        n = 2
        rank_counter = Counter(self.ranks)
        repeated_ranks = [CardDeck.get_rank_value(rank) for rank, repetition
                          in rank_counter.items() if repetition == n]
        # print(self.ranks)
        if len(repeated_ranks) == 2:
            return tuple(repeated_ranks)

    def hand_rank(self):
        """Возвращает значение определяющее ранг 'руки'"""
        # «Стрит Флеш» – 5 карт одной масти по порядку:
        if self.straight() and self.flush():
            return (8, max(self.ranks_values))
        # «Каре» – 4 карты одного ранга:
        elif self.kind(4):
            return (7, self.kind(4), self.kind(1))
        # «Фулл Хаус» – комбинация, включающая в себя «Пару» и «Тройку» одновременно:
        elif self.kind(3) and self.kind(2):
            return (6, self.kind(3), self.kind(2))
        # «Флеш» – 5 одномастных карт:
        elif self.flush():
            return (5, self.ranks_values)
        # «Стрит» – 5 собранных по порядку карт любой масти:
        elif self.straight():
            return (4, max(self.ranks_values))
        # «Сет» или «Тройка» – 3 карты одного ранга:
        elif self.kind(3):
            return (3, self.kind(3), self.ranks_values)
        # «Две пары» – 4 карты, среди которых собраны по 2 одинаковых по рангу:
        elif self.two_pair():
            return (2, self.two_pair(), self.ranks_values)
        # «Пара» – это 2 одинаковые карты:
        elif self.kind(2):
            return (1, self.kind(2), self.ranks_values)
        else:
            return (0, self.ranks_values)

    def get_aux_rank(self, aux_ranks):
        ranks_sum = 0
        for rank_val in aux_ranks:
            if type(rank_val) in (list, tuple):
                ranks_sum += sum(rank_val)
            elif type(rank_val) == int:
                ranks_sum += rank_val
        return ranks_sum


def get_wild_hands_iter(joker_hand_list: list):
    joker_hand_list = joker_hand_list[:]
    hand_set = set([(card[0], card[1]) for card in joker_hand_list if card[0] != '?'])
    suits = ''
    if '?B' in joker_hand_list:
        suits += 'CS'
        joker_hand_list.remove('?B')
    if '?R' in joker_hand_list:
        suits += 'HD'
        joker_hand_list.remove('?R')

    joker_cards_set = set(product(CardDeck.ranks, suits))
    joker_cards_set.difference_update(hand_set)
    str_hand = ' '.join(joker_hand_list)

    if suits == 'CSHD':
        jokers_cards_iter = combinations(joker_cards_set, 2)  # two jokers
    else:
        jokers_cards_iter = joker_cards_set  # one joker

    for card in jokers_cards_iter:
        if len(suits) == 2:  # one joker
            cards_str = ''.join(card)
        if len(suits) == 4:  # two jokers
            cards_str = ' '.join((''.join(card[0]), ''.join(card[1])))
        yield '{} {}'.format(str_hand, cards_str).split()


def best_hand(hand: list):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    len(hand)
    gen_five_cards = (" ".join(i) for i in combinations(hand, 5))
    best_five_cards = get_best_five_cards(gen_five_cards)
    return best_five_cards.cards_list


def get_best_five_cards(five_cards_iter):
    max_rank = 0
    max_aux_rank = 0
    best_five_cards = 0
    for five_cards in five_cards_iter:
        if type(five_cards) != str:
            five_cards = ' '.join(five_cards)
        five_cards = FiveCards(five_cards)

        if five_cards.rank > max_rank:
            max_rank = five_cards.rank
            max_aux_rank = five_cards.aux_rank
            best_five_cards = five_cards
            # print(max_rank, best_hand.cards_list)

        if five_cards.rank == best_five_cards.rank:
            # print('-----------', five_cards.aux_rank, five_cards.cards_list)
            if five_cards.aux_rank > max_aux_rank:
                max_aux_rank = five_cards.aux_rank
                best_five_cards = five_cards
    return best_five_cards


def best_wild_hand(hand_list):
    """best_hand но с джокерами"""
    if '?B' in hand_list or '?R' in hand_list:
        wild_hand_iter = get_wild_hands_iter(hand_list)
        best_hands_set = set()

        for hand in wild_hand_iter:
            best_hands_set.add(' '.join(best_hand(hand)))

        return sorted(get_best_five_cards(best_hands_set).cards_list)
    else:
        return best_hand(hand_list)


if __name__ == '__main__':

    c_list = "TD TC 5H 5C 7C ?R ?B".split()

    print('6C 7C 8C 9C TC 5C JS : {}'.format(
        best_hand("6C 7C 8C 9C TC 5C JS".split())))

    print(sorted(best_wild_hand(c_list)))
