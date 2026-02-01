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
        (1, 1, 1): 0
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
                left = prev[(check_pos - 1) % n]
                center = prev[check_pos]
                right = prev[(check_pos + 1) % n] if check_pos + 1 < pos else None
                
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

