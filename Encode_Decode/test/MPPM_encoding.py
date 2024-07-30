import math

def nchoosek(n, k):
    """
    Calculate the binomial coefficient "n choose k".
    """
    if k > n:
        return 0
    return math.comb(n, k)

def encode_MPPM(sk, n, r):
    """
    Encode a symbol sk using MPPM with parameters n and r.
    
    Parameters:
    sk (int): The symbol to encode.
    n (int): The size of the codeword.
    r (int): The number of pulsed slots.
    
    Returns:
    list: The encoded MPPM symbol as a list of 0s and 1s.
    """
    # Initialize an empty frame
    encoded_MPPM = [0] * n
    
    while n > 0:
        if 0 < r < n:
            y = nchoosek(n-1, r)
        else:
            y = 0
        
        # Encode sk by placing pulses in the appropriate slots
        if y <= sk:
            sk = sk - y
            encoded_MPPM[n-1] = 1
            r = r - 1
        else:
            encoded_MPPM[n-1] = 0
        
        n = n - 1
    
    return encoded_MPPM

# Example usage
sk = 9  # Example symbol to encode
n = 6   # Size of the codeword
r = 4   # Number of pulsed slots
encoded_symbol = encode_MPPM(sk, n, r)
print(encoded_symbol)