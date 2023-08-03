# Problem Set 4A

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    
    # Base Case
    if len(sequence) == 1:
        return [sequence]
    
    # Recursive Call Stack with <> except First Letter
    perms = get_permutations(sequence[1:])
    
    print('function call:', perms)
    
    # First Letter to switch around 
    char = sequence[0]
    
    # List which contains the string bits and eventual end result
    result = []
    
    for perm in perms:
        for i in range(len(perm)+1):
            result.append(perm[:i] + char + perm[i:])
    return result 


