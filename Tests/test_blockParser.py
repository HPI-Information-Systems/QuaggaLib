from unittest import TestCase

from Quagga import Quagga, ListReaderExtractedBodies
from Quagga.Utils.BlockParser import BlockParser
from Quagga.Utils.Email import EmailMessage
import json
import os
import filecmp
from email import parser as ep


class TestBlockParser(TestCase):

	def get_relative_filename(self, file):
		dirname = os.path.dirname(__file__)
		filename = os.path.join(dirname, file)
		return filename

	def setUp(self):
		self.test_data_dir = self.get_relative_filename('testData/two')
		self.block_parser = BlockParser()

	def construct_email(self, filename, raw_mail):
		parser = ep.Parser()
		return EmailMessage(self.test_data_dir, filename, parser.parsestr(raw_mail))

	def test_parse_predictions(self):
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
		filename = 'bass-e__sent_mail_20.txt'
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

		email_input = self.construct_email(filename, raw_mail)
		assert self.generate_predict(email_input) == predicted

		expected = {'blocks': [{'from': 'eric.bass@enron.com', 'to': ['phillip.love@enron.com'],
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
		                                                                                     '<Embedded StdOleLink>']}]}

		parsed = self.block_parser.parse_predictions(predicted, email_input)
		print(parsed)
		assert parsed == expected

	def test_from_error_farmer_d(self):
		raw_mail = """Message-ID: <12955863.1075854025405.JavaMail.evans@thyme>
Date: Thu, 24 Feb 2000 01:44:00 -0800 (PST)
From: brenda.flores-cuellar@enron.com
To: edward.gottlob@enron.com, lauri.allen@enron.com, daren.farmer@enron.com, 
	dan.junek@enron.com, jared.kaiser@enron.com, judy.townsend@enron.com
Subject: RE: Options Training Classes
Mime-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
X-From: Brenda Flores-Cuellar
X-To: Edward D Gottlob, Lauri A Allen, Daren J Farmer, Dan Junek, Jared Kaiser, Judy Townsend
X-cc: 
X-bcc: 
X-Folder: \Darren_Farmer_Dec2000\All documents
X-Origin: Farmer-D
X-FileName: dfarmer.nsf

FYI

I am currently out of books.  I should be getting some more in today.  As 
soon as they come in, I will make sure you get a copy.

-Brenda

---------------------- Forwarded by Brenda Flores-Cuellar/HOU/ECT on 
02/23/2000 04:26 PM ---------------------------
To: Phillip K Allen/HOU/ECT@ECT, Eric Bass/HOU/ECT@ECT, Sandra F 
Brawner/HOU/ECT@ECT, Mike Grigsby/HOU/ECT@ECT, Keith Holst/HOU/ECT@ect, Brian 
Hoskins/HOU/ECT@ECT, Dick Jenkins/HOU/ECT@ECT, Peter F Keavey/HOU/ECT@ECT, 
Matthew Lenhart/HOU/ECT@ECT, Andrew H Lewis/HOU/ECT@ECT, Thomas A 
Martin/HOU/ECT@ECT, Greg McClendon/HOU/ECT@ECT, Brad McKay/HOU/ECT@ECT, Carey 
M Metz/HOU/ECT@ECT, Sarah Mulholland/HOU/ECT@ECT, Scott Neal/HOU/ECT@ECT, Eva 
Pao/HOU/ECT@ECT, Jim Schwieger/HOU/ECT@ECT, Elizabeth Shim/Corp/Enron@Enron, 
Hunter S Shively/HOU/ECT@ECT, Geoff Storey/HOU/ECT@ECT, Fletcher J 
Sturm/HOU/ECT@ECT, Patricia Tlapek/HOU/ECT@ECT
cc: Shirley Crenshaw/HOU/ECT@ECT 
Subject: RE: Options Training Classes

For those of you who did not see the memos from Jeff that went out on 
February 17th. & February 22nd. regarding the upcoming Options training 
classed, I have attached both memos below:



I have the books at my desk for those of you that have not received your 
copy.  

There will be a third memo in the next couple of days with regards to the 
location of the classes.

If you have any other questions, please feel free to contact me.

-Brenda
x31914


"""
		filename = 'farmer-d_all_documents_2491.txt'
		email_input = self.construct_email(filename, raw_mail)
		predicted = [
			{'text': 'FYI', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'I am currently out of books.  I should be getting some more in today.  As ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'soon as they come in, I will make sure you get a copy.',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '-Brenda', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '---------------------- Forwarded by Brenda Flores-Cuellar/HOU/ECT on ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '02/23/2000 04:26 PM ---------------------------',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'To: Phillip K Allen/HOU/ECT@ECT, Eric Bass/HOU/ECT@ECT, Sandra F ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Brawner/HOU/ECT@ECT, Mike Grigsby/HOU/ECT@ECT, Keith Holst/HOU/ECT@ect, Brian ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Hoskins/HOU/ECT@ECT, Dick Jenkins/HOU/ECT@ECT, Peter F Keavey/HOU/ECT@ECT, ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Matthew Lenhart/HOU/ECT@ECT, Andrew H Lewis/HOU/ECT@ECT, Thomas A ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Martin/HOU/ECT@ECT, Greg McClendon/HOU/ECT@ECT, Brad McKay/HOU/ECT@ECT, Carey ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'M Metz/HOU/ECT@ECT, Sarah Mulholland/HOU/ECT@ECT, Scott Neal/HOU/ECT@ECT, Eva ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Pao/HOU/ECT@ECT, Jim Schwieger/HOU/ECT@ECT, Elizabeth Shim/Corp/Enron@Enron, ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Hunter S Shively/HOU/ECT@ECT, Geoff Storey/HOU/ECT@ECT, Fletcher J ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Sturm/HOU/ECT@ECT, Patricia Tlapek/HOU/ECT@ECT',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'cc: Shirley Crenshaw/HOU/ECT@ECT ', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Subject: RE: Options Training Classes', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'For those of you who did not see the memos from Jeff that went out on ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'February 17th. & February 22nd. regarding the upcoming Options training ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'classed, I have attached both memos below:',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'I have the books at my desk for those of you that have not received your ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'copy.  ', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'There will be a third memo in the next couple of days with regards to the ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'location of the classes.', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'If you have any other questions, please feel free to contact me.',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '-Brenda', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'x31914', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}}]

		expected = {'blocks': [{'from': 'brenda.flores-cuellar@enron.com',
		                        'to': ['edward.gottlob@enron.com', 'lauri.allen@enron.com', 'daren.farmer@enron.com',
		                               'dan.junek@enron.com', 'jared.kaiser@enron.com', 'judy.townsend@enron.com'],
		                        'cc': '', 'sent': '2000-02-24 08:44:00 UTC', 'subject': 'RE: Options Training Classes',
		                        'type': 'root', 'raw_header': [], 'text': ['FYI', '',
		                                                                   'I am currently out of books.  I should be getting some more in today.  As ',
		                                                                   'soon as they come in, I will make sure you get a copy.',
		                                                                   '', '-Brenda', '']},
		                       {'from': 'Brenda Flores-Cuellar/HOU/ECT',
		                        'to': ['edward.gottlob@enron.com', 'lauri.allen@enron.com', 'daren.farmer@enron.com',
		                               'dan.junek@enron.com', 'jared.kaiser@enron.com', 'judy.townsend@enron.com'],
		                        'cc': '', 'sent': '2000-02-23 15:26:00 UTC', 'subject': None, 'type': 'forward',
		                        'raw_header': ['---------------------- Forwarded by Brenda Flores-Cuellar/HOU/ECT on ',
		                                       '02/23/2000 04:26 PM ---------------------------'], 'text': []},
		                       {'from': None, 'to': ['Phillip K Allen/HOU/ECT@ECT', 'Eric Bass/HOU/ECT@ECT',
		                                             'Sandra F  Brawner/HOU/ECT@ECT', 'Mike Grigsby/HOU/ECT@ECT',
		                                             'Keith Holst/HOU/ECT@ect', 'Brian  Hoskins/HOU/ECT@ECT',
		                                             'Dick Jenkins/HOU/ECT@ECT', 'Peter F Keavey/HOU/ECT@ECT',
		                                             'Matthew Lenhart/HOU/ECT@ECT', 'Andrew H Lewis/HOU/ECT@ECT',
		                                             'Thomas A  Martin/HOU/ECT@ECT', 'Greg McClendon/HOU/ECT@ECT',
		                                             'Brad McKay/HOU/ECT@ECT', 'Carey  M Metz/HOU/ECT@ECT',
		                                             'Sarah Mulholland/HOU/ECT@ECT', 'Scott Neal/HOU/ECT@ECT',
		                                             'Eva  Pao/HOU/ECT@ECT', 'Jim Schwieger/HOU/ECT@ECT',
		                                             'Elizabeth Shim/Corp/Enron@Enron', 'Hunter S Shively/HOU/ECT@ECT',
		                                             'Geoff Storey/HOU/ECT@ECT', 'Fletcher J  Sturm/HOU/ECT@ECT',
		                                             'Patricia Tlapek/HOU/ECT@ECT'],
		                        'cc': ['Shirley Crenshaw/HOU/ECT@ECT'], 'sent': None,
		                        'subject': 'RE: Options Training Classes', 'type': 'reply',
		                        'raw_header': ['To: Phillip K Allen/HOU/ECT@ECT, Eric Bass/HOU/ECT@ECT, Sandra F ',
		                                       'Brawner/HOU/ECT@ECT, Mike Grigsby/HOU/ECT@ECT, Keith Holst/HOU/ECT@ect, Brian ',
		                                       'Hoskins/HOU/ECT@ECT, Dick Jenkins/HOU/ECT@ECT, Peter F Keavey/HOU/ECT@ECT, ',
		                                       'Matthew Lenhart/HOU/ECT@ECT, Andrew H Lewis/HOU/ECT@ECT, Thomas A ',
		                                       'Martin/HOU/ECT@ECT, Greg McClendon/HOU/ECT@ECT, Brad McKay/HOU/ECT@ECT, Carey ',
		                                       'M Metz/HOU/ECT@ECT, Sarah Mulholland/HOU/ECT@ECT, Scott Neal/HOU/ECT@ECT, Eva ',
		                                       'Pao/HOU/ECT@ECT, Jim Schwieger/HOU/ECT@ECT, Elizabeth Shim/Corp/Enron@Enron, ',
		                                       'Hunter S Shively/HOU/ECT@ECT, Geoff Storey/HOU/ECT@ECT, Fletcher J ',
		                                       'Sturm/HOU/ECT@ECT, Patricia Tlapek/HOU/ECT@ECT',
		                                       'cc: Shirley Crenshaw/HOU/ECT@ECT ',
		                                       'Subject: RE: Options Training Classes'],
		                        'text': ['', 'For those of you who did not see the memos from Jeff that went out on ',
		                                 'February 17th. & February 22nd. regarding the upcoming Options training ',
		                                 'classed, I have attached both memos below:', '', '', '',
		                                 'I have the books at my desk for those of you that have not received your ',
		                                 'copy.  ', '',
		                                 'There will be a third memo in the next couple of days with regards to the ',
		                                 'location of the classes.', '',
		                                 'If you have any other questions, please feel free to contact me.', '',
		                                 '-Brenda', 'x31914', '', '', '']}]}

		parsed = self.block_parser.parse_predictions(predicted, email_input)
		print(parsed)
		assert parsed == expected

	def generate_predict(self, mail):
		quagga = Quagga(ListReaderExtractedBodies(''), '')

		return quagga._predict(mail.clean_body)

	def test_from_error_germany_c(self):
		raw_mail = """Message-ID: <1335181.1075853733451.JavaMail.evans@thyme>
Date: Thu, 30 Dec 1999 02:44:00 -0800 (PST)
From: chris.germany@enron.com
To: clarissa.garcia@enron.com, cindy.vachuska@enron.com, 
	pvillag@columbiaenergy.com, molly.lafuze@enron.com, 
	msharif@columbiaenergygroup.com, david.oliver@enron.com, 
	victoria.versen@enron.com
Subject: Jan sale to FirstEnergy @ Carroll Co Meter
Cc: katherine.kelly@enron.com, victor.lamadrid@enron.com, 
	chris.germany@enron.com, scott.hendrickson@enron.com
Mime-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
Bcc: katherine.kelly@enron.com, victor.lamadrid@enron.com, 
	chris.germany@enron.com, scott.hendrickson@enron.com
X-From: Chris Germany
X-To: Clarissa Garcia, Cindy Vachuska, pvillag@columbiaenergy.com, Molly LaFuze, msharif@columbiaenergygroup.com, David Oliver, Victoria Versen
X-cc: Katherine L Kelly, Victor Lamadrid, Chris Germany, Scott Hendrickson
X-bcc: 
X-Folder: \Chris_Germany_Dec2000\\Notes Folders\Ces
X-Origin: Germany-C
X-FileName: cgerman.nsf

CES is buying 2500 dth/day from Equitable in Tenn Z4.  CES is selling 2500 
dth/day to FirstEnergy in Tenn Z4.  Looks like a match to me.  I told Fred 
with Equitable the information John Singer gave to Phil below.  For future 
reference Fred's number is 412-395-3295.  A backup contact at Equitable is 
Steve Rafferty, 412-395-3268.

Per John, FirstEnergy bought the meter (??) from Beldon & Blake effective 
12/1/99.  On CNG, we are showing a purchase (deal 141688) and a sale (deal 
141952) for 2500 dth/day with Beldon & Blake.  I don't see a sale anywhere to 
FirstEnergy.  

Also, I still see an Equitable supply (deal 135956) on CNG for 3226 dth/day.  
I believe this is a duplicate of deal 138741 in Tetco M2.

Comments?

---------------------- Forwarded by Chris Germany/HOU/ECT on 12/30/99 10:23 
AM ---------------------------


pvillag@columbiaenergygroup.com on 12/29/99 03:29:10 PM
To: Chris Germany/HOU/ECT@ECT
cc:  
Subject: Jan sale to FirstEnergy @ Carroll Co Meter



Chris,

This has to do with that TENN zone 4 deal that you e-mailed me about this
morning. Like I mentioned earlier, we never scheduled this gas, it was handled
on a back to back basis.

Phil


---------------------- Forwarded by Phil Villagomez/CES/ColumbiaGas on 
12/29/99
03:33 PM ---------------------------

John Singer
12/29/99 03:05 PM


To: Phil Villagomez/CES/ColumbiaGas@ColumbiaGas
cc:
Subject: Jan sale to FirstEnergy @ Carroll Co Meter

Phil,
FirstEnergy called to change the contract number for the sale I made to them
(originally to Belden & Blake) to be delivered to the Carroll Co Meter.  The
new contract number is 32082.
If you receive this email before you page me, that's what the page is about.
Call or email me with any questions.
Thanks,
John

HAPPY NEW YEAR!!!!!!!!!!!!!!!!!!!

"""
		filename = 'germany-c_ces_357.txt'
		email_input = self.construct_email(filename, raw_mail)
		predicted = [
			{'text': 'CES is buying 2500 dth/day from Equitable in Tenn Z4.  CES is selling 2500 ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'dth/day to FirstEnergy in Tenn Z4.  Looks like a match to me.  I told Fred ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'with Equitable the information John Singer gave to Phil below.  For future ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': "reference Fred's number is 412-395-3295.  A backup contact at Equitable is ",
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Steve Rafferty, 412-395-3268.', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Per John, FirstEnergy bought the meter (??) from Beldon & Blake effective ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '12/1/99.  On CNG, we are showing a purchase (deal 141688) and a sale (deal ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': "141952) for 2500 dth/day with Beldon & Blake.  I don't see a sale anywhere to ",
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'FirstEnergy.  ', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Also, I still see an Equitable supply (deal 135956) on CNG for 3226 dth/day.  ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'I believe this is a duplicate of deal 138741 in Tetco M2.',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Comments?', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '---------------------- Forwarded by Chris Germany/HOU/ECT on 12/30/99 10:23 ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'AM ---------------------------', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'pvillag@columbiaenergygroup.com on 12/29/99 03:29:10 PM',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'To: Chris Germany/HOU/ECT@ECT', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'cc:  ', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Subject: Jan sale to FirstEnergy @ Carroll Co Meter',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Chris,', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'This has to do with that TENN zone 4 deal that you e-mailed me about this',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'morning. Like I mentioned earlier, we never scheduled this gas, it was handled',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'on a back to back basis.', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Phil', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '---------------------- Forwarded by Phil Villagomez/CES/ColumbiaGas on ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '12/29/99', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '03:33 PM ---------------------------', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'John Singer', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '12/29/99 03:05 PM', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'To: Phil Villagomez/CES/ColumbiaGas@ColumbiaGas',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'cc:', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Subject: Jan sale to FirstEnergy @ Carroll Co Meter',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Phil,', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'FirstEnergy called to change the contract number for the sale I made to them',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '(originally to Belden & Blake) to be delivered to the Carroll Co Meter.  The',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'new contract number is 32082.', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': "If you receive this email before you page me, that's what the page is about.",
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Call or email me with any questions.', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Thanks,', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'John', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'HAPPY NEW YEAR!!!!!!!!!!!!!!!!!!!', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}}]

		expected = {'blocks': [{'from': 'chris.germany@enron.com', 'to': ['clarissa.garcia@enron.com', 'cindy.vachuska@enron.com', 'pvillag@columbiaenergy.com', 'molly.lafuze@enron.com', 'msharif@columbiaenergygroup.com', 'david.oliver@enron.com', 'victoria.versen@enron.com'], 'cc': ['katherine.kelly@enron.com', 'victor.lamadrid@enron.com', 'chris.germany@enron.com', 'scott.hendrickson@enron.com'], 'sent': '1999-12-30 09:44:00 UTC', 'subject': 'Jan sale to FirstEnergy @ Carroll Co Meter', 'type': 'root', 'raw_header': [], 'text': ['CES is buying 2500 dth/day from Equitable in Tenn Z4.  CES is selling 2500 ', 'dth/day to FirstEnergy in Tenn Z4.  Looks like a match to me.  I told Fred ', 'with Equitable the information John Singer gave to Phil below.  For future ', "reference Fred's number is 412-395-3295.  A backup contact at Equitable is ", 'Steve Rafferty, 412-395-3268.', '', 'Per John, FirstEnergy bought the meter (??) from Beldon & Blake effective ', '12/1/99.  On CNG, we are showing a purchase (deal 141688) and a sale (deal ', "141952) for 2500 dth/day with Beldon & Blake.  I don't see a sale anywhere to ", 'FirstEnergy.  ', '', 'Also, I still see an Equitable supply (deal 135956) on CNG for 3226 dth/day.  ', 'I believe this is a duplicate of deal 138741 in Tetco M2.', '', 'Comments?', '']}, {'from': 'Chris Germany/HOU/ECT', 'to': ['clarissa.garcia@enron.com', 'cindy.vachuska@enron.com', 'pvillag@columbiaenergy.com', 'molly.lafuze@enron.com', 'msharif@columbiaenergygroup.com', 'david.oliver@enron.com', 'victoria.versen@enron.com'], 'cc': ['katherine.kelly@enron.com', 'victor.lamadrid@enron.com', 'chris.germany@enron.com', 'scott.hendrickson@enron.com'], 'sent': '1999-12-30 09:23:00 UTC', 'subject': None, 'type': 'forward', 'raw_header': ['---------------------- Forwarded by Chris Germany/HOU/ECT on 12/30/99 10:23 ', 'AM ---------------------------'], 'text': []}, {'from': 'pvillag@columbiaenergygroup.com on', 'to': ['Chris Germany/HOU/ECT@ECT'], 'cc': '', 'sent': '1999-12-29 14:29:10 UTC', 'subject': 'Jan sale to FirstEnergy @ Carroll Co Meter', 'type': 'reply', 'raw_header': ['', '', 'pvillag@columbiaenergygroup.com on 12/29/99 03:29:10 PM', 'To: Chris Germany/HOU/ECT@ECT', 'cc:  ', 'Subject: Jan sale to FirstEnergy @ Carroll Co Meter'], 'text': ['', '', '', 'Chris,', '', 'This has to do with that TENN zone 4 deal that you e-mailed me about this', 'morning. Like I mentioned earlier, we never scheduled this gas, it was handled', 'on a back to back basis.', '', 'Phil', '', '']}, {'from': 'Phil Villagomez/CES/ColumbiaGas', 'to': ['Chris Germany/HOU/ECT@ECT'], 'cc': '', 'sent': '1999-12-28 23:00:00 UTC', 'subject': None, 'type': 'forward', 'raw_header': ['---------------------- Forwarded by Phil Villagomez/CES/ColumbiaGas on ', '12/29/99'], 'text': []}, {'from': '---------------------------  John Singer', 'to': ['Phil Villagomez/CES/ColumbiaGas@ColumbiaGas'], 'cc': '', 'sent': '1999-12-29 02:05:00 UTC', 'subject': 'Jan sale to FirstEnergy @ Carroll Co Meter', 'type': 'reply', 'raw_header': ['03:33 PM ---------------------------', '', 'John Singer', '12/29/99 03:05 PM', '', '', 'To: Phil Villagomez/CES/ColumbiaGas@ColumbiaGas', 'cc:', 'Subject: Jan sale to FirstEnergy @ Carroll Co Meter'], 'text': ['', 'Phil,', 'FirstEnergy called to change the contract number for the sale I made to them', '(originally to Belden & Blake) to be delivered to the Carroll Co Meter.  The', 'new contract number is 32082.', "If you receive this email before you page me, that's what the page is about.", 'Call or email me with any questions.', 'Thanks,', 'John', '', 'HAPPY NEW YEAR!!!!!!!!!!!!!!!!!!!', '', '']}]}


		parsed = self.block_parser.parse_predictions(predicted, email_input)
		print(parsed)
		assert parsed == expected

	def test_giron_d(self):
		raw_mail = """Message-ID: <13840872.1075852222598.JavaMail.evans@thyme>
Date: Mon, 15 Oct 2001 08:08:09 -0700 (PDT)
From: souad.mahmassani@enron.com
To: denver.plachy@enron.com, martin.cuilla@enron.com, geoff.storey@enron.com, 
	virawan.yawapongsiri@enron.com, lisa.kinsey@enron.com, 
	tom.donohoe@enron.com, kevin.ruscitti@enron.com, h..lewis@enron.com, 
	trading <.williams@enron.com>, bryant.frihart@enron.com, 
	patrick.tucker@enron.com, c..giron@enron.com, s..pollan@enron.com, 
	e.murrell@enron.com, lindsay.culotta@enron.com, 
	justin.o'malley@enron.com, m..love@enron.com, 
	cora.pendergrass@enron.com, kirk.lenart@enron.com, 
	l..schrab@enron.com
Subject: FW: Classes
Cc: laura.luce@enron.com, s..shively@enron.com
Mime-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
Bcc: laura.luce@enron.com, s..shively@enron.com
X-From: Mahmassani, Souad </O=ENRON/OU=NA/CN=RECIPIENTS/CN=SMAHMASS>
X-To: Plachy, Denver </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Dplachy>, Cuilla, Martin </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Mcuilla>, Storey, Geoff </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Gstorey>, Yawapongsiri, Virawan </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Vyawapon>, Kinsey, Lisa </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Lkinsey>, Donohoe, Tom </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Tdonoho>, Ruscitti, Kevin </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Kruscit>, Lewis, Andrew H. </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Alewis>, Williams, Jason (Trading) </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Jwillia>, Frihart, Bryant </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Bfrihart>, Tucker, Patrick </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Ptucker>, Giron, Darron C. </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Dgiron>, Pollan, Sylvia S. </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Spollan>, Murrell, Russell E </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Rmurrel>, Culotta, Lindsay </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Lculotta>, O'Malley, Justin </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Jomalley>, Love, Phillip M. </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Plove>, Pendergrass, Cora </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Cpender>, Lenart, Kirk </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Klenart>, Schrab, Mark L. </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Mschrab>
X-cc: Luce, Laura </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Lluce>, Shively, Hunter S. </O=ENRON/OU=NA/CN=RECIPIENTS/CN=Hshivel>
X-bcc: 
X-Folder: \DGIRON (Non-Privileged)\Giron, Darron C.\Deleted Items
X-Origin: GIRON-D
X-FileName: DGIRON (Non-Privileged).pst

One more change to class time.  Today's class only (Midcon) will be held @ 1:45 in room 3270 (same room as our 2:30 daily meeting) .
Thanks
 -----Original Message-----
From: 	Mahmassani, Souad  
Sent:	Friday, October 12, 2001 3:18 PM
To:	Plachy, Denver; Cuilla, Martin; Storey, Geoff; Yawapongsiri, Virawan; Kinsey, Lisa; Donohoe, Tom; Ruscitti, Kevin; Lewis, Andrew H.; Williams, Jason (Trading); Frihart, Bryant; Tucker, Patrick; Giron, Darron C.; Pollan, Sylvia S.; Murrell, Russell E; Culotta, Lindsay; O'Malley, Justin; Love, Phillip M.
Cc:	Luce, Laura; Shively, Hunter S.
Subject:	FW: Classes

Just a reminder.  Classes begin Monday the 15th.  They will be in room 3321 from 3 to 4.  
Thanks,

 -----Original Message-----
From: 	Mahmassani, Souad  
Sent:	Tuesday, October 09, 2001 3:05 PM
To:	Plachy, Denver; Cuilla, Martin; Storey, Geoff; Yawapongsiri, Virawan; Kinsey, Lisa; Donohoe, Tom; Ruscitti, Kevin; Lewis, Andrew H.; Williams, Jason (Trading); Frihart, Bryant; Tucker, Patrick; Giron, Darron C.; Pollan, Sylvia S.; Murrell, Russell E; Culotta, Lindsay; O'Malley, Justin; Love, Phillip M.
Cc:	Luce, Laura; Hogan, Irena D.; Shively, Hunter S.
Subject:	RE: Classes

Classes have been moved.  We will begin classes on 15th and end on the 26th. 
Thanks
 -----Original Message-----
From: 	Mahmassani, Souad  
Sent:	Wednesday, October 03, 2001 3:47 PM
To:	Plachy, Denver; Cuilla, Martin; Storey, Geoff; Yawapongsiri, Virawan; Kinsey, Lisa; Donohoe, Tom; Ruscitti, Kevin; Lewis, Andrew H.; Williams, Jason (Trading); Frihart, Bryant; Tucker, Patrick; Giron, Darron C.; Pollan, Sylvia S.; Murrell, Russell E; Culotta, Lindsay; O'Malley, Justin; Love, Phillip M.
Cc:	Shively, Hunter S.; Luce, Laura
Subject:	Classes


I spoke to the professors and we decided that the Midcontinent class will be held Monday's and Wednesday's from 3:00 to 4:00, Ontario class will be held Tuesday's and Thursday's at the same time.  

Classes will commence Monday 8, 2001, and will continue until Thursday 19, 2001.  Midcontinent test will be held on Monday the 22nd and Ontario test will be held on Tuesday the 23rd.


Please e-mail any suggestions, conflict, registry.  

Thanks"""
		email_input = self.construct_email('giron-d_deleted_items_225.txt', raw_mail)
		predicted = [
			{
				'text': "One more change to class time.  Today's class only (Midcon) will be held @ 1:45 in room 3270 (same room as our 2:30 daily meeting) .",
				'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Thanks', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': ' -----Original Message-----', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'From: \tMahmassani, Souad  ', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Sent:\tFriday, October 12, 2001 3:18 PM', 'predictions': {'Body': 0.0, 'Header': 1.0}}, {
				'text': "To:\tPlachy, Denver; Cuilla, Martin; Storey, Geoff; Yawapongsiri, Virawan; Kinsey, Lisa; Donohoe, Tom; Ruscitti, Kevin; Lewis, Andrew H.; Williams, Jason (Trading); Frihart, Bryant; Tucker, Patrick; Giron, Darron C.; Pollan, Sylvia S.; Murrell, Russell E; Culotta, Lindsay; O'Malley, Justin; Love, Phillip M.",
				'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Cc:\tLuce, Laura; Shively, Hunter S.', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Subject:\tFW: Classes', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}}, {
				'text': 'Just a reminder.  Classes begin Monday the 15th.  They will be in room 3321 from 3 to 4.  ',
				'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Thanks,', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': ' -----Original Message-----', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'From: \tMahmassani, Souad  ', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Sent:\tTuesday, October 09, 2001 3:05 PM', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{
				'text': "To:\tPlachy, Denver; Cuilla, Martin; Storey, Geoff; Yawapongsiri, Virawan; Kinsey, Lisa; Donohoe, Tom; Ruscitti, Kevin; Lewis, Andrew H.; Williams, Jason (Trading); Frihart, Bryant; Tucker, Patrick; Giron, Darron C.; Pollan, Sylvia S.; Murrell, Russell E; Culotta, Lindsay; O'Malley, Justin; Love, Phillip M.",
				'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Cc:\tLuce, Laura; Hogan, Irena D.; Shively, Hunter S.',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Subject:\tRE: Classes', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Classes have been moved.  We will begin classes on 15th and end on the 26th. ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Thanks', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': ' -----Original Message-----', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'From: \tMahmassani, Souad  ', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Sent:\tWednesday, October 03, 2001 3:47 PM',
			 'predictions': {'Body': 0.0, 'Header': 1.0}}, {
				'text': "To:\tPlachy, Denver; Cuilla, Martin; Storey, Geoff; Yawapongsiri, Virawan; Kinsey, Lisa; Donohoe, Tom; Ruscitti, Kevin; Lewis, Andrew H.; Williams, Jason (Trading); Frihart, Bryant; Tucker, Patrick; Giron, Darron C.; Pollan, Sylvia S.; Murrell, Russell E; Culotta, Lindsay; O'Malley, Justin; Love, Phillip M.",
				'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Cc:\tShively, Hunter S.; Luce, Laura', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Subject:\tClasses', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}}, {
				'text': "I spoke to the professors and we decided that the Midcontinent class will be held Monday's and Wednesday's from 3:00 to 4:00, Ontario class will be held Tuesday's and Thursday's at the same time.  ",
				'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}}, {
				'text': 'Classes will commence Monday 8, 2001, and will continue until Thursday 19, 2001.  Midcontinent test will be held on Monday the 22nd and Ontario test will be held on Tuesday the 23rd.',
				'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Please e-mail any suggestions, conflict, registry.  ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Thanks', 'predictions': {'Body': 1.0, 'Header': 0.0}}]

		expected = {'blocks': [{'from': 'souad.mahmassani@enron.com',
		                        'to': ['denver.plachy@enron.com', 'martin.cuilla@enron.com', 'geoff.storey@enron.com',
		                               'virawan.yawapongsiri@enron.com', 'lisa.kinsey@enron.com',
		                               'tom.donohoe@enron.com', 'kevin.ruscitti@enron.com', 'h..lewis@enron.com',
		                               'trading <.williams@enron.com>', 'bryant.frihart@enron.com',
		                               'patrick.tucker@enron.com', 'c..giron@enron.com', 's..pollan@enron.com',
		                               'e.murrell@enron.com', 'lindsay.culotta@enron.com', "justin.o'malley@enron.com",
		                               'm..love@enron.com', 'cora.pendergrass@enron.com', 'kirk.lenart@enron.com',
		                               'l..schrab@enron.com'], 'cc': ['laura.luce@enron.com', 's..shively@enron.com'],
		                        'sent': '2001-10-15 13:08:09 UTC', 'subject': 'FW: Classes', 'type': 'root',
		                        'raw_header': [], 'text': [
				"One more change to class time.  Today's class only (Midcon) will be held @ 1:45 in room 3270 (same room as our 2:30 daily meeting) .",
				'Thanks']}, {'from': 'Mahmassani, Souad',
		                     'to': ['Plachy, Denver', 'Cuilla, Martin', 'Storey, Geoff', 'Yawapongsiri, Virawan',
		                            'Kinsey, Lisa', 'Donohoe, Tom', 'Ruscitti, Kevin', 'Lewis, Andrew H.',
		                            'Williams, Jason (Trading)', 'Frihart, Bryant', 'Tucker, Patrick',
		                            'Giron, Darron C.', 'Pollan, Sylvia S.', 'Murrell, Russell E', 'Culotta, Lindsay',
		                            "O'Malley, Justin", 'Love, Phillip M.'],
		                     'cc': ['Luce, Laura', 'Shively, Hunter S.'], 'sent': '2001-10-12 13:18:00 UTC',
		                     'subject': 'FW: Classes  Just a reminder.  Classes begin Monday the 15th.  They will be in room 3321 from 3 to 4.   Thanks,',
		                     'type': 'reply',
		                     'raw_header': [' -----Original Message-----', 'From: \tMahmassani, Souad  ',
		                                    'Sent:\tFriday, October 12, 2001 3:18 PM',
		                                    "To:\tPlachy, Denver; Cuilla, Martin; Storey, Geoff; Yawapongsiri, Virawan; Kinsey, Lisa; Donohoe, Tom; Ruscitti, Kevin; Lewis, Andrew H.; Williams, Jason (Trading); Frihart, Bryant; Tucker, Patrick; Giron, Darron C.; Pollan, Sylvia S.; Murrell, Russell E; Culotta, Lindsay; O'Malley, Justin; Love, Phillip M.",
		                                    'Cc:\tLuce, Laura; Shively, Hunter S.', 'Subject:\tFW: Classes', '',
		                                    'Just a reminder.  Classes begin Monday the 15th.  They will be in room 3321 from 3 to 4.  ',
		                                    'Thanks,', ''], 'text': []}, {'from': 'Mahmassani, Souad',
		                                                                  'to': ['Plachy, Denver', 'Cuilla, Martin',
		                                                                         'Storey, Geoff',
		                                                                         'Yawapongsiri, Virawan',
		                                                                         'Kinsey, Lisa', 'Donohoe, Tom',
		                                                                         'Ruscitti, Kevin', 'Lewis, Andrew H.',
		                                                                         'Williams, Jason (Trading)',
		                                                                         'Frihart, Bryant', 'Tucker, Patrick',
		                                                                         'Giron, Darron C.',
		                                                                         'Pollan, Sylvia S.',
		                                                                         'Murrell, Russell E',
		                                                                         'Culotta, Lindsay', "O'Malley, Justin",
		                                                                         'Love, Phillip M.'],
		                                                                  'cc': ['Luce, Laura', 'Hogan, Irena D.',
		                                                                         'Shively, Hunter S.'],
		                                                                  'sent': '2001-10-09 13:05:00 UTC',
		                                                                  'subject': 'RE: Classes  Classes have been moved.  We will begin classes on 15th and end on the 26th.  Thanks',
		                                                                  'type': 'reply',
		                                                                  'raw_header': [' -----Original Message-----',
		                                                                                 'From: \tMahmassani, Souad  ',
		                                                                                 'Sent:\tTuesday, October 09, 2001 3:05 PM',
		                                                                                 "To:\tPlachy, Denver; Cuilla, Martin; Storey, Geoff; Yawapongsiri, Virawan; Kinsey, Lisa; Donohoe, Tom; Ruscitti, Kevin; Lewis, Andrew H.; Williams, Jason (Trading); Frihart, Bryant; Tucker, Patrick; Giron, Darron C.; Pollan, Sylvia S.; Murrell, Russell E; Culotta, Lindsay; O'Malley, Justin; Love, Phillip M.",
		                                                                                 'Cc:\tLuce, Laura; Hogan, Irena D.; Shively, Hunter S.',
		                                                                                 'Subject:\tRE: Classes', '',
		                                                                                 'Classes have been moved.  We will begin classes on 15th and end on the 26th. ',
		                                                                                 'Thanks'], 'text': []},
		                       {'from': 'Mahmassani, Souad',
		                        'to': ['Plachy, Denver', 'Cuilla, Martin', 'Storey, Geoff', 'Yawapongsiri, Virawan',
		                               'Kinsey, Lisa', 'Donohoe, Tom', 'Ruscitti, Kevin', 'Lewis, Andrew H.',
		                               'Williams, Jason (Trading)', 'Frihart, Bryant', 'Tucker, Patrick',
		                               'Giron, Darron C.', 'Pollan, Sylvia S.', 'Murrell, Russell E',
		                               'Culotta, Lindsay', "O'Malley, Justin", 'Love, Phillip M.'],
		                        'cc': ['Shively, Hunter S.', 'Luce, Laura'], 'sent': '2001-10-03 13:47:00 UTC',
		                        'subject': 'Classes', 'type': 'reply',
		                        'raw_header': [' -----Original Message-----', 'From: \tMahmassani, Souad  ',
		                                       'Sent:\tWednesday, October 03, 2001 3:47 PM',
		                                       "To:\tPlachy, Denver; Cuilla, Martin; Storey, Geoff; Yawapongsiri, Virawan; Kinsey, Lisa; Donohoe, Tom; Ruscitti, Kevin; Lewis, Andrew H.; Williams, Jason (Trading); Frihart, Bryant; Tucker, Patrick; Giron, Darron C.; Pollan, Sylvia S.; Murrell, Russell E; Culotta, Lindsay; O'Malley, Justin; Love, Phillip M.",
		                                       'Cc:\tShively, Hunter S.; Luce, Laura', 'Subject:\tClasses'],
		                        'text': ['', '',
		                                 "I spoke to the professors and we decided that the Midcontinent class will be held Monday's and Wednesday's from 3:00 to 4:00, Ontario class will be held Tuesday's and Thursday's at the same time.  ",
		                                 '',
		                                 'Classes will commence Monday 8, 2001, and will continue until Thursday 19, 2001.  Midcontinent test will be held on Monday the 22nd and Ontario test will be held on Tuesday the 23rd.',
		                                 '', '', 'Please e-mail any suggestions, conflict, registry.  ', '',
		                                 'Thanks']}]}

		parsed = self.block_parser.parse_predictions(predicted, email_input)
		print(parsed)

		assert parsed == expected

	def test_bass_e(self):
		# same in '/dasovich-j_all_documents_8956.txt'

		raw_mail = """Message-ID: <6390395.1075854651228.JavaMail.evans@thyme>
Date: Thu, 30 Nov 2000 02:50:00 -0800 (PST)
From: eric.bass@enron.com
To: shanna.husser@enron.com
Subject: Re: aggie/longhorn letter
Mime-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
X-From: Eric Bass
X-To: Shanna Husser
X-cc: 
X-bcc: 
X-Folder: \Eric_Bass_Dec2000\\Notes Folders\Discussion threads
X-Origin: Bass-E
X-FileName: ebass.nsf

waaaaa! waaaaa! you notice that she didn't mention the corps of cadet members 
that tackled and beat on women after texas victory in college station a 
couple of year back


   
	Enron North America Corp.
	
	From:  Shanna Husser @ EES                           11/30/2000 10:36 AM
	

To: Eric Bass/HOU/ECT@ECT
cc:  
Subject: aggie/longhorn letter

Something to get you ALL riled up!!  And you talk about LSU fans being bad- 
"Kill him"!!!
---------------------- Forwarded by Shanna Husser/HOU/EES on 11/30/2000 10:35 
AM ---------------------------


Christina Barthel
11/30/2000 09:43 AM
To: Shanna Husser/HOU/EES@EES, Kim Chick/HOU/EES@EES, Leon 
Branom/Corp/Enron@ENRON, Jason Sharp/ENRON_DEVELOPMENT@ENRON_DEVELOPMENt, 
James Hollman/Corp/Enron@ENRON, Robert B Cothran/Corp/Enron@ENRON, "Meredith" 
<meredith@friersoncpa.com>, "Zogheib, Lisa A" <Lisa_Zogheib@AIMFUNDS.COM>, 
"Kelly Kohrman" <pyrowoman@hotmail.com>, "Ashley" 
<Ashley.Victorick@coastalcorp.com>, "Jaimie" <Jaimie.Parker@coastalcorp.com>, 
"Erin" <elaggie99@hotmail.com>, "Anthony" <urbanaj@texaco.com>, "Jose" 
<jose.a.suarez@us.pwcglobal.com>, "Albert" <albert.r.ferrel@exxon.com>, 
"Oscar " <oscgarcia@notes.primeco.com>, "Misti" <mkuehn@tcresidential.com>
cc:  
Subject: aggie/longhorn letter


---------------------- Forwarded by Christina Barthel/HOU/EES on 11/30/2000 
09:39 AM ---------------------------


Amy.Jon@enron.com on 11/30/2000 09:37:29 AM
To: Christina.Barthel@enron.com, kchick@enron.com, dflinn@enron.com, 
Lynna.Kacal@enron.com, "Leigh Ann Perry" <aotleighann@hotmail.com>, 
aramirez@enron.com, "Michelle" <mtram@nccol.com>, "Sponge" <CZachgo@aol.com>
cc:  
Subject: FW: Are we surprised to hear this?




 "Conduct of Texas Fans at Friday's Football Game Dismays Former Student"

 November 28, 2000

 Dear Battalion and Daily Texan:

Please help me.  As a product of both Texas A&M and the University of
Texas - Austin, I thought I had learned a lot.  But I experienced some new
things at the football game this past Friday that my education had not 
prepared
me for.  No doubt there are Longhorn scholars who can set me straight.  I
watched many joyful Texas fans along with a few Aggies tailgating and
carousing.  Super.  Fall football rivalry.  Spirits were literally in
abundance.  May the better football team win.

Then I saw things that I cannot really comprehend.  I saw a Longhorn fan
with a t-shirt showing a fallen-over Bonfire.  The caption read, "What's
wrong, Aggies? Can't keep it up?"  Can someone explain that to me?  I do
not get it.  I assure you, I get the sexual nuance - I just do not understand
evil.

I saw Longhorn fans mocking and taunting the fans from A&M who were in
Corps of Cadets uniforms.  "Little Hitlers," they were called.  They were 
being
spat at.  Help me to understand this Longhorn slant on rivalry.  I
thought we were all against Hitler - Longhorns and Aggies.

I saw a Longhorn cheerleader - isn't he supposed to represent UT in the
finest possible way?  - run in front of the Aggie Band, turn and face it
square on and salute with the clicked heels, arm-above-head, "Heil
Hitler" sign. 

What don't I know here?  What didn't I learn in history class?  All these
things happened before kickoff.

Aggies, I respect your presentation of a $50,000 endowed scholarship as a
thank-you for UT's respect and support shown last year.  That support
obviously came from the finer Horns.  I admired the fortitude and
restraint exercised by the Corps of Cadets under attack.

Unfortunately, I learned that hundreds and hundreds of Longhorns have
More than one way to show the Hook 'em Horns sign.  They prefer to use their
middle finger.  Class.  Really intelligent and creative.  That will
quickly teach those "littlest" Longhorns how to show spirit.  I just pray they
get an honest chance to choose.

I am learning.  I have attended both schools.  I will choose the higher
ground.

Susan Priest
Classes of '77 and '81
>
>








"""
		filename = "bass-e_discussion_threads_1019.txt"
		email_input = self.construct_email(filename, raw_mail)
		predicted = [
			{'text': "waaaaa! waaaaa! you notice that she didn't mention the corps of cadet members ",
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'that tackled and beat on women after texas victory in college station a ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'couple of year back', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '   ', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '\tEnron North America Corp.', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '\t', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '\tFrom:  Shanna Husser @ EES                           11/30/2000 10:36 AM',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '\t', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'To: Eric Bass/HOU/ECT@ECT', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'cc:  ', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Subject: aggie/longhorn letter', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Something to get you ALL riled up!!  And you talk about LSU fans being bad- ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '"Kill him"!!!', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '---------------------- Forwarded by Shanna Husser/HOU/EES on 11/30/2000 10:35 ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'AM ---------------------------', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Christina Barthel', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '11/30/2000 09:43 AM', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'To: Shanna Husser/HOU/EES@EES, Kim Chick/HOU/EES@EES, Leon ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Branom/Corp/Enron@ENRON, Jason Sharp/ENRON_DEVELOPMENT@ENRON_DEVELOPMENt, ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'James Hollman/Corp/Enron@ENRON, Robert B Cothran/Corp/Enron@ENRON, "Meredith" ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '<meredith@friersoncpa.com>, "Zogheib, Lisa A" <Lisa_Zogheib@AIMFUNDS.COM>, ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '"Kelly Kohrman" <pyrowoman@hotmail.com>, "Ashley" ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '<Ashley.Victorick@coastalcorp.com>, "Jaimie" <Jaimie.Parker@coastalcorp.com>, ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '"Erin" <elaggie99@hotmail.com>, "Anthony" <urbanaj@texaco.com>, "Jose" ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '<jose.a.suarez@us.pwcglobal.com>, "Albert" <albert.r.ferrel@exxon.com>, ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '"Oscar " <oscgarcia@notes.primeco.com>, "Misti" <mkuehn@tcresidential.com>',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'cc:  ', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Subject: aggie/longhorn letter', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '---------------------- Forwarded by Christina Barthel/HOU/EES on 11/30/2000 ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '09:39 AM ---------------------------', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Amy.Jon@enron.com on 11/30/2000 09:37:29 AM',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'To: Christina.Barthel@enron.com, kchick@enron.com, dflinn@enron.com, ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Lynna.Kacal@enron.com, "Leigh Ann Perry" <aotleighann@hotmail.com>, ',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'aramirez@enron.com, "Michelle" <mtram@nccol.com>, "Sponge" <CZachgo@aol.com>',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'cc:  ', 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': 'Subject: FW: Are we surprised to hear this?',
			 'predictions': {'Body': 0.0, 'Header': 1.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': ' "Conduct of Texas Fans at Friday\'s Football Game Dismays Former Student"',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': ' November 28, 2000', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': ' Dear Battalion and Daily Texan:', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Please help me.  As a product of both Texas A&M and the University of',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Texas - Austin, I thought I had learned a lot.  But I experienced some new',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'things at the football game this past Friday that my education had not ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'prepared', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'me for.  No doubt there are Longhorn scholars who can set me straight.  I',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'watched many joyful Texas fans along with a few Aggies tailgating and',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'carousing.  Super.  Fall football rivalry.  Spirits were literally in',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'abundance.  May the better football team win.',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Then I saw things that I cannot really comprehend.  I saw a Longhorn fan',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'with a t-shirt showing a fallen-over Bonfire.  The caption read, "What\'s',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'wrong, Aggies? Can\'t keep it up?"  Can someone explain that to me?  I do',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'not get it.  I assure you, I get the sexual nuance - I just do not understand',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'evil.', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'I saw Longhorn fans mocking and taunting the fans from A&M who were in',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Corps of Cadets uniforms.  "Little Hitlers," they were called.  They were ',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'being', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'spat at.  Help me to understand this Longhorn slant on rivalry.  I',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'thought we were all against Hitler - Longhorns and Aggies.',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': "I saw a Longhorn cheerleader - isn't he supposed to represent UT in the",
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'finest possible way?  - run in front of the Aggie Band, turn and face it',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'square on and salute with the clicked heels, arm-above-head, "Heil',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Hitler" sign. ', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': "What don't I know here?  What didn't I learn in history class?  All these",
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'things happened before kickoff.', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Aggies, I respect your presentation of a $50,000 endowed scholarship as a',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': "thank-you for UT's respect and support shown last year.  That support",
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'obviously came from the finer Horns.  I admired the fortitude and',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'restraint exercised by the Corps of Cadets under attack.',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Unfortunately, I learned that hundreds and hundreds of Longhorns have',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': "More than one way to show the Hook 'em Horns sign.  They prefer to use their",
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'middle finger.  Class.  Really intelligent and creative.  That will',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'quickly teach those "littlest" Longhorns how to show spirit.  I just pray they',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'get an honest chance to choose.', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'I am learning.  I have attended both schools.  I will choose the higher',
			 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'ground.', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': 'Susan Priest', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': "Classes of '77 and '81", 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '>', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '>', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}},
			{'text': '', 'predictions': {'Body': 1.0, 'Header': 0.0}}]
		expected = {'blocks': [{'from': 'eric.bass@enron.com', 'to': ['shanna.husser@enron.com'], 'cc': '', 'sent': '2000-11-30 09:50:00 UTC', 'subject': 'Re: aggie/longhorn letter', 'type': 'root', 'raw_header': [], 'text': ["waaaaa! waaaaa! you notice that she didn't mention the corps of cadet members ", 'that tackled and beat on women after texas victory in college station a ', 'couple of year back', '', '']}, {'from': 'Enron North America Corp.    Shanna Husser @ EES', 'to': ['Eric Bass/HOU/ECT@ECT'], 'cc': '', 'sent': '2000-11-30 09:36:00 UTC', 'subject': 'aggie/longhorn letter  Something to get you ALL riled up!!  And you talk about LSU fans being bad-  "Kill him"!!!', 'type': 'reply', 'raw_header': ['   ', '\tEnron North America Corp.', '\t', '\tFrom:  Shanna Husser @ EES                           11/30/2000 10:36 AM', '\t', '', 'To: Eric Bass/HOU/ECT@ECT', 'cc:  ', 'Subject: aggie/longhorn letter', '', 'Something to get you ALL riled up!!  And you talk about LSU fans being bad- ', '"Kill him"!!!'], 'text': []}, {'from': 'Shanna Husser/HOU/EES', 'to': ['Eric Bass/HOU/ECT@ECT'], 'cc': '', 'sent': '2000-11-30 09:35:00 UTC', 'subject': None, 'type': 'forward', 'raw_header': ['---------------------- Forwarded by Shanna Husser/HOU/EES on 11/30/2000 10:35 ', 'AM ---------------------------'], 'text': []}, {'from': 'Christina Barthel', 'to': ['Shanna Husser/HOU/EES@EES, Kim Chick/HOU/EES@EES, Leon  Branom/Corp/Enron@ENRON, Jason Sharp/ENRON_DEVELOPMENT@ENRON_DEVELOPMENt,  James Hollman/Corp/Enron@ENRON, Robert B Cothran/Corp/Enron@ENRON, "Meredith"  <meredith@friersoncpa.com>, "Zogheib, Lisa A" <Lisa_Zogheib@AIMFUNDS.COM>,  "Kelly Kohrman" <pyrowoman@hotmail.com>, "Ashley"  <Ashley.Victorick@coastalcorp.com>, "Jaimie" <Jaimie.Parker@coastalcorp.com>,  "Erin" <elaggie99@hotmail.com>, "Anthony" <urbanaj@texaco.com>, "Jose"  <jose.a.suarez@us.pwcglobal.com>, "Albert" <albert.r.ferrel@exxon.com>,  "Oscar " <oscgarcia@notes.primeco.com>, "Misti" <mkuehn@tcresidential.com>'], 'cc': '', 'sent': '2000-11-30 08:43:00 UTC', 'subject': 'aggie/longhorn letter', 'type': 'reply', 'raw_header': ['', '', 'Christina Barthel', '11/30/2000 09:43 AM', 'To: Shanna Husser/HOU/EES@EES, Kim Chick/HOU/EES@EES, Leon ', 'Branom/Corp/Enron@ENRON, Jason Sharp/ENRON_DEVELOPMENT@ENRON_DEVELOPMENt, ', 'James Hollman/Corp/Enron@ENRON, Robert B Cothran/Corp/Enron@ENRON, "Meredith" ', '<meredith@friersoncpa.com>, "Zogheib, Lisa A" <Lisa_Zogheib@AIMFUNDS.COM>, ', '"Kelly Kohrman" <pyrowoman@hotmail.com>, "Ashley" ', '<Ashley.Victorick@coastalcorp.com>, "Jaimie" <Jaimie.Parker@coastalcorp.com>, ', '"Erin" <elaggie99@hotmail.com>, "Anthony" <urbanaj@texaco.com>, "Jose" ', '<jose.a.suarez@us.pwcglobal.com>, "Albert" <albert.r.ferrel@exxon.com>, ', '"Oscar " <oscgarcia@notes.primeco.com>, "Misti" <mkuehn@tcresidential.com>', 'cc:  ', 'Subject: aggie/longhorn letter', '', ''], 'text': []}, {'from': 'Christina Barthel/HOU/EES', 'to': ['Shanna Husser/HOU/EES@EES, Kim Chick/HOU/EES@EES, Leon  Branom/Corp/Enron@ENRON, Jason Sharp/ENRON_DEVELOPMENT@ENRON_DEVELOPMENt,  James Hollman/Corp/Enron@ENRON, Robert B Cothran/Corp/Enron@ENRON, "Meredith"  <meredith@friersoncpa.com>, "Zogheib, Lisa A" <Lisa_Zogheib@AIMFUNDS.COM>,  "Kelly Kohrman" <pyrowoman@hotmail.com>, "Ashley"  <Ashley.Victorick@coastalcorp.com>, "Jaimie" <Jaimie.Parker@coastalcorp.com>,  "Erin" <elaggie99@hotmail.com>, "Anthony" <urbanaj@texaco.com>, "Jose"  <jose.a.suarez@us.pwcglobal.com>, "Albert" <albert.r.ferrel@exxon.com>,  "Oscar " <oscgarcia@notes.primeco.com>, "Misti" <mkuehn@tcresidential.com>'], 'cc': '', 'sent': '2000-11-30 08:39:00 UTC', 'subject': None, 'type': 'forward', 'raw_header': ['---------------------- Forwarded by Christina Barthel/HOU/EES on 11/30/2000 ', '09:39 AM ---------------------------'], 'text': []}, {'from': 'Amy.Jon@enron.com on', 'to': ['Christina.Barthel@enron.com, kchick@enron.com, dflinn@enron.com,  Lynna.Kacal@enron.com, "Leigh Ann Perry" <aotleighann@hotmail.com>,  aramirez@enron.com, "Michelle" <mtram@nccol.com>, "Sponge" <CZachgo@aol.com>'], 'cc': '', 'sent': '2000-11-30 08:37:29 UTC', 'subject': 'FW: Are we surprised to hear this?', 'type': 'reply', 'raw_header': ['', '', 'Amy.Jon@enron.com on 11/30/2000 09:37:29 AM', 'To: Christina.Barthel@enron.com, kchick@enron.com, dflinn@enron.com, ', 'Lynna.Kacal@enron.com, "Leigh Ann Perry" <aotleighann@hotmail.com>, ', 'aramirez@enron.com, "Michelle" <mtram@nccol.com>, "Sponge" <CZachgo@aol.com>', 'cc:  ', 'Subject: FW: Are we surprised to hear this?'], 'text': ['', '', '', '', ' "Conduct of Texas Fans at Friday\'s Football Game Dismays Former Student"', '', ' November 28, 2000', '', ' Dear Battalion and Daily Texan:', '', 'Please help me.  As a product of both Texas A&M and the University of', 'Texas - Austin, I thought I had learned a lot.  But I experienced some new', 'things at the football game this past Friday that my education had not ', 'prepared', 'me for.  No doubt there are Longhorn scholars who can set me straight.  I', 'watched many joyful Texas fans along with a few Aggies tailgating and', 'carousing.  Super.  Fall football rivalry.  Spirits were literally in', 'abundance.  May the better football team win.', '', 'Then I saw things that I cannot really comprehend.  I saw a Longhorn fan', 'with a t-shirt showing a fallen-over Bonfire.  The caption read, "What\'s', 'wrong, Aggies? Can\'t keep it up?"  Can someone explain that to me?  I do', 'not get it.  I assure you, I get the sexual nuance - I just do not understand', 'evil.', '', 'I saw Longhorn fans mocking and taunting the fans from A&M who were in', 'Corps of Cadets uniforms.  "Little Hitlers," they were called.  They were ', 'being', 'spat at.  Help me to understand this Longhorn slant on rivalry.  I', 'thought we were all against Hitler - Longhorns and Aggies.', '', "I saw a Longhorn cheerleader - isn't he supposed to represent UT in the", 'finest possible way?  - run in front of the Aggie Band, turn and face it', 'square on and salute with the clicked heels, arm-above-head, "Heil', 'Hitler" sign. ', '', "What don't I know here?  What didn't I learn in history class?  All these", 'things happened before kickoff.', '', 'Aggies, I respect your presentation of a $50,000 endowed scholarship as a', "thank-you for UT's respect and support shown last year.  That support", 'obviously came from the finer Horns.  I admired the fortitude and', 'restraint exercised by the Corps of Cadets under attack.', '', 'Unfortunately, I learned that hundreds and hundreds of Longhorns have', "More than one way to show the Hook 'em Horns sign.  They prefer to use their", 'middle finger.  Class.  Really intelligent and creative.  That will', 'quickly teach those "littlest" Longhorns how to show spirit.  I just pray they', 'get an honest chance to choose.', '', 'I am learning.  I have attended both schools.  I will choose the higher', 'ground.', '', 'Susan Priest', "Classes of '77 and '81", '>', '>', '', '', '', '', '', '', '', '', '']}]}


		parsed = self.block_parser.parse_predictions(predicted, email_input)
		print(parsed)

		assert parsed == expected
