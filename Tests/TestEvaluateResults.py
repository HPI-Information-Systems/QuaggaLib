from unittest import TestCase

import os
from email import parser as ep

from Quagga import Quagga, ListReaderRawEmailTexts
from Quagga.Utils.Annotation.AnnotatedEmails import AnnotatedEmails
from Quagga.Utils.Annotation.DenotationBlockConverter import DenotationBlockConverter
from Quagga.Utils.Reader.Email import EmailMessage
from Tests.TestUtils import eq

from Levenshtein import distance, ratio, setratio


class TestEvaluateResults(TestCase):

	def get_relative_filename(self, file):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, file)
		return filename

	def setUp(self):
		self.annotatedDir = self.get_relative_filename('testData/datasets/Enron/annotated_all')
		self.mails_denotated = AnnotatedEmails(self.annotatedDir, lambda x: x).train_set
		self.quagga = Quagga(ListReaderRawEmailTexts([""]), "annotatedOutput")

	def test_levenshtein(self):
		eq(distance('a', 'ab'), 1)  # number of additions, deletions, updates
		eq(ratio('a', 'b'), 0)  # in [0, 1]
		eq(setratio(['a', 'b'], ['b', 'c']), 0.5)  # in [0, 1] compares two sets by best fit, order doesnt matter

	def test_evaluate(self):
		for mail in self.mails_denotated:
			raw = mail.original_email
			input = EmailMessage("", "", ep.Parser().parsestr(raw))
			predicted = self.quagga._predict(input.clean_body)
			parsed = self.quagga._parse(predicted, input)

			denotations = mail.denotations
			denotation_blocks = DenotationBlockConverter.convert(denotations)

			print(parsed)
			print(denotation_blocks)
