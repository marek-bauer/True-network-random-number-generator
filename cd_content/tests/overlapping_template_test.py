import math


# Implementation of KMP algorithm https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
def count_occurrences(text, pattern):
    """Counts number of occurrences of pattern in text"""
    m = len(pattern)
    n = len(text)

    pattern_pos = 0
    found = 0
    lps = get_lsp_array(pattern)

    text_pos = 0
    while text_pos < n:
        if pattern[pattern_pos] == text[text_pos]:
            text_pos += 1
            pattern_pos += 1

        if pattern_pos == m:
            found += 1
            pattern_pos = lps[pattern_pos - 1]

        elif text_pos < n and pattern[pattern_pos] != text[text_pos]:
            if pattern_pos != 0:
                pattern_pos = lps[pattern_pos - 1]
            else:
                text_pos += 1
    return found


def get_lsp_array(pattern):
    """Generates ancillary array for KMP algorithm"""
    pattern_length = len(pattern)
    lps = [0] * pattern_length
    length_of_longest = 0
    pos = 1

    while pos < pattern_length:
        if pattern[pos] == pattern[length_of_longest]:
            length_of_longest += 1
            lps[pos] = length_of_longest
            pos += 1
        else:
            if length_of_longest != 0:
                length_of_longest = lps[length_of_longest - 1]
            else:
                lps[pos] = 0
                pos += 1
    return lps


def probability_of_known_tail(pattern):
    """Computes sum probabilities of pattern occurring in next (length of pattern - 1) positions,
     knowing it occurred last time"""
    result = 0
    for i in range(1, len(pattern)):
        if pattern[0:-i] == pattern[i:]:
            result += 2 ** -(len(pattern) - i)
    return result


def overlapping_template_test(vector, pattern):
    """Tests randomness by counting occurrences of pattern in vector"""
    m = len(pattern)
    n = len(vector)
    expected_column = (2 ** (-m))
    expected_value = (n - m + 1) * expected_column
    base_var = expected_column * (1 - expected_column)
    tail_probabilities = probability_of_known_tail(pattern)
    var = base_var
    for i in range(1, n - m + 1):
        e_xy = (tail_probabilities + (i - 1) * 2 ** (-m)) / (2 ** m)
        ex_ey = expected_column * i * expected_column
        cov = e_xy - ex_ey
        var += base_var + 2 * cov
    q = count_occurrences(vector, pattern)
    return 1 - math.erf(abs(q - expected_value) / math.sqrt(2 * var))
