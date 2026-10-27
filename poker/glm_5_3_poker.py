def best_hands(hands):
    def evaluate(hand):
        cards = hand.split()
        rank_map = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
                     '10':10,'J':11,'Q':12,'K':13,'A':14}
        ranks = sorted((rank_map[c[:-1]] for c in cards), reverse=True)
        suits = {c[-1] for c in cards}

        # straight check (with wheel)
        unique = sorted(set(ranks), reverse=True)
        straight_high = None
        if len(unique) == 5:
            if unique[0] - unique[4] == 4:
                straight_high = unique[0]
            elif unique == [14, 5, 4, 3, 2]:
                straight_high = 5

        flush = len(suits) == 1

        from collections import Counter
        counts = Counter(ranks)
        # sort by count desc, then rank desc
        groups = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
        pattern = sorted(counts.values(), reverse=True)

        if flush and straight_high:
            category = 8
            tiebreak = [straight_high]
        elif pattern == [4, 1]:
            category = 7
            tiebreak = [groups[0][0], groups[1][0]]
        elif pattern == [3, 2]:
            category = 6
            tiebreak = [groups[0][0], groups[1][0]]
        elif flush:
            category = 5
            tiebreak = ranks
        elif straight_high:
            category = 4
            tiebreak = [straight_high]
        elif pattern == [3, 1, 1]:
            category = 3
            tiebreak = [g[0] for g in groups]
        elif pattern == [2, 2, 1]:
            category = 2
            tiebreak = [g[0] for g in groups]
        elif pattern == [2, 1, 1, 1]:
            category = 1
            tiebreak = [g[0] for g in groups]
        else:
            category = 0
            tiebreak = ranks

        return (category, tiebreak)

    if not hands:
        return []
    scores = [(evaluate(h), h) for h in hands]
    best = max(s for s, _ in scores)
    return [h for s, h in scores if s == best]