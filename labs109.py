def ryerson_letter_grade(n):
    if n < 50:
        return 'F'
    elif n > 89:
        return 'A+'
    elif n > 84:
        return 'A'
    elif n > 79:
        return 'A-'
    tens = n // 10
    ones = n % 10
    if ones < 3:
        adjust = "-"
    elif ones > 6:
        adjust = "+"
    else:
        adjust = ""
    return "DCB"[tens - 5] + adjust

# def reverse_110(current):
#     n = len(current)
    
#     # Rule 110 lookup table: maps (left, center, right) to next state
#     rule_110 = {
#         (0, 0, 0): 0,
#         (0, 0, 1): 1,
#         (0, 1, 0): 1,
#         (0, 1, 1): 1,
#         (1, 0, 0): 0,
#         (1, 0, 1): 1,
#         (1, 1, 0): 1,
#         (1, 1, 1): 0
#     
    
#     def apply_rule_110(prev):
#         """Apply Rule 110 to get next state"""
#         next_state = []
#         for i in range(n):
#             left = prev[(i - 1) % n]
#             center = prev[i]
#             right = prev[(i + 1) % n]
#             next_state.append(rule_110[(left, center, right)])
#         return next_state
    
#     def backtrack(prev, pos):
#         """Build previous state position by position"""
#         # Base case: filled all positions
#         if pos == n:
#             # Check if applying Rule 110 gives us current state
#             if apply_rule_110(prev) == current:
#                 return prev[:]
#             else:
#                 return None
        
#         # Try both 0 and 1 for this position
#         for value in [0, 1]:
#             prev.append(value)
            
#             # Check if this is still valid so far
#             # We can check positions that have enough neighbors filled in
#             if pos >= 2:
#                 # Check position pos-1
#                 check_pos = pos - 1
#                 left = prev[(check_pos - 1) % n]
#                 center = prev[check_pos]
#                 right = prev[(check_pos + 1) % n] if check_pos + 1 < pos else None
                
#                 if right is not None:
#                     expected = rule_110[(left, center, right)]
#                     if expected != current[check_pos]:
#                         prev.pop()
#                         continue
            
#             result = backtrack(prev, pos + 1)
#             if result is not None:
#                 return result
            
#             prev.pop()
        
#         return None
    
#     return backtrack([], 0)

def bandwidth(edges):
    n = len(edges)
    
    def try_bandwidth(limit):
        """Try to find a numbering with given bandwidth limit"""
        numbering = [-1] * n  # numbering[node] = assigned number
        used = [False] * n     # used[number] = whether number is used
        
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
            maxEdge = float('-inf')

            for i in range(n):

                if(numbering[i] == -1):

                    numEdge = 0
                    
                    for neighbor in edges[i]:
                        if numbering[neighbor] != -1:
                            numEdge += 1
                            
                    if(numEdge > maxEdge):
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


