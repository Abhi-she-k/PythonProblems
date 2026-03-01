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
            if (
                new_second[0 : len(new_first)] == new_first
                or new_first[0 : len(new_second)] == new_second
            ):
                if backtrack(new_first, new_second):
                    return True
            else:

                continue

        return False

    return backtrack("", "")


# bandwith

def bandwidth(edges):
    n = len(edges)

    def try_bandwidth(limit):
        """Try to find a numbering with given bandwidth limit"""
        numbering = [-1] * n  # numbering[node] = assigned number
        used = [False] * n  # used[number] = whether number is used

        def backtrack(node_idx):
            """Try to assign numbers to nodes"""
            # Base case: all nodes numbered
            if node_idx == n:
                return True

            # Choose next node to number (could be optimized)

            # FIX 1: In the default implementation, the next node we assign is just the sequential nodes starting from 0;
            # this implementation is not as fast as picking a node that is already limited to a small number of options,
            # meaning we are reducing our branching as well as the width of the search tree. To implement this, we would
            # be picking the node with the most neighbours that are already assigned at each recursive step. This would give
            # us the node with the least amount of options and branching. Overall, this would greatly reduce the branching
            # and speed of the algorithm.
            node = -1
            maxEdge = float("-inf")

            for i in range(n):

                if numbering[i] == -1:

                    numEdge = 0

                    for neighbor in edges[i]:
                        if numbering[neighbor] != -1:
                            numEdge += 1

                    if numEdge > maxEdge:
                        maxEdge = numEdge
                        node = i

            # Try each available number
            for num in range(n):
                if used[num]:
                    continue

                # Check if this number violates bandwidth constraint
                valid = True
                for neighbor in edges[node]:
                    if numbering[neighbor] != -1:
                        if abs(num - numbering[neighbor]) > limit:
                            valid = False
                            break

                if valid:
                    # Assign this number
                    numbering[node] = num
                    used[num] = True

                    if backtrack(node_idx + 1):
                        return True

                    # Backtrack
                    numbering[node] = -1
                    used[num] = False

            return False

        return backtrack(0)

    # Iterative deepening: try bandwidth 1, 2, 3, ...
    for bw in range(1, n):
        if try_bandwidth(bw):
            return bw

    return n - 1


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


    # Apart of FIX 1: Where we build the original possible placements set. 
    for pos in ones:
        board[pos] = 1
        for neighbor in get_neighbors(pos[0], pos[1]):
            if neighbor not in board:
                possiblePlacements.add(neighbor)

    def get_sum(r, c):
        """Get sum of neighboring stones"""
        total = 0
        for neighbor in get_neighbors(r, c):
            if neighbor in board:
                total += board[neighbor]
        return total

    def backtrack(k):
        """Try to place stone k and continue"""
        best = k - 1  # Best we've achieved so far

        # Try each empty position

        # FIX 1: In the original implementation we would loop through the entire board to find the empty positions, 
        # but this is inefficient. As when we start on a select few positions can be used to place a stone, looping through
        # the entire board would be a waste, instead of looping O(n^2) at every recursive call, we can just loop through the
        # possible placements which would be smaller than (nxn), would be more like O(k), where k is the number of stones to place. 
        for r, c in list(possiblePlacements):
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



# unity_partition

def unity_partition(n):
    from fractions import Fraction
    
    def backtrack(target_sum, target_frac, current_list, start):
        # Base case: we've used up both the sum and the fraction
        if target_sum == 0 and target_frac == 0:
            return current_list[:]
        
        # Dead ends
        if target_sum <= 0 or target_frac <= 0:
            return None
        
        # Try each possible next number
        for num in range(start, target_sum):

            reciprocal = Fraction(1, num)
            
            # Skip if reciprocal is too large
            if reciprocal > target_frac:
                continue

            if target_sum - num < 0:
                continue

            # FIX 1: We are checking that in the best case if we take remaning recipriocal sums before we exceed our remaining budget for sum, 
            # we can still reach our target fraction. If our max fraction is less that our target fraction we know in the best case, taking
            # all the allowed remaining numbers, we won't reach our target fraction and this path will not lead to a solution.
            remaining_sum = target_sum - num
            temp = num+1
            max_fraction = 0 

            while True:
                if(remaining_sum - temp < 0):
                    break
                else:
                    remaining_sum -= temp
                    max_fraction += 1 / temp
                    temp += 1

            if(max_fraction < target_frac - reciprocal):
                continue

            # Try adding this number
            current_list.append(num)
            result = backtrack(target_sum - num, target_frac - reciprocal, current_list, num + 1)
            
            if result is not None:
                return result
            
            current_list.pop()
        
        return None
    
    result = backtrack(n, Fraction(1, 1), [], 2)
    return result if result else []