from unittest import TestCase

from Quagga import Quagga, EmailDirectoryReader, ModelBuilder
from Quagga.Utils.Email import EmailMessage
import json
import os
import filecmp
from email import parser as ep

class TestQuagga(TestCase):

	def setUp(self):
		self.test_data_dir = 'testData/two'
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
		self.test_output_dir = self.test_data_dir + '/output'
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
      [
          {
              "text": "Jill,",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          },
          {
              "text": "",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          },
          {
              "text": "I was wondering if I could get some information on the Costilla deal, ",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          },
          {
              "text": "specifically the repurchase option.  I need to know the term, locations, ",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          },
          {
              "text": "volume and strike price of the call.  ",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          },
          {
              "text": "",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          },
          {
              "text": "",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          },
          {
              "text": "Thanks,",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          },
          {
              "text": "",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          },
          {
              "text": "",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          },
          {
              "text": "Eric",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          },
          {
              "text": "x3-0977 ",
              "predictions": {
                  "Body": 1.0,
                  "Header": 0.0
              }
          }
      ]]
		self.test_parse_expected = [{"blocks": [
      {
        "from": "eric.bass@enron.com",
        "to": "phillip.love@enron.com",
        "cc": "chance.rabon@enron.com, david.baumbach@enron.com, o'neal.winfree@enron.com",
        "sent": "01/01/2000 12:12 PM",
        "subject": "Re:",
        "type": "root",
        "raw_header": [],
        "text": [
          "That's it.  Thanks to plove I am no longer entering my own deals.",
          "",
          "",
          ""
        ]
      },
      {
        "from": "  \tPhillip M Love 03/26/2001 10:20 AM",
        "to": " \tEric Bass/HOU/ECT@ECT",
        "cc": " \t ",
        "sent": " 03/26/2001 10:20 am",
        "subject": " \tRe:   ",
        "type": "reply",
        "raw_header": [
          "",
          "From:\tPhillip M Love",
          "03/26/2001 10:20 AM",
          "To:\tEric Bass/HOU/ECT@ECT",
          "cc:\t ",
          "Subject:\tRe:   "
        ],
        "text": [
          "",
          "We can always count on you to at least give us one on the error report.",
          "PL",
          "",
          "",
          "",
          "",
          "",
          "<Embedded StdOleLink>"
        ]
      }
    ]},
		{"blocks": [
		{
			"from": "eric.bass@enron.com",
			"to": "jill.zivley@enron.com",
			"cc": "",
			"sent": "01/01/2000 12:12 PM",
			"subject": "Costilla",
			"type": "root",
			"raw_header": [],
			"text": [
				"Jill,",
				"",
				"I was wondering if I could get some information on the Costilla deal, ",
				"specifically the repurchase option.  I need to know the term, locations, ",
				"volume and strike price of the call.  ",
				"",
				"",
				"Thanks,",
				"",
				"",
				"Eric",
				"x3-0977 "
			]
		}
	]}
	]

	def tearDown(self):
		pass

	def expected_filename(self, email_input):
		return self.test_expected_dir + '/' + email_input.filename

	def output_filename(self, email_input):
		return self.test_output_dir + '/' + email_input.filename

	def test_emails_input(self):
		for email_input in self.quagga.emails_input:
			with open(self.expected_filename(email_input) + Quagga.fileending_input(), 'r') as fp:
				expected_input = json.loads(fp.read())[Quagga._INPUT()]
				assert email_input.file == expected_input['file']
				assert email_input.folder == expected_input['folder']
				assert email_input.sent_string == expected_input['sent']
				assert email_input.id == expected_input['id']
				assert email_input.mailbox == expected_input['mailbox']
				assert email_input.subject == expected_input['subject']
				assert email_input.sender == expected_input['sender']
				assert email_input.xsender == expected_input['xsender']
				assert email_input.to == expected_input['to']
				assert email_input.xto == expected_input['xto']
				assert email_input.cc == expected_input['cc']
				assert email_input.xcc == expected_input['xcc']
				assert email_input.bcc == expected_input['bcc']
				assert email_input.xbcc == expected_input['xbcc']
				assert email_input.body == expected_input['body']
				assert email_input.clean_body == expected_input['clean_body']

	def test_store_input(self):
		self.quagga.store_input(self.test_output_dir)
		for email_input in self.quagga.emails_input:
			assert filecmp.cmp(self.expected_filename(email_input) + Quagga.fileending_input(),
			                   self.output_filename(email_input) + Quagga.fileending_input())






	def test__build_model(self):
		self.quagga.model = None
		self.quagga._build_model(ModelBuilder(with_crf=False, zones=5, trainset='asf'))
		assert self.quagga.model.with_crf == False
		assert self.quagga.model.zones == 5
		assert self.quagga.model.trainset == 'asf'


	def test__predict(self):
		assert self.quagga._predict(self.test_mails[0]) == self.test_predict_expected[0]
	def test_emails_predicted(self):
		for email_predicted, email_expected in zip(self.quagga.emails_predicted(input_reader=self.test_mails), self.test_predict_expected):
			assert email_predicted == email_expected
	def test_store_predicted(self):
		self.quagga.store_predicted(self.test_output_dir)
		for email_input in self.quagga.emails_input:
			assert filecmp.cmp(self.expected_filename(email_input) + Quagga.fileending_predicted(),
			                   self.output_filename(email_input) + Quagga.fileending_predicted())

	def test__parse(self):
		email_input = EmailMessage(self.test_data_dir, self.test_filename, ep.Parser().parsestr(self.test_raw_mail))
		assert self.quagga._parse(self.test_predict_expected[0], email_input) == self.test_parse_expected[0]

	def test_emails_parsed(self):
		for email_parsed, email_expected in zip(self.quagga.emails_parsed(prediction_reader=self.test_predict_expected), self.test_parse_expected):
			assert email_parsed == email_expected

	def test_store_parsed(self):
		self.quagga.store_parsed(self.test_output_dir)
		for email_input in self.quagga.emails_input:
			assert filecmp.cmp(self.expected_filename(email_input) + Quagga.fileending_parsed(),
			                   self.output_filename(email_input) + Quagga.fileending_parsed())

	def test_store_all(self):
		self.quagga.store_all(self.test_expected_dir)
		for email_input in self.quagga.emails_input:
			assert filecmp.cmp(self.expected_filename(email_input) + Quagga.fileending_input(),
			                   self.output_filename(email_input) + Quagga.fileending_input())
			assert filecmp.cmp(self.expected_filename(email_input) + Quagga.fileending_predicted(),
			                   self.output_filename(email_input) + Quagga.fileending_predicted())
			assert filecmp.cmp(self.expected_filename(email_input) + Quagga.fileending_parsed(),
			                   self.output_filename(email_input) + Quagga.fileending_parsed())

	def test_store_many(self):
		output_dir = 'testData/enron_tiny/output'
		self.quagga = Quagga(EmailDirectoryReader('testData/enron_tiny'), output_dir)
		self.quagga.store_all(output_dir)
