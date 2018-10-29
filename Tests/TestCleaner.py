
from unittest import TestCase

from Quagga.Utils.BlockParser.BlockCleaner import BlockCleaner
import os

def eq(a, b):
	if a != b:
		print(a)
		print(b)
	assert a == b

class TestCleaner(TestCase):

	def get_relative_filename(self, file):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, file)
		return filename

	def setUp(self):
		self.cleaner = BlockCleaner()

	def testCleanMail(self):
		mail_parsed = {'blocks': [{'from': 'eric.bass@enron.com', 'to': 'phillip.love@enron.com', 'cc': "chance.rabon@enron.com, david.baumbach@enron.com, o'neal.winfree@enron.com", 'sent': '2001-03-26 21:33:00', 'subject': 'Re:', 'type': 'root', 'raw_header': [], 'text': ["That's it.  Thanks to plove I am no longer entering my own deals.", '', '', '']}, {'from': '  \tPhillip M Love  ', 'to': ' \tEric Bass/HOU/ECT@ECT', 'cc': ' \t ', 'sent': ' 03/26/2001 10:20 am', 'subject': ' \tRe:   ', 'type': 'reply', 'raw_header': ['', 'From:\tPhillip M Love', '03/26/2001 10:20 AM', 'To:\tEric Bass/HOU/ECT@ECT', 'cc:\t ', 'Subject:\tRe:   '], 'text': ['', 'We can always count on you to at least give us one on the error report.', 'PL', '', '', '', '', '', '<Embedded StdOleLink>']}]}
		for block in mail_parsed['blocks']:
			self.cleaner.clean(block)
		expected = {'blocks': [{'from': 'eric.bass@enron.com', 'to': 'phillip.love@enron.com', 'cc': "chance.rabon@enron.com, david.baumbach@enron.com, o'neal.winfree@enron.com", 'sent': '2001-03-26 21:33:00', 'subject': 'Re:', 'type': 'root', 'raw_header': [], 'text': ["That's it.  Thanks to plove I am no longer entering my own deals.", '', '', '']}, {'from': 'Phillip M Love', 'to': 'Eric Bass/HOU/ECT@ECT', 'cc': '', 'sent': '03/26/2001 10:20 am', 'subject': 'Re:', 'type': 'reply', 'raw_header': ['', 'From:\tPhillip M Love', '03/26/2001 10:20 AM', 'To:\tEric Bass/HOU/ECT@ECT', 'cc:\t ', 'Subject:\tRe:   '], 'text': ['', 'We can always count on you to at least give us one on the error report.', 'PL', '', '', '', '', '', '<Embedded StdOleLink>']}]}
		eq(mail_parsed, expected)

	# todo add more tests for edge cases..