#!/usr/bin/env python3
"""
Created on 16 February 2020

@author: Lee Boon Keong
@github: 1bk
"""

import csv
import re
from os import path

import pandas as pd
import requests
from requests import Response
from typing import List

from util.tools import create_dir
from util.yaml_config import read_yaml_file

pd.set_option('display.max_columns', 150)
pd.set_option('display.width', 150)

PARENT_PATH: str = path.dirname(__file__)
ROOT_PATH: str = path.abspath(path.join(PARENT_PATH, '..'))
DBT_DATA_DIR: str = path.join(ROOT_PATH, 'dbt/data')
OUTPUT_DIR: str = path.join(PARENT_PATH, 'output')

CONFIG = read_yaml_file(path.join(PARENT_PATH, 'config.yaml'))
HEADERS = CONFIG['HEADERS']
AIRPORT_WEBSITE = CONFIG['WEBSITE']['AIRPORTS']

OUTPUT_FILE_NAME = CONFIG['OUTPUT']['FILE_NAME']['AIRPORTS']


def main():
    print(f'Downloading raw airport data from `{AIRPORT_WEBSITE}`.')
    response: Response = requests.get(AIRPORT_WEBSITE)

    create_dir(OUTPUT_DIR)

    output_file_path_1: str = path.join(DBT_DATA_DIR, OUTPUT_FILE_NAME)
    output_file_path_2: str = path.join(OUTPUT_DIR, OUTPUT_FILE_NAME)

    output_csv(headers=HEADERS, response=response, file_path=output_file_path_1)
    output_csv(headers=HEADERS, response=response, file_path=output_file_path_2)

    print('Done')


def output_csv(headers: List[str], response: Response, file_path: str) -> None:
    """Simple function to save request.Response data to CSV."""
    print(f'Saving data to `{path.abspath(file_path)}`.')
    with open(file_path, 'w') as f:
        w: csv.DictWriter = csv.writer(f)
        w.writerow(headers)
        for line in response.iter_lines(decode_unicode=True):
            # REGEX Source: https://stackoverflow.com/questions/18893390/splitting-on-comma-outside-quotes
            w.writerow(re.split(r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", line))


if __name__ == '__main__':
    main()
