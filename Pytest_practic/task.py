import pytest


def get_full_name(name, surname):
    return f'{name} {surname}'


def is_string_contains(string, substring):
    if substring.lower() in string.lower():
        return True
    else:
        return False


def divide(a, b):
    if b == 0:
        return 'Деление на ноль запрещено'
    return a / b


@pytest.fixture
def sort_list():
    def sort_list_wrapper(list_of_numbers):
        sorted_list = sorted(list_of_numbers)
        return sorted_list

    return sort_list_wrapper


@pytest.fixture(params=[
    ([1, 54, 23, 21, 3, 9], [1, 3, 9, 21, 23, 54]),
    ([2, 55, 24, 22, 4, 10], [2, 4, 10, 22, 24, 55]),
    ([3, 56, 25, 23, 5, 11], [3, 5, 11, 23, 25, 56]),
    ([4, 57, 26, 24, 6, 12], [4, 6, 12, 24, 26, 57]),
])
def sort_list_param(request):
    return request.param


@pytest.fixture
def merge_list():
    def merge(list1, list2):
        return list1 + list2
    return merge
