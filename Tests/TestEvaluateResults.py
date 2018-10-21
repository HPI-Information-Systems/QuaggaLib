from unittest import TestCase

import os
from email import parser as ep
import matplotlib.pyplot as plt

from Quagga import Quagga, ListReaderRawEmailTexts
from Quagga.Utils.Annotation.AnnotatedEmails import AnnotatedEmails
from Quagga.Utils.Annotation.DenotationBlockConverter import DenotationBlockConverter
from Quagga.Utils.Reader.Email import EmailMessage
from Tests.TestUtils import eq

from Levenshtein import distance, ratio, setratio, seqratio


class TestEvaluateResults(TestCase):

	def get_relative_filename(self, file):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, file)
		return filename

	def setUp(self):
		self.annotatedDir = self.get_relative_filename('testData/datasets/Enron/annotated_all')
		self.mails_denotated = AnnotatedEmails(self.annotatedDir, lambda x: x).eval_set
		self.quagga = Quagga(ListReaderRawEmailTexts([""]), "annotatedOutput")

	def test_levenshtein(self):
		eq(distance('a', 'ab'), 1)  # number of additions, deletions, updates
		eq(ratio('a', 'b'), 0)  # in [0, 1]
		eq(setratio(['a', 'b'], ['b', 'a']), 1.0)  # in [0, 1] compares two sets by best fit, order doesnt matter
		eq(seqratio(['a', 'b'], ['b', 'a']), 0.5)  # in [0, 1]

	@staticmethod
	def clean_list(names):
		if names == '' or names is None:
			names = []
		if type(names) is str:
			names = [names]
		names = [TestEvaluateResults.clean_string(string) for string in names]
		names = [string for string in names if string != '']
		return names

	@staticmethod
	def clean_string(string):
		if string is None:
			string = ''
		string = string.replace(' ', '')
		string = string.lower()
		return string

	"""
	{'blocks': [{'from': 'jennifer.rudolph@enron.com', 'raw_from': 'jennifer.rudolph@enron.com', 'to': ['ca.team@enron.com'], 'raw_to': 'ca.team@enron.com', 'cc': '', 'raw_cc': '', 'sent': '2001-04-11 14:30:00 UTC', 'raw_sent': '2001-04-11 14:30:00', 'subject': 'NEWS: bill signed?', 'raw_subject': 'NEWS: bill signed?', 'type': 'root', 'raw_header': [], 'text': ['*  Heard through sources that SBX 43 (SDG&E rate freeze) was signed by the ', 'Governor today', "*  However, the Legislature's web site still doesn't reflect the signing.", '*  Let me know if you hear/see more news', '']}]}
	{'blocks': [{'from': None, 'raw_from': None, 'to': None, 'raw_to': None, 'cc': None, 'raw_cc': None, 'sent': None, 'raw_sent': None, 'subject': None, 'raw_subject': None, 'type': 'root', 'raw_header': [], 'text': ['*  Heard through sources that SBX 43 (SDG&E rate freeze) was signed by the ', 'Governor today', "*  However, the Legislature's web site still doesn't reflect the signing.", '*  Let me know if you hear/see more news', '']}]}

	"""

	@staticmethod
	def clean_block(block):  # todo later differentiate between raw and processed stuff
		block['from'] = TestEvaluateResults.clean_string(block['from'])
		block['to'] = TestEvaluateResults.clean_list(block['to'])
		block['cc'] = TestEvaluateResults.clean_list(block['cc'])
		block['sent'] = TestEvaluateResults.clean_string(block['sent'])  # todo use normalizer?
		block['subject'] = TestEvaluateResults.clean_string(block['subject'])
		block['type'] = 'reply' if block['type'] == 'forward' else block['type']  # annotated doesnt have forward
		block['raw_header'] = TestEvaluateResults.clean_list(block['raw_header'])
		block['text'] = TestEvaluateResults.clean_list(block['text'])

	def test_evaluate(self):
		overall_error = {}

		for mail in self.mails_denotated:
			raw = mail.original_email
			email_input = EmailMessage(mail.path, mail.filename, ep.Parser().parsestr(raw))
			predicted = self.quagga._predict(email_input.clean_body)
			parsed = self.quagga._parse(predicted, email_input)

			denotations = mail.denotations
			denotation_blocks = DenotationBlockConverter.convert(denotations)


			for i, (parsed_block, annotated_block) in enumerate(zip(parsed['blocks'], denotation_blocks['blocks'])):

				self.clean_block(parsed_block)
				self.clean_block(annotated_block)

				block_error = {'from': 0,
				               'to': 0,
				               'cc': 0,
				               'sent': 0,
				               'subject': 0,
				               'raw_header': 0,
				               'type': 0,
				               'text': 0}
				if i == 0 and parsed_block['type'] == 'root' and annotated_block['type'] == 'root':
					block_error['text'] = seqratio(parsed_block['text'], annotated_block['text'])
				else:
					block_error['from'] = ratio(parsed_block['from'], annotated_block['from'])
					block_error['to'] = setratio(parsed_block['to'], annotated_block['to'])
					block_error['cc'] = setratio(parsed_block['cc'], annotated_block['cc'])
					block_error['sent'] = ratio(parsed_block['sent'], annotated_block['sent'])
					block_error['subject'] = ratio(parsed_block['subject'], annotated_block['subject'])
					block_error['raw_header'] = seqratio(parsed_block['raw_header'], annotated_block['raw_header'])
					block_error['type'] = ratio(parsed_block['type'], annotated_block['type'])
					block_error['text'] = seqratio(parsed_block['text'], annotated_block['text'])

				annotated_block['error'] = block_error

			if len(parsed['blocks']) != len(denotation_blocks['blocks']):
				print("blocks have different length")

			mail_error = {}
			for annotated_block in denotation_blocks['blocks']:
				try:
					for key in annotated_block['error'].keys():
						try:
							mail_error[key] += annotated_block['error'][key]
						except KeyError:
							mail_error[key] = annotated_block['error'][key]
				except KeyError: # different length
					annotated_block['error'] = {'from': 1,
				               'to': 1,
				               'cc': 1,
				               'sent': 1,
				               'subject': 1,
				               'raw_header': 1,
				               'type': 1,
				               'text': 1}
					for key in annotated_block['error'].keys():
						try:
							mail_error[key] += annotated_block['error'][key]
						except KeyError:
							mail_error[key] = annotated_block['error'][key]


			for key in mail_error.keys():
				mail_error[key] /= len(denotation_blocks['blocks'])

			plt.plot(mail_error.keys(), mail_error.values(), label=mail.filename)
			for key in mail_error.keys():
				try:
					overall_error[key] += mail_error[key]
				except KeyError:
					overall_error[key] = mail_error[key]

		for key in overall_error.keys():
			overall_error[key] /= len(self.mails_denotated)

		print(overall_error)
		#plt.legend()
		plt.show()
