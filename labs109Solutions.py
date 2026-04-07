# Reverse the Rule 110
# --------------------------------------------------------------------------
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
            # FIX 3: 
            # In our pruning logic, we check whether the neighbouring positions match the current state we want. 
            # There is no reason to run applying rule 110 to the entire list again, as we validated all the states from 
            # current[1] to current[n-2]; Since the states wrap around once we have reached the end of the list, the states 
            # that we have not fully validated are the state at position 0 and the state at position n-1, as they are 
            # dependent on what value n-1 gets. Therefore, checking if the rule_110 states are equal to the current[n-1] 
            # and current[0] is only needed when we have reached our base case, not the entire built list, using the O(n) 
            # cost operation of apply_rule_110
            if rule_110[(prev[n-2], prev[n-1], prev[0])] == current[n-1] and rule_110[(prev[n-1], prev[0], prev[1])] == current[0]:
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

                # FIX 2: 
                # Another fix observed was reducing the overhead the algorithm caused. 
                # The modulo in the algorithm caused unnecessary overhead since we are checking 
                # neighbours that are already filled. check_pos = pos - 1, check_pos - 1 = pos - 2 
                # and check_pos + 1 = pos; all of these positions are already filled, so we do not 
                # need to worry about wrapping around the list.
                left = prev[check_pos - 1]
                # FIX 1: 
                # In the original implementation, check_pos + 1 will never be < pos since check_pos = pos - 1 
                # and check_pos + 1 = pos. This causes the condition check_pos + 1 < pos to never be true 
                # and causes right always to be none. The block of code that actually prunes the tree is 
                # wrapped in an if statement that checks whether the right is “not” None. If this is true, 
                # we can enter the pruning logic; if not, then we would never prune our branch. Causing the 
                # runtime to explode horizontally. A fix for this was to simply set it right and then check expected 
                # and prune based on those results.
                right = prev[check_pos + 1]

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
# --------------------------------------------------------------------------


# Post Correspondence Problem
# --------------------------------------------------------------------------
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
            # The first fix that was made was to improve the pruning. In the original implementation, there was no pruning involved, 
            # so the implementation was simply brute force until we achieved equal strings that were within the length of high and 
            # low constraints. A pruning fix that would greatly reduce the branches of the subtrees would be to confirm if the 2 string 
            # prefixes matched each other. In other words, string A either starts with string B or string B starts with string A. 
            # This would greatly reduce the branching, as when we confirm that neither of the 2 strings starts with the other, then 
            # this can never be a valid solution, so we would end traversing this branch early. Overall, we would significantly decrease 
            # the size of the tree that is being traversed with every prune, reducing the overall number of recursive calls. 
            if (new_second.startswith(new_first) or new_first.startswith(new_second)):
                if backtrack(new_first, new_second):
                    return True
            else:
                continue

        return False

    return backtrack("", "")
# --------------------------------------------------------------------------


