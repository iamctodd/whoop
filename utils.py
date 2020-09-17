"""
Created on: 16 Sep 2020
Created by: Philip.P_adm

Generic Utils functions
"""
import datetime as dt
import os
import re
from typing import Union

import numpy as np
import pandas as pd


def to_array(*args: Union[np.ndarray, list, tuple, pd.Series, np.datetime64, dt.datetime]):
    """Turning x into np.ndarray

    Yields:
        :class:'np.ndarray'

    Raises:
        ValueError if x is not in the listed type

    Example
    >>> import numpy as np
    >>> x,y,z = to_array(2,["a","b"],None)
    >>> date_array, =  to_array(np.datetime64("2019-01-01"))
    """

    for x in args:
        if isinstance(x, dt.date):
            yield np.array([x.strftime('%Y-%m-%d')], dtype='datetime64[D]')
            # if already an array yield as is
        elif isinstance(x, np.ndarray):
            yield x
        elif isinstance(x, (list, tuple)):
            yield np.array(x)
        elif isinstance(x, (pd.Series, pd.core.indexes.base.Index, pd.core.series.Series)):
            yield x.values
        elif isinstance(x, (int, float, str, bool, np.bool_)):
            yield np.array([x], dtype=type(x))
        # np.int{#}
        elif isinstance(x, (np.int8, np.int16, np.int32, np.int64)):
            yield np.array([x], dtype=type(x))
        # np.float{#}
        elif isinstance(x, (np.float16, np.float32, np.float64)):
            yield np.array([x], dtype=type(x))
        # np.bool*
        elif isinstance(x, (np.bool, np.bool_, np.bool8)):
            yield np.array([x], dtype=type(x))
        # np.datetime64
        elif isinstance(x, np.datetime64):
            yield np.array([x], "datetime64[D]")
        elif x is None:
            yield np.array([])
        else:
            from warnings import warn
            warn(f"Data type {type(x)} is not configured in to_array.")
            yield np.array([x], dtype=object)


def find(folder_path, pattern='.*', full_path=False, expect_one=True):
    """
    To find path(s) of file(s), especially useful for searching the same file pattern in multiple
    folders

    Args: folder_path (str, list, np.ndarray): Folder path(s). If multiple, it will be searched
    in its order pattern (str, list/tuple): regex pattern. Use list/tuple if you need multiple
    conditions full_path (bool, default False): if the full path of the files are needed
    expect_one (bool, default True): True will raise AssertionError if more than one file is found

    Returns:
        str: If one file is found
        list of str: If multiple files are found

    Note:
        This function can only handle same search pattern for every folderPath, and will return the first one it finds \
        if there are multiple folderPath. If it cannot find any, it will raise exceptions about the first folderPath

    Raises:
        FileNotFoundError: If folderPath(s) or pattern(s) does not match any findings
        FileExistsError: If more than one file is found when expectOne = True
    """
    if isinstance(folder_path, str):
        folder_path, = to_array(folder_path)

    for i, path in enumerate(folder_path):

        try:
            list_of_files = os.listdir(path=path)
        except (FileNotFoundError, OSError) as err:
            if i < len(folder_path) - 1:
                print(err.args[-1] + ' for "%s",... trying next' % path)
                continue  # go for next folderPath
            # out of luck
            err.args = (err.args[0], err.args[1] + ': %s' % path)  # raise with first folderPath
            raise

        if isinstance(pattern, (list, tuple)):
            n = len(pattern)
            # multi condition pattern matching
            ipattern = '|'.join(pattern)
            # strict matching of all required patters
            files = [f for f in list_of_files if
                     np.unique(re.findall(ipattern, f, re.IGNORECASE)).size == n]
        else:
            files = [f for f in list_of_files if re.findall(pattern, f, re.IGNORECASE)]

        try:
            if len(files) == 0:
                # remove some special characters before raising error
                if isinstance(pattern, str):
                    pattern = re.sub('[^A-Za-z0-9_.-]+', '', pattern)
                else:
                    pattern = [re.sub('[^A-Za-z0-9_.-]+', '', pat) for pat in pattern]
                raise FileNotFoundError(
                    '%s exists but no file names with pattern: %s' % (path, pattern))
            elif (len(files) > 1) and expect_one:
                raise FileExistsError('%s exists but %s files found' % (path, len(files)))

        except (FileNotFoundError, FileExistsError) as err:
            if i < len(folder_path) - 1:
                print(err.args[0] + ',... trying next')
                continue  # go for next folderPath
            # out of luck, raise with first folderPath
            err.args = (
                re.sub(path.replace('\\', '/'), folder_path[0],
                       err.args[0]),)  # re.sub doesn't like double backslashes
            raise

        break  # stop loop when we got the files we wanted

    if full_path:
        if path[-1] == '/':
            path = path[:-1]
        files = ['/'.join((path, f)) for f in files]

    if len(files) == 1 and expect_one:
        files = files[0]

    return files


def difference(a, b):
    """Give difference between two iterables by keeping values in first"""
    set_a, set_b = set(a), set(b)
    return set_a.difference(set_b)


if __name__ == '__main__':
    pass
