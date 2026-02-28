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