# bandwith
# --------------------------------------------------------------------------
def bandwidth(edges):
    n = len(edges)

    def try_bandwidth(limit):
        """Try to find a numbering with given bandwidth limit"""
        numbering = [-1] * n  # numbering[node] = assigned number
        used = [False] * n  # used[number] = whether number is used
        
        node_allowed_bandwidth = [(0, n-1) for node in range(n)]

        def backtrack(node_idx):
            """Try to assign numbers to nodes"""
            # Base case: all nodes numbered
            if node_idx == n:
                return True

            # Choose next node to number (could be optimized)

            # FIX 1: 
            # In the default implementation, the next node we assign a value to is just the sequential nodes starting from 0; 
            # this is not as optimal as picking a node with a small number of options, which reduces our branching and the 
            # width of the search tree. This is much like picking the most constrained node to assign. To implement this, 
            # we would pick the node with the most neighbours already assigned at each recursive step. This would give us the
            # node with the most constraints with more restrictions and would allow invalid assignments to be detected earlier, 
            # reducing branches. Overall, this would greatly reduce the branching and improve the algorithm's speed.
            node = -1
            # maxEdge = float("-inf")
            min_num_allowed_values = float("inf")

            for i in range(n):

                if numbering[i] == -1:

                    # numEdge = 0

                    # for neighbor in edges[i]:
                    #     if numbering[neighbor] != -1:
                    #         numEdge += 1

                    # if numEdge > maxEdge:
                    #     maxEdge = numEdge
                    #     node = i

                    # FIX 3:
                    num_allowed_values = (node_allowed_bandwidth[i][1] - node_allowed_bandwidth[i][0]) + 1

                    if num_allowed_values < min_num_allowed_values:
                        min_num_allowed_values = num_allowed_values
                        node = i


            # Try each available number
            for num in range(node_allowed_bandwidth[node][0], node_allowed_bandwidth[node][1] + 1):
                if used[num]:
                    continue

                # Check if this number violates bandwidth constraint
                valid = True
                
                for neighbor in edges[node]:
                    if numbering[neighbor] != -1:
                        if abs(num - numbering[neighbor]) > limit:
                            valid = False
                            break
                if not valid:
                    continue

                valid = True

                # Assign this number
                numbering[node] = num
                used[num] = True

                changes = []
                
                # FIX 2: 
                # We can have an allowed range of [0…n-1] for each node. After we select a node to be placed, we update the neighbours' 
                # allowed ranges so that they can still be assigned a valid number. If this interval becomes empty, as the ranges of 
                # high and low are not valid (low > high), then we can prune that branch. This is like constraint propagation, where 
                # we confirm that all remaining neighbours of our node can be a value based on the constraints. Additionally, using this 
                # new allowed range, we can try these numbers for the current node we are assigning, greatly reducing the looping in this 
                # function. Although there is now a list that tracks changes, increasing space complexity
                for neighbor in edges[node]:
                    if numbering[neighbor] == -1:

                        high_limit = num + limit
                        low_limit = num - limit

                        old_limit = node_allowed_bandwidth[neighbor]
                        
                        node_allowed_bandwidth[neighbor] = (max(node_allowed_bandwidth[neighbor][0], low_limit), min(node_allowed_bandwidth[neighbor][1], high_limit))

                        if(old_limit != node_allowed_bandwidth[neighbor]):
                            changes.append((neighbor, old_limit))
                        
                        if node_allowed_bandwidth[neighbor][0] > node_allowed_bandwidth[neighbor][1]:
                            valid = False
                            break


                if valid:
                    
                    if backtrack(node_idx + 1):
                        return True

                # Backtrack
                numbering[node] = -1
                used[num] = False

                # Revert the changes to the allowed bandwidth for the neighbors
                for neighbor, old_limit in changes:
                    node_allowed_bandwidth[neighbor] = old_limit

            return False

        return backtrack(0)

    # Iterative deepening: try bandwidth 1, 2, 3, ...
    for bw in range(1, n):
        if try_bandwidth(bw):
            return bw

    return n - 1
# --------------------------------------------------------------------------


# Stepping stones
# --------------------------------------------------------------------------
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

    # FIX 2: Precompute all neighbouurs for the all of the cells and store in a dictionary, this way we are not
    # recomputing the neighbors in the branching and recursive calls. This is more efficient because getting the neighbors
    # is O(n^2) normally and repeating this for computed cells is a waste. Therefore, by precomputing we can turn it into 
    # a constant time operation.
    neighbor_dict = {}

    for r in range(n):
        for c in range(n):
            neighbor_dict[(r, c)] = get_neighbors(r, c)

    # Apart of FIX 1: Where we build the original possible placements set. 
    for pos in ones:
        board[pos] = 1
        for neighbor in neighbor_dict[pos]:
            if neighbor not in board:
                possiblePlacements.add(neighbor)

    def get_sum(r, c):
        """Get sum of neighboring stones"""
        total = 0
        for neighbor in neighbor_dict[(r, c)]:
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
                for neighbor in neighbor_dict[(r, c)]:
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
# --------------------------------------------------------------------------


# unity_partition
# --------------------------------------------------------------------------
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
        for num in range(start, target_sum+1):
            
            reciprocal = Fraction(1, num)
            
            # Skip if reciprocal is too large
            if reciprocal > target_frac:
                continue

            # FIX 1: We are checking that in the best case if we take remaning recipriocal sums before we exceed our remaining budget for sum, 
            # we can still reach our target fraction. If our max fraction is less that our target fraction we know in the best case, taking
            # all the allowed remaining numbers, we won't reach our target fraction and this path will not lead to a solution.
            remaining_sum = target_sum - num
            remaining_fraction = target_frac - reciprocal
            temp = num+1
            max_fraction = 0 

            # FIX 2: Here we check that in the best case if we take the smallest reciprocal possible to reach our target remaining recipricol, 
            # will we exceed the remaining fraction. That then we know that the paths that come from this point will not lead to a solution and 
            # we can prune this path. As the smalled reciprocol sum is already greater than the remaining fraction, we know that any other recipricol 
            # sum will also be greater than the remaining fraction and thus we can prune this path.
            if(remaining_sum > 0 and Fraction(1, remaining_sum) > remaining_fraction):
                continue

            while True:
                if(remaining_sum - temp < 0):
                    break
                else:
                    remaining_sum -= temp
                    max_fraction += 1 / temp
                    temp += 1

            if(max_fraction < remaining_fraction):
                return None

            # Try adding this number
            current_list.append(num)
            result = backtrack(target_sum - num, remaining_fraction, current_list, num + 1)
            
            if result is not None:
                return result
            
            current_list.pop()
        
        return None
    
    result = backtrack(n, Fraction(1, 1), [], 2)
    return result if result else []
# --------------------------------------------------------------------------
