from task import get_full_name, is_string_contains, divide, sort_list, sort_list_param, merge_list

import pytest


@pytest.mark.full_name
def test_get_full_name():
    assert get_full_name('Ivan', 'Vitayev') == 'Ivan Vitayev'


@pytest.mark.params_full
@pytest.mark.parametrize("name, surname, full_name", [
    ('Gleb', 'Ivanov', 'Gleb Ivanov'),
    ('Vadim', 'Zviagintsev', 'Vadim Zviagintsev'),
    ('Gavriil', 'Ibragimov', 'Gavriil Ibragimov')
])
def test_get_full_name_param(name, surname, full_name):
    assert get_full_name(name, surname) == full_name


@pytest.mark.search
def test_is_string_contains():
    assert is_string_contains("one by one", 'one') is True
    assert is_string_contains('two by two', 'one') is False


@pytest.mark.param_search
@pytest.mark.parametrize('string, substring, result', [
    ('Two by Two', 'two', True),
    ('Four by four', 'Three', False),
    ('Four by four', 'Four', True),
    ('I love live', 'live', True),
])
def test_is_string_contains_params(string, substring, result):
    assert is_string_contains(string, substring) == result


@pytest.mark.divide
def test_divide():
    assert divide(4, 2) == 2


@pytest.mark.param_divide
@pytest.mark.parametrize('a, b, result', [
    (4, 2, 2),
    (5, 0, 'Деление на ноль запрещено'),
    (-22, -11, 2),
    (3.14, 2, 1.57)
])
def test_divide_param(a, b, result):
    assert divide(a, b) == result


@pytest.mark.sort
def test_sort_list(sort_list):
    number = [5, 3, 21, 12, 1]
    exp = [1, 3, 5, 12, 21]
    assert sort_list(number) == exp


@pytest.mark.sorted
def test_sort_list_param(sort_list_param):
    list_numbers, expect = sort_list_param
    result = sorted(list_numbers)
    assert result == expect


@pytest.mark.merge
def test_merge(merge_list):
    result = merge_list([4, 5, 6], [1, 2, 3])
    assert sorted(result) == [1, 2, 3, 4, 5, 6]


@pytest.mark.merge_param
@pytest.mark.parametrize('list1, list2, expected_sorted', [
    ([4, 5, 6], [1, 2, 3], [1, 2, 3, 4, 5, 6]),
    ([], [1, 2, 3], [1, 2, 3]),
    ([-6, 5, -4], [12, 0, 8], [-6, -4, 0, 5, 8, 12]),
    ([0], [-10,0,10], [-10, 0, 0, 10]),
])
def test_merge_param(merge_list, list1, list2, expected_sorted):
    merge_list = merge_list(list1, list2)
    assert sorted(merge_list) == expected_sorted
