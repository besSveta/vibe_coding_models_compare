def best_hands(hands):
    def card_value(card):
        rank = card[:-1]
        if rank == 'A':
            return 14
        elif rank == 'K':
            return 13
        elif rank == 'Q':
            return 12
        elif rank == 'J':
            return 11
        else:
            return int(rank)

    def evaluate_hand(hand):
        cards = hand.split()
        values = sorted([card_value(card) for card in cards], reverse=True)
        suits = [card[-1] for card in cards]
        
        # Check for flush
        is_flush = len(set(suits)) == 1
        
        # Check for straight
        is_straight = False
        straight_high = 0
        
        # Regular straight
        if len(set(values)) == 5:
            if values[0] - values[4] == 4:
                is_straight = True
                straight_high = values[0]
            # Ace-low straight (A,2,3,4,5)
            elif values == [14, 5, 4, 3, 2]:
                is_straight = True
                straight_high = 5
        
        # Count occurrences of each value
        value_counts = {}
        for v in values:
            value_counts[v] = value_counts.get(v, 0) + 1
        
        # Sort by count (descending), then by value (descending)
        counts = sorted(value_counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
        count_values = [c[1] for c in counts]
        
        # Determine hand rank
        if is_straight and is_flush:
            # Straight flush (including royal flush)
            return (8, [straight_high])
        elif count_values == [4, 1]:
            # Four of a kind
            return (7, [counts[0][0], counts[1][0]])
        elif count_values == [3, 2]:
            # Full house
            return (6, [counts[0][0], counts[1][0]])
        elif is_flush:
            # Flush
            return (5, values)
        elif is_straight:
            # Straight
            return (4, [straight_high])
        elif count_values == [3, 1, 1]:
            # Three of a kind
            kickers = sorted([c[0] for c in counts[1:]], reverse=True)
            return (3, [counts[0][0]] + kickers)
        elif count_values == [2, 2, 1]:
            # Two pair
            pairs = sorted([counts[0][0], counts[1][0]], reverse=True)
            kicker = counts[2][0]
            return (2, pairs + [kicker])
        elif count_values == [2, 1, 1, 1]:
            # One pair
            kickers = sorted([c[0] for c in counts[1:]], reverse=True)
            return (1, [counts[0][0]] + kickers)
        else:
            # High card
            return (0, values)

    if not hands:
        return []
    
    # Evaluate all hands
    evaluated = [(evaluate_hand(hand), hand) for hand in hands]
    
    # Find the best hand(s)
    best_rank = max(evaluated, key=lambda x: x[0])[0]
    return [hand for rank, hand in evaluated if rank == best_rank]