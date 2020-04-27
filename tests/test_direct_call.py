#!/usr/bin/env python3

"""
@file test_direct_call.py
@author Anthony Remazeilles
@brief check the computation runs as expected

Copyright (C) 2020 Tecnalia Research and Innovation
Distributed under the Non-Profit Open Software License 3.0 (NPOSL-3.0).

"""

import os
import io
import unittest
import tempfile
import logging
import sys


class DirectCallTest(unittest.TestCase):
    """gather program tests
    """

    INPUT_DATA = "data_in.csv"

    def setUp(self):
        """Common initialization operations
        """

        self.log = logging.getLogger("test_log")

        self.log.debug("Setting up the test")

        self.log.debug("Testing direct program call ")
        rel_path = os.path.dirname(__file__)
        self.input_data_path = os.path.abspath(os.getcwd() + "/" + rel_path + "/data/input/" + self.INPUT_DATA)

        self.output_groundtruth_path = os.path.abspath(os.getcwd() + "/" + rel_path + "/data/output/")

        self.log.debug("Relative path: {}".format(rel_path))
        self.log.debug("Input data in: {}".format(self.input_data_path))
        self.log.debug("Output data in: {}".format(self.output_groundtruth_path))

        self.output_data_path = tempfile.mkdtemp()
        os.chmod(self.output_data_path, 0o777)

        # preparing the generation command

        self.command = "./run_pi " + self.input_data_path + " "
        self.command += self.output_data_path

        self.log.debug("Command generated: \n{}".format(self.command))

    def test_call(self):
        """test the run_pi script with stored input and output

        """

        self.log.info("Launching the run_pi command")
        # TODO how to catch the result of the command (error or success)
        os.system(self.command)

        self.log.info("Command launched")

        # check generated files
        output_files = os.listdir(self.output_data_path)
        output_files_expected = os.listdir(self.output_groundtruth_path)

        self.assertCountEqual(output_files, output_files_expected)

        # Check the content of each file

        for filename in output_files:
            self.log.debug("comparing file: {}".format(filename))

            file_generated = self.output_data_path + "/" + filename

            lines_generated = list()
            with open(file_generated) as f:
                for line in f:
                    lines_generated.append(line)

            file_groundtruth = self.output_groundtruth_path + "/" + filename

            lines_groundtruth = list()
            with open(file_groundtruth) as f:
                for line in f:
                    lines_groundtruth.append(line)

            # print("Comparing:\n{}\n with \n{}".format(lines_generated, lines_groundtruth))
            self.assertListEqual(lines_generated, lines_groundtruth)

        self.log.info("Test completed")


if __name__ == '__main__':
    print("test_direct_call -- testing image:")

    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    # TODO using https://stackoverflow.com/questions/11380413/python-unittest-passing-arguments
    # but it is mentioned as not preferrable.
    unittest.main()
