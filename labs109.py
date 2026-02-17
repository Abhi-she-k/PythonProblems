def ryerson_letter_grade(n):
    if n < 50:
        return "F"
    elif n > 89:
        return "A+"
    elif n > 84:
        return "A"
    elif n > 79:
        return "A-"
    tens = n // 10
    ones = n % 10
    if ones < 3:
        adjust = "-"
    elif ones > 6:
        adjust = "+"
    else:
        adjust = ""
    return "DCB"[tens - 5] + adjust

# Reverse the Rule 110

def reverse_110(current):
    n = len(current)

    # Rule 110 lookup table: maps (left, center, right) to next state
    rule_110 = {
        (0, 0, 0): 0,
        (0, 0, 1): 1,
        (0, 1, 0): 1,
        (0, 1, 1): 1,
        (1, 0, 0): 0,
        (1, 0, 1): 1,
        (1, 1, 0): 1,
        (1, 1, 1): 0,
    }

    def apply_rule_110(prev):
        """Apply Rule 110 to get next state"""
        next_state = []
        for i in range(n):
            left = prev[(i - 1) % n]
            center = prev[i]
            right = prev[(i + 1) % n]
            next_state.append(rule_110[(left, center, right)])
        return next_state

    def backtrack(prev, pos):
        """Build previous state position by position"""
        # Base case: filled all positions
        if pos == n:
            # Check if applying Rule 110 gives us current state
            if apply_rule_110(prev) == current:
                return prev[:]
            else:
                return None

        # Try both 0 and 1 for this position
        for value in [0, 1]:
            prev.append(value)

            # Check if this is still valid so far
            # We can check positions that have enough neighbors filled in
            if pos >= 2:

                # Check position pos-1
                check_pos = pos - 1
                center = prev[check_pos]

                # FIX 2: We don't need to use modulo n here since pos < n when we are checking and
                # The script ends when pos == n. So we don't need to wrap around the previous list object.
                left = prev[check_pos - 1]
                # FIX 1: Here check_pos + 1 with never be < pos since check_pos = pos - 1 and
                # check_pos + 1 = pos. Therefore, this condition is always false, and right is
                # always none, therefore, we never check rule_110 and never prune invalid branches.
                right = prev[check_pos + 1]

                if right is not None:
                    expected = rule_110[(left, center, right)]
                    if expected != current[check_pos]:
                        prev.pop()
                        continue

            result = backtrack(prev, pos + 1)
            if result is not None:
                return result

            prev.pop()

        return None

    return backtrack([], 0)

# Post Correspondence Problem

def post_correspondence_problem(first, second, lo, hi):

    def backtrack(first_str, second_str):
        # If strings match and length is in range, we found a solution
        if first_str == second_str and lo <= len(first_str) <= hi:
            return True
        
        # If strings are too long, stop
        if len(first_str) > hi or len(second_str) > hi:
            return False
        
        # Try appending each possible string pair
        for i in range(len(first)):

            new_first = first_str + first[i]
            new_second = second_str + second[i]

            # FIX 1: 
            # The first fix that was made was to improve the pruning. In the post_correspondence_problem implementation, 
            # no matter if the addition of elements from the first and second lists would make the strings never be compatible. 
            # If we check if the new first string or the new second string is in the prefix of the other, we know these strings 
            # still have a chance at being equivalent later in the recursion. If not, then they have no chance. 
            if(new_second[0:len(new_first)] == new_first or new_first[0:len(new_second)] == new_second):
                if backtrack(new_first, new_second):
                    return True
            else:

                continue

        return False
    
    return backtrack('', '')


# Stepping stones

def stepping_stones(n, ones):
    # Initialize board with stones
    board = {}  # (row, col) -> stone number
    possiblePlacements = set()

    def get_neighbors(r, c):
        """Get all valid neighbors of a position"""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    neighbors.append((nr, nc))
        return neighbors
    
    def get_sum(r, c):
        """Get sum of neighboring stones"""
        total = 0
        for neighbor in get_neighbors(r, c):
            if neighbor in board:
                total += board[neighbor]
        return total

    for pos in ones:
        board[pos] = 1
        for neighbor in get_neighbors(pos[0], pos[1]):
            if neighbor not in board:
                possiblePlacements.add(neighbor)

    def backtrack(k):
        """Try to place stone k and continue"""
        best = k - 1  # Best we've achieved so far
        
        # Try each empty position
        for (r,c) in list(possiblePlacements):
            if (r, c) in board:
                continue
            
            # Check if sum of neighbors equals k
            if get_sum(r, c) == k:
                # Place stone k here
                board[(r, c)] = k
                possiblePlacements.remove((r, c))

                added_neighbors = []    
                for neighbor in get_neighbors(r, c):
                    if neighbor not in board and neighbor not in possiblePlacements:
                        possiblePlacements.add(neighbor)
                        added_neighbors.append(neighbor)
                
                # Try to continue
                result = backtrack(k + 1)
                best = max(best, result)
                
                # Backtrack
                del board[(r, c)]

                for neighbor in added_neighbors:
                    possiblePlacements.remove(neighbor)

                possiblePlacements.add((r, c))

        return best
    
    return backtrack(2)