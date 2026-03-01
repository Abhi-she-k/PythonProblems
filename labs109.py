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
                
                # FIX 2: We can have a allowed range of numbers for each node after we select a node to be place we update the neibourse allowed ranges so that they can still be assigned a valid number.
                # If this interval becomes empty, as the ranges of high and low are not valid (high > low) then we can prune that branch. Addtionally using this new allowed range, we can only try these numbers
                # for the current node we are assigning, greatly reducing the looping in this function. With this implementation, we are also storing our changes so that we can backtrack when we need to
                # prune this branch. 
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