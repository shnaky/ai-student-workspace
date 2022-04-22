from module_1 import is_positive, is_even

def is_even_and_positive(x):
    """
    Please modify the body of this function so that it returns
    - True if `x` is an even and positive integer
    - False in all other cases
    """
    # This function body should be edited such that
    # it contains the correct solution
    return is_even(x) and is_positive(x)

    # one possibility would be to use the functions
    # provided by module_1
    # return is_even(x) and is_positive(x)