def factorial( n ):
    """Compute n! recursively.

    :param n: an integer >= 0
    :returns: n!

    Because of Python's stack limitation, this won't
    compute a value larger than about a 1000!.

    >>> factorial(4)
    24
    >>> factorial(5)
    120
    """
    if n == 0: return 1
    return n * factorial(n-1)
