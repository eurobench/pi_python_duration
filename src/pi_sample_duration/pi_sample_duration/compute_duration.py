#!/usr/bin/env python3
"""
@package pi_sample_duration
@file compute_duration.py
@author Anthony Remazeilles
@brief Compute an experiment duration based on a jointAngle File information

Copyright (C) 2020 Tecnalia Research and Innovation
Distributed under the pache 2.0 license.

"""

# Used to handle csv file as dataframe
import pandas as pd
import sys
from termcolor import colored
import os


def compute_duration(file_ja_name):

    try:
        data = pd.read_csv(file_ja_name)
    except FileNotFoundError as err:
        print(colored(
            "Could not load file {}: {}".format(file_ja_name, err),
            "red"))
        return -1

    print("\n")
    print(data.head())

    if 'timestamp' not in list(data):
        print(colored("Missing column timestamp", "red"))
        return -1

    time_start = data.iloc[0]['timestamp']
    time_end = data.iloc[-1]['timestamp']

    duration = time_end - time_start

    return duration


def store_result(file_out, value):

    file = open(file_out, 'w')
    file.write('type: \'scalar\'\nvalue: ' + format(value, '.5f') + '\n')
    file.close()

    return True


USAGE = """usage: run_pi file_in folder_out
file_in: csv file containing at least a timestamp column
folder_out: folder where the PI yaml file yaml file will be stored
"""


def main():
    if len(sys.argv) != 3:
        print(colored("Wrong input parameters !", "red"))
        print(colored(USAGE, "yellow"))
        return -1

    file_in = sys.argv[1]
    folder_out = sys.argv[2]

    # check input parameters are good
    if not os.path.exists(file_in):
        print(colored("Input file {} does not exist".format(file_in), "red"))
        return -1
    if not os.path.isfile(file_in):
        print(colored("Input path {} is not a file".format(file_in), "red"))
        return -1

    if not os.path.exists(folder_out):
        print(colored(
            "Output folder {} does not exist".format(folder_out),
            "red"))
        return -1
    if not os.path.isfile(file_in):
        print(colored("Output path {} is not a folder".format(file_in), "red"))
        return -1

    duration = compute_duration(file_in)

    if duration == -1:
        return -1

    file_out = folder_out + "/pi_duration.yaml"
    if not store_result(file_out, duration):
        return -1
    print(colored(
        "duration: {} stored in {}".format(duration, file_out),
        "green"))
    return 0
