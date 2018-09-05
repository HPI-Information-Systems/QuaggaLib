from unittest import TestCase

from Quagga.Utils.BlockParser import BlockParser
from Quagga.Utils.Email import EmailMessage
import json
import os
import filecmp
from email import parser as ep

class TestBlockParser(TestCase):

	def setUp(self):



		self.test_data_dir = 'testData/two'
		self.test_output_dir = self.test_data_dir + '/output'
		self.test_expected_dir = self.test_data_dir + '/output_expected'

		self.block_parser = BlockParser()


	def test_parse_predictions(self):
		parser = ep.Parser()
		raw_mail = """Message-ID: <20646012.1075840326283.JavaMail.evans@thyme>
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
		predicted = [
			{'predictions': {'Body': 1.0, 'Header': 0.0},
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
			 {'predictions': {'Body': 1.0, 'Header': 0.0}, 'text': '<Embedded StdOleLink>'}]
		expected = {"blocks": [
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
		]}
		email_input = EmailMessage(self.test_data_dir, 'bass-e__sent_mail_20.txt', parser.parsestr(raw_mail))
		assert self.block_parser.parse_predictions(predicted, email_input) == expected
