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