#!/usr/bin/env python3
"""
Created on 16 February 2020

@author: Lee Boon Keong
@github: 1bk
"""

import os

import yaml

from util.exceptions import YAMLFileNotFound


def read_yaml_file(yaml_file_path: str) -> dict:
    """
    This function reads the YAML file and returns the contents as a dictionary object.

    :param yaml_file_path:  Path to YAML file to be loaded
    :return:                A dictionary object
    """
    if not os.path.isfile(yaml_file_path):
        raise YAMLFileNotFound()

    with open(yaml_file_path, 'r') as config:
        try:
            configuration: dict = yaml.safe_load(config)
        except yaml.YAMLError:
            print("Error importing YAML configuration file")

    return configuration
