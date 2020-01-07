def is_multiple(n, comparison):
    return n % comparison == 0


def word_buzz(n, comparison_1, comparison_2, word_1, word_2):
    if is_multiple(n, comparison_1) and is_multiple(n, comparison_2):
        return word_1 + word_2

    elif is_multiple(n, comparison_1):
        return word_1

    elif is_multiple(n, comparison_2):
        return word_2

    else:
        return n

def fizz_buzz(n, comparison_1, comparison_2):
    return word_buzz(n, comparison_1, comparison_2, 'fizz', 'buzz')
