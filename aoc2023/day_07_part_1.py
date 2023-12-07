import functools
from collections import Counter, namedtuple
from enum import IntEnum, auto

CARD_RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")


class HandType(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


Ordering = namedtuple("Ordering", ("hand_type", "subordering"))


def create_ordering(hand, hand_type):
    return Ordering(hand_type, tuple(CARD_RANKS.index(card) for card in hand))


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        hand_to_bid = {
            tokens[0]: int(tokens[1])
            for line in ifile.read().split("\n")
            if (tokens := line.split(" "))
        }
    hand_to_ordering = {hand: strongest_ordering(hand) for hand in hand_to_bid}
    return sum(
        (hand_rank * hand_to_bid[hand])
        for hand_rank, hand in enumerate(
            sorted(hand_to_bid, key=lambda hand: hand_to_ordering[hand]),
            1,
        )
    )


def strongest_ordering(hand):
    ordering_of_type = functools.partial(create_ordering, hand)

    match sorted(Counter(hand).values(), reverse=True):
        case [5]:
            ret = ordering_of_type(HandType.FIVE_OF_A_KIND)
        case [4, 1]:
            ret = ordering_of_type(HandType.FOUR_OF_A_KIND)
        case [3, 2]:
            ret = ordering_of_type(HandType.FULL_HOUSE)
        case [3, 1, 1]:
            ret = ordering_of_type(HandType.THREE_OF_A_KIND)
        case [2, 2, 1]:
            ret = ordering_of_type(HandType.TWO_PAIR)
        case [2, 1, 1, 1]:
            ret = ordering_of_type(HandType.ONE_PAIR)
        case [1, 1, 1, 1, 1]:
            ret = ordering_of_type(HandType.HIGH_CARD)
    return ret


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
