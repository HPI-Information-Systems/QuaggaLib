#!/usr/bin/env python3.6


from Quagga import Quagga
from Quagga import EmailDirectoryReader, ListReaderRawEmailTexts, ListReaderExtractedBodies, TempQuaggaReader


import os.path


def get_relative_filename(file):
	dirname = os.path.dirname(__file__)
	filename = os.path.join(dirname, file)
	return filename



"""@profile
def profile_test(quagga, output_dir):
	quagga.store_input(output_dir)
	quagga.store_predicted(output_dir)
	quagga.store_parsed(output_dir)
	quagga.store_parsed(output_dir, prediction_reader=TempQuaggaReader(Quagga.PREDICTED_NAME(), output_dir))
	quagga.store_all(output_dir)"""

"""
"""

input_dir = get_relative_filename("Tests/testData/enron_small")
#input_dir = get_relative_filename("/san2/data/websci/email_datasets/enron_original")
output_dir = get_relative_filename("Tests/testData/output")
#output_dir = get_relative_filename("/san2/data/websci/email_datasets/enron_quagga")

quagga = Quagga(EmailDirectoryReader(input_dir), output_dir)

# profile_test(quagga, output_dir)

quagga.store_parsed(output_dir, prediction_reader=TempQuaggaReader(Quagga.PREDICTED_NAME, output_dir))