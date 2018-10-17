from unittest import TestCase

from Quagga import Quagga, EmailDirectoryReader, ModelBuilder
import json
import os
import filecmp


class TestQuagga(TestCase):
	def get_relative_filename(self, file):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, file)
		return filename

	def setUp(self):
		self.test_data_dir = self.get_relative_filename('testData/two')
		self.test_filename = 'bass-e__sent_mail_20.txt'
		self.test_raw_mail = """Message-ID: <20646012.1075840326283.JavaMail.evans@thyme>
Date: Mon, 26 Mar 2001 13:33:00 -0800 (PST)
From: eric.bass@enron.com
To: phillip.love@enron.com
Subject: Re:
Cc: chance.rabon@enron.com, david.baumbach@enron.com, o'neal.winfree@enron.com
Mime-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
Bcc: chance.rabon@enron.com, david.baumbach@enron.com, o'neal.winfree@enron.com
X-From: Eric Bass
X-To: Phillip M Love <Phillip M Love/HOU/ECT@ECT>
X-cc: Chance Rabon <Chance Rabon/ENRON@enronXgate>, David Baumbach <David Baumbach/HOU/ECT@ECT>, O'Neal D Winfree <O'Neal D Winfree/HOU/ECT@ECT>
X-bcc: 
X-Folder: \ExMerge - Bass, Eric\'Sent Mail
X-Origin: BASS-E
X-FileName: eric bass 6-25-02.PST

That's it.  Thanks to plove I am no longer entering my own deals.




From:	Phillip M Love
03/26/2001 10:20 AM
To:	Eric Bass/HOU/ECT@ECT
cc:	 
Subject:	Re:   

We can always count on you to at least give us one on the error report.
PL





<Embedded StdOleLink>"""
		self.test_output_dir = self.get_relative_filename('testData/output')
		self.test_expected_dir = self.test_data_dir + '/output_expected'
		self.quagga = Quagga(EmailDirectoryReader(self.test_data_dir), self.test_output_dir)

		for f in os.listdir(self.test_output_dir):
			os.remove(os.path.join(self.test_output_dir, f))

		self.test_mails = ["""That's it.  Thanks to plove I am no longer entering my own deals.




From:	Phillip M Love
03/26/2001 10:20 AM
To:	Eric Bass/HOU/ECT@ECT
cc:	 
Subject:	Re:   

We can always count on you to at least give us one on the error report.
PL





<Embedded StdOleLink>""",
       """Jill,

I was wondering if I could get some information on the Costilla deal, 
specifically the repurchase option.  I need to know the term, locations, 
volume and strike price of the call.  


Thanks,


Eric
x3-0977 """]
		self.test_predict_expected = [
			[{'predictions': {'Body': 1.0, 'Header': 0.0},
			  'text': "That's it.  Thanks to plove I am no longer entering my own deals."},
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': ''},
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': ''},
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': ''},
			 {'predictions': {'Body': 0.0, 'Header': 1.0}, 'text': ''},
			 {'predictions': {'Body': 0.0, 'Header': 1.0}, 'text': 'From:\tPhillip M Love'},
			 {'predictions': {'Body': 0.0, 'Header': 1.0}, 'text': '03/26/2001 10:20 AM'},
			 {'predictions': {'Body': 0.0, 'Header': 1.0},
			  'text': 'To:\tEric Bass/HOU/ECT@ECT'},
			 {'predictions': {'Body': 0.0, 'Header': 1.0}, 'text': 'cc:\t '},
			 {'predictions': {'Body': 0.0, 'Header': 1.0}, 'text': 'Subject:\tRe:   '},
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': ''},
			 {'predictions': {'Body': 1.0, 'Header': 0.0},
			  'text': 'We can always count on you to at least give us one on the error '
			          'report.'},
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': 'PL'},
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': ''},
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': ''},
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': ''},
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': ''},
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': ''},
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': '<Embedded StdOleLink>'}],
			[{"text": "Jill,", "predictions": {"Body": 1.0, "Header": 0.0 } }, {"text": "", "predictions": {"Body": 1.0, "Header": 0.0 } }, {"text": "I was wondering if I could get some information on the Costilla deal, ", "predictions": {"Body": 1.0, "Header": 0.0 } }, {"text": "specifically the repurchase option.  I need to know the term, locations, ", "predictions": {"Body": 1.0, "Header": 0.0 } }, {"text": "volume and strike price of the call.  ", "predictions": {"Body": 1.0, "Header": 0.0 } }, {"text": "", "predictions": {"Body": 1.0, "Header": 0.0 } }, {"text": "", "predictions": {"Body": 1.0, "Header": 0.0 } }, {"text": "Thanks,", "predictions": {"Body": 1.0, "Header": 0.0 } }, {"text": "", "predictions": {"Body": 1.0, "Header": 0.0 } }, {"text": "", "predictions": {"Body": 1.0, "Header": 0.0 } }, {"text": "Eric", "predictions": {"Body": 1.0, "Header": 0.0 } }, {"text": "x3-0977 ", "predictions": {"Body": 1.0, "Header": 0.0 } } ]]
		self.test_parse_expected = [{'blocks': [{'from': 'eric.bass@enron.com', 'to': ['phillip.love@enron.com'],
		                        'cc': ['chance.rabon@enron.com', 'david.baumbach@enron.com',
		                               "o'neal.winfree@enron.com"], 'sent': '2001-03-26 19:33:00 UTC', 'subject': 'Re:',
		                        'type': 'root', 'raw_header': [],
		                        'text': ["That's it.  Thanks to plove I am no longer entering my own deals.", '', '',
		                                 '']}, {'from': 'Phillip M Love', 'to': ['Eric Bass/HOU/ECT@ECT'], 'cc': '',
		                                        'sent': '2001-03-26 08:20:00 UTC', 'subject': 'Re:', 'type': 'reply',
		                                        'raw_header': ['', 'From:\tPhillip M Love', '03/26/2001 10:20 AM',
		                                                       'To:\tEric Bass/HOU/ECT@ECT', 'cc:\t ',
		                                                       'Subject:\tRe:   '], 'text': ['',
		                                                                                     'We can always count on you to at least give us one on the error report.',
		                                                                                     'PL', '', '', '', '', '',
		                                                                                     '<Embedded StdOleLink>']}]}, {}]
	def tearDown(self):
		pass

	def expected_filename(self, email_input):
		return self.test_expected_dir + '/' + email_input.filename

	def output_filename(self, email_input):
		return self.test_output_dir + '/' + email_input.filename

	@staticmethod #todo use nose.tools.eq
	def assertComparisionError(expected, actual):
		TestQuagga.printComparisionError(expected, actual)
		assert expected == actual

	@staticmethod
	def printComparisionError(expected, actual):
		if expected != actual:
			print("expected output")
			print(expected)
			print("actual parsed output")
			print(actual)

	def test_emails_input(self):
		for email_input in self.quagga.emails_input:
			with open(self.expected_filename(email_input) + self.quagga.fileending_input, 'r') as fp:
				expected_input = json.loads(fp.read())[Quagga.INPUT_NAME]
				TestQuagga.assertComparisionError(email_input.file, expected_input['file'])
				TestQuagga.assertComparisionError(email_input.folder, expected_input['folder'])
				TestQuagga.assertComparisionError(email_input.sent_string, expected_input['sent'])
				TestQuagga.assertComparisionError(email_input.id, expected_input['id'])
				TestQuagga.assertComparisionError(email_input.mailbox, expected_input['mailbox'])
				TestQuagga.assertComparisionError(email_input.subject, expected_input['subject'])
				TestQuagga.assertComparisionError(email_input.sender, expected_input['sender'])
				TestQuagga.assertComparisionError(email_input.xsender, expected_input['xsender'])
				TestQuagga.assertComparisionError(email_input.to, expected_input['to'])
				TestQuagga.assertComparisionError(email_input.xto, expected_input['xto'])
				TestQuagga.assertComparisionError(email_input.cc, expected_input['cc'])
				TestQuagga.assertComparisionError(email_input.xcc, expected_input['xcc'])
				TestQuagga.assertComparisionError(email_input.bcc, expected_input['bcc'])
				TestQuagga.assertComparisionError(email_input.xbcc, expected_input['xbcc'])
				TestQuagga.assertComparisionError(email_input.body, expected_input['body'])
				TestQuagga.assertComparisionError(email_input.clean_body, expected_input['clean_body'])

	def test_store_input(self):
		self.quagga.store_input(self.test_output_dir)
		for email_input in self.quagga.emails_input:
			assert filecmp.cmp(self.expected_filename(email_input) + self.quagga.fileending_input,
			                   self.output_filename(email_input) + self.quagga.fileending_input)

	def test__build_model(self):
		self.quagga.model = None
		self.quagga._build_model(ModelBuilder(with_crf=False, zones=5, trainset='asf'))
		assert self.quagga.model.with_crf == False
		assert self.quagga.model.zones == 5
		assert self.quagga.model.trainset == 'asf'

	def test__predict(self):
		assert self.quagga._predict(self.test_mails[0]) == self.test_predict_expected[0]

	def test_emails_predicted(self):
		for email_predicted, email_expected in zip(self.quagga.emails_predicted(input_reader=self.test_mails),
		                                           self.test_predict_expected):
			TestQuagga.printComparisionError(email_expected, email_predicted)
			assert email_predicted == email_expected

	def test_store_predicted(self):
		self.quagga.store_predicted(self.test_output_dir)
		for email_input in self.quagga.emails_input:
			assert filecmp.cmp(self.expected_filename(email_input) + self.quagga.fileending_predicted,
			                   self.output_filename(email_input) + self.quagga.fileending_predicted)

	"""def test__parse(self):
		email_input = EmailMessage(self.test_data_dir, self.test_filename, ep.Parser().parsestr(self.test_raw_mail))
		assert self.quagga._parse(self.test_predict_expected[0], email_input) == self.test_parse_expected[0]"""

	"""def test_emails_parsed(self):
		for email_parsed, email_expected in zip(self.quagga.emails_parsed(prediction_reader=self.test_predict_expected), self.test_parse_expected):
			print(email_expected)
			print(email_parsed)
			assert email_parsed == email_expected"""

	# json validity check left out in all isfile checks
	def test_store_parsed(self):
		self.quagga.store_parsed(self.test_output_dir)
		for email_input in self.quagga.emails_input:
			assert os.path.isfile(self.output_filename(email_input) + self.quagga.fileending_parsed)

	def test_store_all(self):
		self.quagga.store_all(self.test_output_dir)
		for email_input in self.quagga.emails_input:
			assert os.path.isfile(self.output_filename(email_input) + self.quagga.fileending_input)
			assert os.path.isfile(self.output_filename(email_input) + self.quagga.fileending_predicted)
			assert os.path.isfile(self.output_filename(email_input) + self.quagga.fileending_parsed)

	def test_store_many(self):
		output_dir = 'testData/output'
		self.quagga = Quagga(EmailDirectoryReader('testData/enron_tiny'), output_dir)
		self.quagga.store_all(output_dir)
