from unittest import TestCase

import os
from email import parser as ep
import matplotlib.pyplot as plt

from Quagga import Quagga, ListReaderRawEmailTexts
from Quagga.Utils.Annotation.AnnotatedEmails import AnnotatedEmails
from Quagga.Utils.Annotation.DenotationBlockConverter import DenotationBlockConverter
from Quagga.Utils.Reader.Email import EmailMessage
from Quagga.Utils.BlockParser.Normalizer import Normalizer
from Tests.TestUtils import eq

from Levenshtein import distance, ratio, setratio, seqratio


# this test evalutates the result of the whole pipeline
# it does not just check whether the blockparser separated the lines correctly
# but also takes normalizing into account
class TestEvaluateResults(TestCase):

	def get_relative_filename(self, file):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, file)
		return filename

	def setUp(self):
		self.annotatedDir = self.get_relative_filename('testData/datasets/Enron/annotated_all')
		self.mails_denotated = AnnotatedEmails(self.annotatedDir, lambda x: x).eval_set
		print("using eval set")
		self.quagga = Quagga(ListReaderRawEmailTexts([""]), "annotatedOutput")

	def test_levenshtein(self):
		eq(distance('a', 'ab'), 1)  # number of additions, deletions, updates

		eq(ratio('a', 'b'), 0)  # in [0, 1]
		eq(ratio('a', 'a'), 1)

		eq(setratio(['a', 'b'], ['b', 'a']), 1.0)  # in [0, 1] compares two sets by best fit, order doesnt matter
		eq(setratio(['c', 'd'], ['b', 'a']), 0)  # in [0, 1] compares two sets by best fit, order doesnt matter

		eq(seqratio(['a', 'b'], ['b', 'a']), 0.5)  # in [0, 1]
		eq(seqratio(['a', 'b'], ['a', 'b']), 1.0)  # in [0, 1]
		eq(seqratio(['a'], ['a', 'b']), 1.0)

	@staticmethod
	def clean_list(lines):
		if lines == '' or lines is None:
			lines = []
		if type(lines) is str:
			lines = [lines]
		lines = [TestEvaluateResults.clean_string(string) for string in lines]
		lines = [string for string in lines if string != '']

		words_split = []
		for line in lines:
			words_split.extend(line.split(" "))
		words_split = [TestEvaluateResults.clean_string(word) for word in words_split]
		words_split = [word for word in words_split if word != '']

		return words_split

	@staticmethod
	def clean_string(string):
		if string is None:
			string = ''
		string = string.replace('\t', '')
		string = string.replace('\n', '')
		string = string.replace('\r', '')
		string = string.lstrip()
		string = string.rstrip()
		string = string.lower()
		return string

	"""
	{'blocks': [{'from': 'jennifer.rudolph@enron.com', 'raw_from': 'jennifer.rudolph@enron.com', 'to': ['ca.team@enron.com'], 'raw_to': 'ca.team@enron.com', 'cc': '', 'raw_cc': '', 'sent': '2001-04-11 14:30:00 UTC', 'raw_sent': '2001-04-11 14:30:00', 'subject': 'NEWS: bill signed?', 'raw_subject': 'NEWS: bill signed?', 'type': 'root', 'raw_header': [], 'text': ['*  Heard through sources that SBX 43 (SDG&E rate freeze) was signed by the ', 'Governor today', "*  However, the Legislature's web site still doesn't reflect the signing.", '*  Let me know if you hear/see more news', '']}]}
	{'blocks': [{'from': None, 'raw_from': None, 'to': None, 'raw_to': None, 'cc': None, 'raw_cc': None, 'sent': None, 'raw_sent': None, 'subject': None, 'raw_subject': None, 'type': 'root', 'raw_header': [], 'text': ['*  Heard through sources that SBX 43 (SDG&E rate freeze) was signed by the ', 'Governor today', "*  However, the Legislature's web site still doesn't reflect the signing.", '*  Let me know if you hear/see more news', '']}]}

	"""

	@staticmethod
	def clean_block(block):
		block['from'] = TestEvaluateResults.clean_string(block['from'])
		block['raw_from'] = TestEvaluateResults.clean_string(block['raw_from'])
		block['to'] = TestEvaluateResults.clean_list(block['to'])
		block['raw_to'] = TestEvaluateResults.clean_list(block['to'])
		block['cc'] = TestEvaluateResults.clean_list(block['cc'])
		block['sent'] = TestEvaluateResults.clean_string(block['sent'])
		block['raw_sent'] = TestEvaluateResults.clean_string((block['raw_sent']))
		block['subject'] = TestEvaluateResults.clean_string(block['subject'])
		block['raw_header'] = TestEvaluateResults.clean_list(block['raw_header'])
		block['text'] = TestEvaluateResults.clean_list(block['text'])

		if block['type'] == 'forward':
			block['type'] = 'reply' # annotated doesnt have forward
			block['raw_to'] = '' # dont include to and cc from previous block then since we dont have it in annotations
			block['to'] = ''
			block['raw_subject'] = ''
			block['subject'] = ''

	def test_evaluate(self):
		overall_accuracy = {}

		mail_count = 0
		for mail in self.mails_denotated:
			raw = mail.original_email
			email_input = EmailMessage(mail.path, mail.filename, ep.Parser().parsestr(raw))
			predicted = self.quagga._predict(email_input.clean_body)
			parsed = self.quagga._parse(predicted, email_input)

			denotations = mail.denotations
			denotation_blocks = DenotationBlockConverter.convert(denotations)

			for i, (parsed_block, annotated_block) in enumerate(zip(parsed['blocks'], denotation_blocks['blocks'])):

				# since some annotations are not consistent (some have day before date)
				# we normalize the parsed and the annotated stuff, only the outcome matters anyway
				annotated_block['sent'] = Normalizer.normalize_sent(annotated_block['sent'])
				self.clean_block(parsed_block)
				self.clean_block(annotated_block)

				block_accuracy = {'from': 1,
				               'to': 1,
				               'cc': 1,
				               'sent': 1,
				               'subject': 1,
				               'raw_header': 1,
				               'type': 1,
				               'text': 1}
				if i == 0 and parsed_block['type'] == 'root' and annotated_block['type'] == 'root':
					block_accuracy['text'] = seqratio(parsed_block['text'], annotated_block['text'])
				else:
					block_accuracy['from'] = ratio(parsed_block['from'], annotated_block['from'])
					block_accuracy['to'] = setratio(parsed_block['raw_to'], annotated_block['to'])
					block_accuracy['cc'] = setratio(parsed_block['cc'], annotated_block['cc'])
					block_accuracy['sent'] = ratio(parsed_block['sent'], annotated_block['sent'])
					block_accuracy['subject'] = ratio(parsed_block['subject'], annotated_block['subject'])
					block_accuracy['raw_header'] = seqratio(parsed_block['raw_header'], annotated_block['raw_header'])
					block_accuracy['type'] = ratio(parsed_block['type'], annotated_block['type'])
					block_accuracy['text'] = seqratio(parsed_block['text'], annotated_block['text'])

				annotated_block['error'] = block_accuracy

			if len(parsed['blocks']) != len(denotation_blocks['blocks']):
				print("blocks have different length, skipping")
				continue

			mail_accuracy = {'from': 0,
				               'to': 0,
				               'cc': 0,
				               'sent': 0,
				               'subject': 0,
				               'raw_header': 0,
				               'type': 0,
				               'text': 0}
			for i, annotated_block in enumerate(denotation_blocks['blocks']):
				if i == 0:
					mail_accuracy['text'] += annotated_block['error']['text']
				else:
					for key in annotated_block['error'].keys():
						mail_accuracy[key] += annotated_block['error'][key]


			for key in mail_accuracy.keys():
				if key == 'text':
					mail_accuracy['text'] /= len(denotation_blocks['blocks'])
				else:
					if len(denotation_blocks['blocks']) == 1:
						mail_accuracy[key] = 1
					else:
						mail_accuracy[key] /= len(denotation_blocks['blocks']) - 1

			plt.plot(mail_accuracy.keys(), mail_accuracy.values(), label=mail.filename)
			for key in mail_accuracy.keys():
				try:
					overall_accuracy[key] += mail_accuracy[key]
				except KeyError:
					overall_accuracy[key] = mail_accuracy[key]
			mail_count += 1

		for key in overall_accuracy.keys():
			overall_accuracy[key] /= mail_count

		print(overall_accuracy)
		#plt.legend()
		plt.show()
