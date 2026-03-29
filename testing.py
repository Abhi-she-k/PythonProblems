def post_correspondence_problem(first, second, lo, hi):

    repeated_strings = {}

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

            if((new_first, new_second) in repeated_strings):
                if(repeated_strings[(new_first, new_second)] == True):
                    return True
                continue
            
            # FIX 1:
            # The first fix that was made was to improve the pruning. In the post_correspondence_problem implementation,
            # no matter if the addition of elements from the first and second lists would make the strings never be compatible.
            # If we check if the new first string or the new second string is in the prefix of the other, we know these strings
            # still have a chance at being equivalent later in the recursion. If not, then they have no chance.
            if (new_second[0 : len(new_first)] == new_first or new_first[0 : len(new_second)] == new_second):
                if backtrack(new_first, new_second):
                    return True
            else:
                repeated_strings[(new_first, new_second)] = False
                continue

        return False

    return backtrack("", "")



def post_correspondence_problem(first, second, lo, hi):
    memo = {}

    def backtrack(first_str, second_str):
        state = (first_str, second_str)
        if state in memo:
            return memo[state]

        if first_str == second_str and lo <= len(first_str) <= hi:
            memo[state] = True
            return True

        if len(first_str) > hi or len(second_str) > hi:
            memo[state] = False
            return False

        for i in range(len(first)):
            new_first = first_str + first[i]
            new_second = second_str + second[i]

            if new_first.startswith(new_second) or new_second.startswith(new_first):
                if backtrack(new_first, new_second):
                    memo[state] = True
                    return True

        memo[state] = False
        return False

    return backtrack("", "")