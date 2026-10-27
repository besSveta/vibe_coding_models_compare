def best_hands(hands):
    def evaluate(hand):
        ranks = sorted(['--23456789TJQKA'.index(c[0]) for c in hand], reverse=True)
        suits = [c[1] for c in hand]
        is_flush = len(set(suits)) == 1
        is_straight = ranks == list(range(ranks[0], ranks[0]-5, -1))
        if is_straight and ranks[0] == 14:
            ranks = [5,4,3,2,1]
        counts = {r: ranks.count(r) for r in set(ranks)}
        count_vals = sorted(counts.values(), reverse=True)
        if is_straight and is_flush:
            return (8, ranks)
        if 4 in count_vals:
            return (7, [r for r in ranks if counts[r]==4][0], [r for r in ranks if counts[r]!=4][0])
        if count_vals == [3,2]:
            return (6, [r for r in ranks if counts[r]==3][0], [r for r in ranks if counts[r]==2][0])
        if is_flush:
            return (5, ranks)
        if is_straight:
            return (4, ranks)
        if 3 in count_vals:
            return (3, [r for r in ranks if counts[r]==3][0], [r for r in ranks if counts[r]!=3])
        if count_vals == [2,2,1]:
            pairs = sorted([r for r in ranks if counts[r]==2], reverse=True)
            kicker = [r for r in ranks if counts[r]==1][0]
            return (2, pairs[0], pairs[1], kicker)
        if 2 in count_vals:
            pair = [r for r in ranks if counts[r]==2][0]
            kickers = sorted([r for r in ranks if counts[r]==1], reverse=True)
            return (1, pair, kickers)
        return (0, ranks)
    
    best_score = max(evaluate(h) for h in hands)
    return [h for h in hands if evaluate(h) == best_score]