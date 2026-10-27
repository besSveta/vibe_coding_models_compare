from collections import Counter

RANK_VALUES = {str(n): n for n in range(2, 10)}
RANK_VALUES.update({
    "T": 10,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
})


def _parse_cards(hand):
    if ":" in hand:
        hand = hand.split(":", 1)[1]

    cards = []
    for token in hand.split():
        token = token.strip().upper()
        suit = token[-1]
        rank = token[:-1]
        cards.append((RANK_VALUES[rank], suit))
    return cards


def _hand_rank(hand):
    cards = _parse_cards(hand)
    ranks = [rank for rank, suit in cards]
    suits = [suit for rank, suit in cards]

    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    is_flush = len(suit_counts) == 1 and len(cards) == 5

    unique_ranks = sorted(set(ranks), reverse=True)
    straight_high = 0

    if len(unique_ranks) == 5:
        if unique_ranks == [14, 5, 4, 3, 2]:
            straight_high = 5
        elif unique_ranks[0] - unique_ranks[4] == 4:
            straight_high = unique_ranks[0]

    groups = sorted(
        rank_counts.items(),
        key=lambda item: (item[1], item[0]),
        reverse=True,
    )
    ordered_ranks = [rank for rank, count in groups]
    frequencies = sorted(rank_counts.values(), reverse=True)

    if is_flush and straight_high:
        return (8, (straight_high,))

    if frequencies and frequencies[0] == 4:
        return (7, (ordered_ranks[0], ordered_ranks[1]))

    if frequencies[:2] == [3, 2]:
        return (6, (ordered_ranks[0], ordered_ranks[1]))

    if is_flush:
        return (5, tuple(sorted(ranks, reverse=True)))

    if straight_high:
        return (4, (straight_high,))

    if frequencies and frequencies[0] == 3:
        return (3, tuple(ordered_ranks))

    if frequencies.count(2) == 2:
        return (2, tuple(ordered_ranks))

    if frequencies and frequencies[0] == 2:
        return (1, tuple(ordered_ranks))

    return (0, tuple(sorted(ranks, reverse=True)))


def best_hands(hands):
    if not hands:
        return []

    ranked_hands = [(_hand_rank(hand), hand) for hand in hands]
    best_rank = max(rank for rank, hand in ranked_hands)

    return [hand for rank, hand in ranked_hands if rank == best_rank]