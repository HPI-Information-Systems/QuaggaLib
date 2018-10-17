from unittest import TestCase

from Quagga import Quagga, EmailDirectoryReader, ListReaderRawEmailTexts
from Quagga.Utils.Reader.AnnotatedEmails import AnnotatedEmails
import os
from email import parser as ep
from Quagga.Utils.Reader.Email import EmailMessage


class TestAnnotatedReader(TestCase):

	def get_relative_filename(self, file):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, file)
		return filename

	def setUp(self):
		self.annotatedDir = self.get_relative_filename('datasets/Enron/annotated_all')
		self.mails_denotated = AnnotatedEmails(self.annotatedDir, lambda x: x).train_set
		self.quagga = Quagga(ListReaderRawEmailTexts([""]), "annotatedOutput")

	def test_denotation_to_blocks(self):
		blocks = {'blocks': [{'from': 'jennifer.rudolph@enron.com', 'to': ['ca.team@enron.com'], 'cc': '',
		                      'sent': '2001-04-11 14:30:00 UTC', 'subject': 'NEWS: bill signed?', 'type': 'root',
		                      'raw_header': [],
		                      'text': ['*  Heard through sources that SBX 43 (SDG&E rate freeze) was signed by the ',
		                               'Governor today',
		                               "*  However, the Legislature's web site still doesn't reflect the signing.",
		                               '*  Let me know if you hear/see more news', '']}]}
		denotations = [{'id': 1, 'start': 0, 'end': 206,
		                'text': "*  Heard through sources that SBX 43 (SDG&E rate freeze) was signed by the \nGovernor today\n*  However, the Legislature's web site still doesn't reflect the signing.\n*  Let me know if you hear/see more news\n",
		                'type': 'Body', 'meta': None}]

	def test_reader(self):
		for mail in self.mails_denotated:
			raw = mail.original_email
			m = EmailMessage("", "", ep.Parser().parsestr(raw))
			predicted = self.quagga._predict(m.clean_body)
			parsed = self.quagga._parse(predicted, m)

			denotations = mail.denotations

			#print(parsed)
			#print(denotations)
