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