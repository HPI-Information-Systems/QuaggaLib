from unittest import TestCase

from Quagga import Quagga, ListReaderExtractedBodies
from Quagga.Utils.Reader.AnnotatedReader import AnnotatedEmails
import os

class TestAnnotatedReader(TestCase):

	def get_relative_filename(self, file):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, file)
		return filename

	def setUp(self):
		self.annotatedDir = self.get_relative_filename('datasets/Enron/annotatedAll')
		self.annotatedEmails = AnnotatedEmails(self.annotatedDir, lambda x: x)

	def test_reader(self):
		pass
