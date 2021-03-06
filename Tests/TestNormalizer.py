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
			{'from': 'eric.bass@enron.com', 'raw_from': 'eric.bass@enron.com', 'raw_xfrom': 'Eric Bass',
			 'to': 'phillip.love@enron.com', 'raw_to': 'phillip.love@enron.com',
			 'raw_xto': 'Phillip M Love <Phillip M Love/HOU/ECT@ECT>',
			 'cc': "chance.rabon@enron.com, david.baumbach@enron.com, o'neal.winfree@enron.com",
			 'raw_cc': "chance.rabon@enron.com, david.baumbach@enron.com, o'neal.winfree@enron.com",
			 'raw_xcc': "Chance Rabon <Chance Rabon/ENRON@enronXgate>, David Baumbach <David Baumbach/HOU/ECT@ECT>, O'Neal D Winfree <O'Neal D Winfree/HOU/ECT@ECT>",
			 'sent': '2001-03-26 21:33:00', 'raw_sent': '2001-03-26 21:33:00', 'subject': 'Re:', 'raw_subject': 'Re:',
			 'type': 'root', 'raw_header': [],
			 'text': ["That's it.  Thanks to plove I am no longer entering my own deals.", '', '', '']},
			{'from': '  \tPhillip M Love  ', 'raw_from': '  \tPhillip M Love  ', 'raw_xfrom': '  \tPhillip M Love  ',
			 'to': ' \tEric Bass/HOU/ECT@ECT', 'raw_to': ' \tEric Bass/HOU/ECT@ECT',
			 'raw_xto': ' \tEric Bass/HOU/ECT@ECT', 'cc': ' \t ', 'raw_cc': ' \t ', 'raw_xcc': ' \t ',
			 'sent': ' 03/26/2001 10:20 am', 'raw_sent': ' 03/26/2001 10:20 am', 'subject': ' \tRe:   ',
			 'raw_subject': ' \tRe:   ', 'type': 'reply',
			 'raw_header': ['', 'From:\tPhillip M Love', '03/26/2001 10:20 AM', 'To:\tEric Bass/HOU/ECT@ECT', 'cc:\t ',
			                'Subject:\tRe:   '],
			 'text': ['', 'We can always count on you to at least give us one on the error report.', 'PL', '', '', '',
			          '', '', '<Embedded StdOleLink>']}]}

		for block in mail_parsed['blocks']:
			self.normalizer.normalize(block)
		expected = {'blocks': [
			{'from': {'name': 'Eric Bass', 'email': 'eric.bass@enron.com', 'raw_name': 'eric.bass@enron.com'},
			 'raw_from': 'eric.bass@enron.com', 'raw_xfrom': 'Eric Bass', 'to': [
				{'name': 'Phillip M Love', 'email': 'phillip.love@enron.com', 'raw_name': 'phillip.love@enron.com'}],
			 'raw_to': 'phillip.love@enron.com', 'raw_xto': 'Phillip M Love <Phillip M Love/HOU/ECT@ECT>',
			 'cc': [{'name': 'Chance Rabon', 'email': 'chance.rabon@enron.com', 'raw_name': 'chance.rabon@enron.com'},
			        {'name': 'David Baumbach', 'email': 'david.baumbach@enron.com',
			         'raw_name': 'david.baumbach@enron.com'},
			        {'name': "O'Neal D Winfree", 'email': "o'neal.winfree@enron.com",
			         'raw_name': "o'neal.winfree@enron.com"}],
			 'raw_cc': "chance.rabon@enron.com, david.baumbach@enron.com, o'neal.winfree@enron.com",
			 'raw_xcc': "Chance Rabon <Chance Rabon/ENRON@enronXgate>, David Baumbach <David Baumbach/HOU/ECT@ECT>, O'Neal D Winfree <O'Neal D Winfree/HOU/ECT@ECT>",
			 'sent': '2001-03-26 13:33:00 PST', 'raw_sent': '2001-03-26 21:33:00', 'subject': 'Re:',
			 'raw_subject': 'Re:', 'type': 'root', 'raw_header': [],
			 'text': ["That's it.  Thanks to plove I am no longer entering my own deals.", '', '', '']},
			{'from': {'name': 'Phillip M Love', 'email': '', 'raw_name': 'Phillip M Love'},
			 'raw_from': '  \tPhillip M Love  ', 'raw_xfrom': '  \tPhillip M Love  ',
			 'to': [{'name': 'Eric Bass', 'email': '', 'raw_name': 'Eric Bass/HOU/ECT@ECT'}],
			 'raw_to': ' \tEric Bass/HOU/ECT@ECT', 'raw_xto': ' \tEric Bass/HOU/ECT@ECT',
			 'cc': [{'name': '', 'email': '', 'raw_name': ''}], 'raw_cc': ' \t ', 'raw_xcc': ' \t ',
			 'sent': '2001-03-26 02:20:00 PST', 'raw_sent': ' 03/26/2001 10:20 am', 'subject': ' \tRe:   ',
			 'raw_subject': ' \tRe:   ', 'type': 'reply',
			 'raw_header': ['', 'From:\tPhillip M Love', '03/26/2001 10:20 AM', 'To:\tEric Bass/HOU/ECT@ECT', 'cc:\t ',
			                'Subject:\tRe:   '],
			 'text': ['', 'We can always count on you to at least give us one on the error report.', 'PL', '', '', '',
			          '', '', '<Embedded StdOleLink>']}]}

		eq(mail_parsed, expected)

	def test_normalize_name_on_after_name(self):
		mail_parsed = {'blocks': [
			{'from': 'jeff.dasovich@enron.com', 'raw_from': 'jeff.dasovich@enron.com', 'raw_xfrom': 'Jeff Dasovich',
			 'to': 'ifsg230@mail.bus.utexas.edu', 'raw_to': 'ifsg230@mail.bus.utexas.edu',
			 'raw_xto': '"Joan Wagner" <IFSG230@mail.bus.utexas.edu> @ ENRON', 'cc': '', 'raw_cc': '', 'raw_xcc': '',
			 'sent': '2000-09-18 12:28:00', 'raw_sent': '2000-09-18 12:28:00', 'subject': 'Re: John Waters',
			 'raw_subject': 'Re: John Waters', 'type': 'root', 'raw_header': [],
			 'text': ['Holy moly and hee haw, how the heck are ya, and what are you up to?', '', '', '', '']},
			{'from': ' "Joan Wagner" <IFSG230@mail.bus.utexas.edu> on  ',
			 'raw_from': ' "Joan Wagner" <IFSG230@mail.bus.utexas.edu> on  ',
			 'raw_xfrom': ' "Joan Wagner" <IFSG230@mail.bus.utexas.edu> on  ', 'to': '  <Jeff_Dasovich@enron.com>',
			 'raw_to': '  <Jeff_Dasovich@enron.com>', 'raw_xto': '  <Jeff_Dasovich@enron.com>', 'cc': '   ',
			 'raw_cc': '   ', 'raw_xcc': '   ', 'sent': ' 09/18/2000 12:21:11 pm',
			 'raw_sent': ' 09/18/2000 12:21:11 pm', 'subject': '  John Waters', 'raw_subject': '  John Waters',
			 'type': 'reply', 'raw_header': ['"Joan Wagner" <IFSG230@mail.bus.utexas.edu> on 09/18/2000 12:21:11 PM',
			                                 'To: <Jeff_Dasovich@enron.com>', 'cc:  ', 'Subject: John Waters'],
			 'text': ['', '', 'Your boy had the quote of the day in the NY Times.', '',
			          '"Show me a kid who\'s not sneaking into R-rated movies and I\'ll show you',
			          "a failure.  All the future CEO's of this country are sneaking into", 'R-rated movies."', '',
			          'Happy Monday,', ' - jdw', '', '']}]}

		for block in mail_parsed['blocks']:
			self.normalizer.normalize(block)
		expected = {'blocks': [{'from': {'name': 'Jeff Dasovich', 'email': 'jeff.dasovich@enron.com', 'raw_name': 'jeff.dasovich@enron.com'}, 'raw_from': 'jeff.dasovich@enron.com', 'raw_xfrom': 'Jeff Dasovich', 'to': [{'name': 'Joan Wagner', 'email': 'ifsg230@mail.bus.utexas.edu', 'raw_name': 'ifsg230@mail.bus.utexas.edu'}], 'raw_to': 'ifsg230@mail.bus.utexas.edu', 'raw_xto': '"Joan Wagner" <IFSG230@mail.bus.utexas.edu> @ ENRON', 'cc': [], 'raw_cc': '', 'raw_xcc': '', 'sent': '2000-09-18 05:28:00 PDT', 'raw_sent': '2000-09-18 12:28:00', 'subject': 'Re: John Waters', 'raw_subject': 'Re: John Waters', 'type': 'root', 'raw_header': [], 'text': ['Holy moly and hee haw, how the heck are ya, and what are you up to?', '', '', '', '']}, {'from': {'name': 'Joan Wagner', 'email': 'IFSG230@mail.bus.utexas.edu', 'raw_name': '"Joan Wagner" <IFSG230@mail.bus.utexas.edu> on'}, 'raw_from': ' "Joan Wagner" <IFSG230@mail.bus.utexas.edu> on  ', 'raw_xfrom': ' "Joan Wagner" <IFSG230@mail.bus.utexas.edu> on  ', 'to': [{'name': '', 'email': 'Jeff_Dasovich@enron.com', 'raw_name': '<Jeff_Dasovich@enron.com>'}], 'raw_to': '  <Jeff_Dasovich@enron.com>', 'raw_xto': '  <Jeff_Dasovich@enron.com>', 'cc': [{'name': '', 'email': '', 'raw_name': ''}], 'raw_cc': '   ', 'raw_xcc': '   ', 'sent': '2000-09-18 05:21:11 PDT', 'raw_sent': ' 09/18/2000 12:21:11 pm', 'subject': '  John Waters', 'raw_subject': '  John Waters', 'type': 'reply', 'raw_header': ['"Joan Wagner" <IFSG230@mail.bus.utexas.edu> on 09/18/2000 12:21:11 PM', 'To: <Jeff_Dasovich@enron.com>', 'cc:  ', 'Subject: John Waters'], 'text': ['', '', 'Your boy had the quote of the day in the NY Times.', '', '"Show me a kid who\'s not sneaking into R-rated movies and I\'ll show you', "a failure.  All the future CEO's of this country are sneaking into", 'R-rated movies."', '', 'Happy Monday,', ' - jdw', '', '']}]}


		eq(mail_parsed, expected)
