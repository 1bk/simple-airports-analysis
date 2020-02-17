#!/usr/bin/env python3
"""
Created on 16 February 2020

@author: Lee Boon Keong
@github: 1bk
"""

import os
import shutil


def create_dir(dir_path: str, to_clear: bool = True) -> str:
    """Creates the specified directory with the option of clearing it if it exists.

    :param dir_path:    The desired directory path
    :param to_clear:    To clear the directory or not (default: True)
    :return:            The absolute path to the output directory
    """
    abs_path: str = os.path.abspath(dir_path)

    if not os.path.exists(abs_path):
        print('Directory "{}" does not exists. Creating...'.format(abs_path))
        os.makedirs(abs_path)
        print('Directory "{}" created!'.format(abs_path))

    else:
        if to_clear:
            print('Directory "{}" exists. Clearing...'.format(abs_path))
            clear_dir(abs_path)
            print('Directory "{}" cleared!'.format(abs_path))
        else:
            print('Directory "{}" exists. Not clearing.'.format(abs_path))

    return abs_path


def clear_dir(dir_path: str) -> None:
    """Clears all contents of the specified directory."""
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Error in deleting: {} \n{}'.format(file_name, e))
