#!/usr/bin/env python3.6

from pprint import pprint

from Quagga import Quagga
from Quagga import EmailDirectoryReader, ListReaderRawEmailTexts, ListReaderExtractedBodies, TempQuaggaReader

from Quagga.Utils.ModelBuilder import ModelBuilder
from Quagga.Utils.BlockParser import BlockParser

import os.path

def get_relative_filename(file):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        return filename

input_dir = get_relative_filename("Tests/testData/enron_tiny")
output_dir = get_relative_filename("Tests/testData/output")



quagga = Quagga(EmailDirectoryReader(input_dir), output_dir)



quagga.store_all(output_dir)
"""quagga.store_input(output_dir)
quagga.store_predicted(output_dir)
quagga.store_parsed(output_dir)"""
