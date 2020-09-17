# Created on 16 Sep 2020 for Unit tests

import unittest
from datetime import datetime

import numpy as np
import pandas as pd

from utils import to_array, difference


class TestUtils(unittest.TestCase):
    def test_to_array__list_ints(self):
        # lists - ints: check get same results as using np.array(list)
        list_ints = [1, 2, 3]
        x, = to_array(list_ints)
        y = np.array(list_ints)
        np.testing.assert_array_equal(x, y)

    def test_to_array__list_floats(self):
        # lists - floats: check get same results as using np.array(list)

        list_floats = [1.0, 2 / 100, 3.14]
        x, = to_array(list_floats)
        y = np.array(list_floats)
        np.testing.assert_array_equal(x, y)

    def test_to_array__list_str(self):
        # list - str
        list_str = ["A", "B", "C"]
        x, = to_array(list_str)
        y = np.array(list_str)
        np.testing.assert_array_equal(x, y)

    def test_to_array__list_mixed(self):
        # lists
        list_ints = [1, 2, 3]
        list_floats = [1.0, 2 / 100, 3.14]
        list_str = ["A", "B", "C"]
        x = [i for i in to_array(list_ints, list_floats, list_str)]
        y = [np.array(i) for i in [list_ints, list_floats, list_str]]
        np.testing.assert_array_equal(x, y)

    def test_to_array__tuple(self):
        x, = to_array((1, 2, 3, 4))
        y = np.array((1, 2, 3, 4))
        np.testing.assert_array_equal(x, y)

    def test_to_array__np_array(self):
        y = np.array([1, 2, 3])
        x, = to_array(y)
        np.testing.assert_array_equal(x, y)

    def test_to_array__mixed_single_values(self):
        # single values: ints, floats, str, bool
        listed_mixed_vals = [1, 2.0, '3', True]
        # - unpack the list
        z = [i for i in to_array(*listed_mixed_vals)]
        y = [np.array([i]) for i in listed_mixed_vals]
        np.testing.assert_array_equal(z, y)

    def test_to_array__single_value_np_dtypes(self):
        # single values: np dtypes
        list_int = [getattr(np, f'int{i}')(i) for i in [8, 16, 32, 64]]
        list_float = [getattr(np, f'float{i}')(i) for i in [16, 32, 64]]
        list_bool = [getattr(np, i)(1) for i in ['bool', 'bool8', 'bool_']]
        list_np_datetime = [np.datetime64('2020-12-03')]
        for ll in [list_int, list_float, list_bool, list_np_datetime]:
            z = [i for i in to_array(*ll)]
            y = [np.array([i]) for i in ll]
            np.testing.assert_array_equal(z, y)

    def test_to_array__none(self):
        x, = to_array(None)
        np.testing.assert_array_equal(x, np.array([]))

    def test_to_array__datetime(self):
        x, = to_array(datetime(2020, 12, 3))
        y = np.array(['2020-12-03'], dtype='datetime64[D]')
        np.testing.assert_array_equal(x, y)

    def test_to_array__pandas(self):
        # pandas
        # Series: list to Series and get values same as np.array from list
        # - NOTE: skiped listed_mixed_vals

        list_ints = [1, 2, 3]
        list_floats = [1.0, 2 / 100, 3.14]
        list_str = ["A", "B", "C"]
        list_int = [getattr(np, f'int{i}')(i) for i in [8, 16, 32, 64]]
        list_float = [getattr(np, f'float{i}')(i) for i in [16, 32, 64]]
        list_bool = [getattr(np, i)(1) for i in ['bool', 'bool8', 'bool_']]
        list_np_datetime = [np.datetime64('2020-12-03')]

        lls = [list_ints, list_floats, list_str, list_int, list_float, list_bool, list_np_datetime]
        pds = [pd.Series(i) for i in lls]
        z = [i for i in to_array(*pds)]
        y = [np.array(i) for i in lls]
        for j in range(len(z)):
            np.testing.assert_array_equal(z[j], y[j])

        # Index
        pds = [pd.Index(i) for i in lls]
        z = [i for i in to_array(*pds)]
        for j in range(len(z)):
            np.testing.assert_array_equal(z[j], y[j])

    def test_difference(self):
        self.assertEqual(difference([3, 10, 9], [3, 4, 10]),
                         {9},
                         "Difference function not working as expected")


if __name__ == '__main__':
    unittest.main()
