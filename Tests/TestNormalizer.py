from unittest import TestCase

from Quagga.Utils.BlockParser.Normalizer import Normalizer
import os


def eq(a, b):
	if a != b:
		print(a)
		print(b)
	assert a == b


class TestNormalizer(TestCase):

	def get_relative_filename(self, file):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, file)
		return filename

	def setUp(self):
		self.normalizer = Normalizer()

	def testNormalizeMail(self):
		mail_parsed = {'blocks': [
			{'from': 'eric.bass@enron.com', 'raw_from': 'eric.bass@enron.com', 'to': 'phillip.love@enron.com',
			 'raw_to': 'phillip.love@enron.com',
			 'cc': "chance.rabon@enron.com, david.baumbach@enron.com, o'neal.winfree@enron.com",
			 'raw_cc': "chance.rabon@enron.com, david.baumbach@enron.com, o'neal.winfree@enron.com",
			 'sent': '2001-03-26 21:33:00', 'raw_sent': '2001-03-26 21:33:00', 'subject': 'Re:', 'raw_subject': 'Re:',
			 'type': 'root', 'raw_header': [],
			 'text': ["That's it.  Thanks to plove I am no longer entering my own deals.", '', '', '']},
			{'from': 'Phillip M Love', 'raw_from': '  \tPhillip M Love  ', 'to': 'Eric Bass/HOU/ECT@ECT',
			 'raw_to': ' \tEric Bass/HOU/ECT@ECT', 'cc': '', 'raw_cc': ' \t ', 'sent': '03/26/2001 10:20 am',
			 'raw_sent': ' 03/26/2001 10:20 am', 'subject': 'Re:', 'raw_subject': ' \tRe:   ', 'type': 'reply',
			 'raw_header': ['', 'From:\tPhillip M Love', '03/26/2001 10:20 AM', 'To:\tEric Bass/HOU/ECT@ECT', 'cc:\t ',
			                'Subject:\tRe:   '],
			 'text': ['', 'We can always count on you to at least give us one on the error report.', 'PL', '', '', '',
			          '', '', '<Embedded StdOleLink>']}]}

		for block in mail_parsed['blocks']:
			self.normalizer.normalize(block)
		expected = {'blocks': [{'from': {'name': 'eric.bass', 'email': 'eric.bass@enron.com', 'raw_name': 'eric.bass@enron.com'}, 'raw_from': 'eric.bass@enron.com', 'to': [{'name': 'phillip.love', 'email': 'phillip.love@enron.com', 'raw_name': 'phillip.love@enron.com'}], 'raw_to': 'phillip.love@enron.com', 'cc': [{'name': 'chance.rabon', 'email': 'chance.rabon@enron.com', 'raw_name': 'chance.rabon@enron.com'}, {'name': 'david.baumbach', 'email': 'david.baumbach@enron.com', 'raw_name': 'david.baumbach@enron.com'}, {'name': "o'neal.winfree", 'email': "o'neal.winfree@enron.com", 'raw_name': "o'neal.winfree@enron.com"}], 'raw_cc': "chance.rabon@enron.com, david.baumbach@enron.com, o'neal.winfree@enron.com", 'sent': '2001-03-26 13:33:00 PST', 'raw_sent': '2001-03-26 21:33:00', 'subject': 'Re:', 'raw_subject': 'Re:', 'type': 'root', 'raw_header': [], 'text': ["That's it.  Thanks to plove I am no longer entering my own deals.", '', '', '']}, {'from': {'name': 'Phillip M Love', 'email': '', 'raw_name': 'Phillip M Love'}, 'raw_from': '  \tPhillip M Love  ', 'to': [{'name': 'Eric Bass', 'email': '', 'raw_name': 'Eric Bass/HOU/ECT@ECT'}], 'raw_to': ' \tEric Bass/HOU/ECT@ECT', 'cc': [], 'raw_cc': ' \t ', 'sent': '2001-03-26 02:20:00 PST', 'raw_sent': ' 03/26/2001 10:20 am', 'subject': 'Re:', 'raw_subject': ' \tRe:   ', 'type': 'reply', 'raw_header': ['', 'From:\tPhillip M Love', '03/26/2001 10:20 AM', 'To:\tEric Bass/HOU/ECT@ECT', 'cc:\t ', 'Subject:\tRe:   '], 'text': ['', 'We can always count on you to at least give us one on the error report.', 'PL', '', '', '', '', '', '<Embedded StdOleLink>']}]}

		eq(mail_parsed, expected)

# todo add more tests for edge cases..
