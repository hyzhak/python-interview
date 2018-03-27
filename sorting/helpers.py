import random


def get_dataset(n=128, range_min=1, range_max=100):
    return list(map(lambda _: random.randint(range_min, range_max), range(n)))


def is_sorted(data):
    """
    check whether list is sorted
    """
    return all([d_1 <= d2 for d_1, d2 in zip(data, data[1:])])


assert is_sorted([1, 2, 3, 4])
assert not is_sorted([4, 3, 2, 1])
assert not is_sorted([1, 3, 2, 4])


def swap(data, i, j):
    """
    swap two values in data list
    """
    data[i], data[j] = data[j], data[i]


l = [1, 2, 3]
swap(l, 0, 2)
assert l == [3, 2, 1]

__all__ = [
    get_dataset,
    is_sorted,
    swap,
]
