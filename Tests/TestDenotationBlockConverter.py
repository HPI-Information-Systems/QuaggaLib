from unittest import TestCase

from Quagga import Quagga, ListReaderRawEmailTexts
from Quagga.Utils.Annotation.AnnotatedEmails import AnnotatedEmails
import os
from email import parser as ep
from Quagga.Utils.Reader.Email import EmailMessage
from Tests.TestUtils import eq
from Quagga.Utils.Annotation.DenotationBlockConverter import DenotationBlockConverter


class TestDenotationBlockConverter(TestCase):

	def get_relative_filename(self, file):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, file)
		return filename

	def test_convert(self):
		denotations = [{'id': 1, 'start': 0, 'end': 70,
		                'text': "That's it.  Thanks to plove I am no longer entering my own deals.\n\n\n\n\n",
		                'type': 'Body', 'meta': None},
		               {'id': 2, 'start': 70, 'end': 84, 'text': 'Phillip M Love', 'type': 'Header/Person/From',
		                'meta': None},
		               {'id': 3, 'start': 85, 'end': 95, 'text': '03/26/2001', 'type': 'Header/Sent/Date',
		                'meta': None},
		               {'id': 4, 'start': 96, 'end': 104, 'text': '10:20 AM', 'type': 'Header/Sent/Time',
		                'meta': None},
		               {'id': 5, 'start': 109, 'end': 118, 'text': 'Eric Bass', 'type': 'Header/Person/To',
		                'meta': None},
		               {'id': 6, 'start': 146, 'end': 149, 'text': 'Re:', 'type': 'Header/Subject', 'meta': None},
		               {'id': 7, 'start': 70, 'end': 153,
		                'text': 'Phillip M Love\n03/26/2001 10:20 AM\nTo:\tEric Bass/HOU/ECT@ECT\ncc:\t \nSubject:\tRe:   \n',
		                'type': 'Header', 'meta': None},
		               {'id': 8, 'start': 226, 'end': 228, 'text': 'PL', 'type': 'Body/Outro/Name', 'meta': None},
		               {'id': 9, 'start': 153, 'end': 255,
		                'text': '\nWe can always count on you to at least give us one on the error report.\nPL\n\n\n\n\n\n<Embedded StdOleLink>',
		                'type': 'Body', 'meta': None}]

		blocks = DenotationBlockConverter.convert(denotations)

		expected = {'blocks': [
			{'from': None, 'raw_from': None, 'to': None, 'raw_to': None, 'cc': None, 'raw_cc': None, 'sent': None,
			 'raw_sent': None, 'subject': None, 'raw_subject': None, 'type': 'root', 'raw_header': [],
			 'text': ["That's it.  Thanks to plove I am no longer entering my own deals.", '', '', '', '', '']},
			{'from': 'Phillip M Love', 'raw_from': 'Phillip M Love', 'to': ['Eric Bass'], 'raw_to': ['Eric Bass'],
			 'cc': [], 'raw_cc': [], 'sent': ' 03/26/2001 10:20 AM', 'raw_sent': ' 03/26/2001 10:20 AM',
			 'subject': None, 'raw_subject': None, 'type': 'reply',
			 'raw_header': 'Phillip M Love\n03/26/2001 10:20 AM\nTo:\tEric Bass/HOU/ECT@ECT\ncc:\t \nSubject:\tRe:   \n',
			 'text': ['', 'We can always count on you to at least give us one on the error report.', 'PL', '', '', '',
			          '', '', '<Embedded StdOleLink>']}]}

		eq(blocks, expected)
