import typing
import itertools
from math import comb, floor

MAX_SUPPORTED_NUM_NOTES = 15
MAX_NUM_EXPANSIONS = comb(
    MAX_SUPPORTED_NUM_NOTES, floor((MAX_SUPPORTED_NUM_NOTES - 1) / 2.0)
)

"""
One of our goals is to expand 'notes' to a size of 'm_max' by adding some notes from itself.
We can create a vector 'expansion' (*) with size 'm_max' with elements from {0, 1, ..., notes.size() - 1}
(sorted in ascending order), then the desired expansion is simply { notes[expansion[i]] }.
'expansion_indexes[min][max][i]' is the 'i'th alternative of expansion (*) for 'notes.size() = min' and 'm_max = max'.

Take for example: if we have 3 notes C4, E4, G4,
but we need to expand to 5 notes, there are comb(5-1, 3-1) = 6 solutions 
(you can view it as choosing 2 gaps out of 4 gaps):

(1) C4   C4   C4 | E4 | G4
(2) C4   C4 | E4   E4 | G4
(3) C4   C4 | E4 | G4   G4
(4) C4 | E4   E4   E4 | G4
(5) C4 | E4   E4 | G4   G4
(6) C4 | E4 | G4   G4   G4

This corresponds to:
expansion_indexes[3][5][0] = [0, 0, 0, 1, 2]
expansion_indexes[3][5][1] = [0, 0, 1, 1, 2]
expansion_indexes[3][5][2] = [0, 0, 1, 2, 2]
expansion_indexes[3][5][3] = [0, 1, 1, 1, 2]
expansion_indexes[3][5][4] = [0, 1, 1, 2, 2]
expansion_indexes[3][5][5] = [0, 1, 2, 2, 2]
  

However, expansion_indexes itself has nothing to do with music - 
it is simply a cache of all possibilities of ways of choosing m_max items so that all m_min types of items are present
in the solution.
"""
expansion_indexes: typing.List[typing.List[typing.List[typing.List[int]]]] = []


def different_name(str1: str, str2: str) -> bool:
    """
    Here 'str1' and 'str2' are names of a chord.
    We extract names of each note in both chords to two vectors and compare whether they are equal.
    In this process, all spaces and numbers representing octave are discarded.
    If any note is represented by MIDI note number (or any other error occurs), the result is false.

    However, with music21, we probably don't need this function anymore
    :param str1:
    :param str2:
    :return:
    """
    raise NotImplementedError()


def insert(ar: typing.List[int], pos: typing.List[int], len1: int, len2: int):
    """
    e.g. ar = [0, 1, 2, 3], pos = [1, 1, 2]
    ar -> [0, 1, 2, 2, 3] -> [0, 1, 1, 2, 2, 3] -> [0, 1, 1, 1, 2, 2, 3]
    :param ar:
    :param pos:
    :param len1:
    :param len2:
    :return:
    """
    for i in range(len2 - 1, -1, -1):
        for j in range(len1 - 1, pos[i], -1):
            ar[j + 1] = ar[j]
        ar[pos[i] + 1] = pos[i]
        len1 += 1


def legacy_comb(n: int, m: int):
    res = 1
    for i in range(1, m + 1):
        res *= n + 1 - i
        res //= i
    return res


def legacy_initialize_expansion_indexes() -> typing.List[
    typing.List[typing.List[typing.List[int]]]
]:
    """
    This is straight translation from the original C++ implementation.
    :return:
    """
    ret_expansion_indexes = [
        [
            [[0] * MAX_SUPPORTED_NUM_NOTES for j in range(MAX_NUM_EXPANSIONS)]
            for k in range(MAX_SUPPORTED_NUM_NOTES + 1)
        ]
        for l in range(MAX_SUPPORTED_NUM_NOTES + 1)
    ]

    for _min in range(1, (MAX_SUPPORTED_NUM_NOTES + 1)):  # index starts with 1
        for _max in range(_min, (MAX_SUPPORTED_NUM_NOTES + 1)):  # index starts with 1
            diff = _max - _min
            size = legacy_comb(_max - 1, _min - 1)
            index1, index2, index3 = 0, 0, 0
            pos = [0] * MAX_SUPPORTED_NUM_NOTES
            for i in range(size):
                for j in range(_min):
                    ret_expansion_indexes[_min][_max][i][j] = j

            while index1 >= 0:
                if index2 >= _min:
                    index1 -= 1
                    index2 = pos[index1] + 1
                elif index1 == diff:
                    insert(ret_expansion_indexes[_min][_max][index3], pos, _min, diff)
                    index1 -= 1
                    index2 += 1
                    index3 += 1
                else:
                    pos[index1] = index2
                    index1 += 1
    return ret_expansion_indexes


def initialize_expansion_indexes() -> typing.List[
    typing.List[typing.List[typing.List[int]]]
]:
    """
    This is another implementation that is more pythonic.
    :return:
    """
    ret_expansion_indexes = [
        [
            [[0] * MAX_SUPPORTED_NUM_NOTES for j in range(MAX_NUM_EXPANSIONS)]
            for k in range(MAX_SUPPORTED_NUM_NOTES + 1)
        ]
        for l in range(MAX_SUPPORTED_NUM_NOTES + 1)
    ]

    for _min in range(1, MAX_SUPPORTED_NUM_NOTES + 1):  # index starts with 1
        for _max in range(_min, MAX_SUPPORTED_NUM_NOTES + 1):  # index starts with 1
            total_combinations = comb(_max - 1, _min - 1)
            for index, iter in enumerate(
                itertools.combinations(range(1, _max), _min - 1)
            ):
                new_item = []
                last_element = 0
                for i in range(_min - 1):
                    new_item += [i] * (iter[i] - last_element)
                    last_element = iter[i]
                new_item += [_min - 1] * (_max - last_element)

                # The padding below is for backward compatibility but they should not be used
                new_item += [0] * (MAX_SUPPORTED_NUM_NOTES - _max)
                ret_expansion_indexes[_min][_max][
                    total_combinations - 1 - index
                ] = new_item  # Reverse the order
    return ret_expansion_indexes


def intersect(
    A: typing.List[int], B: typing.List[int], regular: bool
) -> typing.List[int]:
    """
    Gets the intersection of two vectors.
    If 'regular' == false, the vectors will be sorted and duplicate elements of each vector will be deleted.
    """
    # Welcome to Python
    return list(set.intersection(set(A), set(B)))


def get_union(A: typing.List[int], B: typing.List[int]) -> typing.List[int]:
    """
    Gets the union of two vectors.
    :param A:
    :param B:
    :return:
    """
    ret = list(set.union(set(A), set(B)))
    sorted(ret)
    return ret
