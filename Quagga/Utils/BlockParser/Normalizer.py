# -*- coding: utf-8 -*-

import re
import dateparser
import dateutil.parser
from datetime import timezone, datetime
import pytz


class Normalizer:
	EMAIL_REGEX = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

	"""
	[{'from': 'brenda.flores-cuellar@enron.com',
		                        'to': 'edward.gottlob@enron.com, lauri.allen@enron.com, daren.farmer@enron.com, \n\tdan.junek@enron.com, jared.kaiser@enron.com, judy.townsend@enron.com',
		                        'cc': '', 'sent': '2000-02-24 09:44:00', 'subject': 'RE: Options Training Classes',
		                        'type': 'root', 'raw_header': [], 'text': ['FYI', '',
		                                                                   'I am currently out of books.  I should be getting some more in today.  As ',
		                                                                   'soon as they come in, I will make sure you get a copy.',
		                                                                   '', '-Brenda', '']},
		                       {'from': 'Brenda Flores-Cuellar/HOU/ECT',
		                        'to': 'edward.gottlob@enron.com, lauri.allen@enron.com, daren.farmer@enron.com, \n\tdan.junek@enron.com, jared.kaiser@enron.com, judy.townsend@enron.com',
		                        'cc': None, 'sent': '02/23/2000 04:26 PM ', 'subject': None, 'type': 'forward',
		                        'raw_header': ['---------------------- Forwarded by Brenda Flores-Cuellar/HOU/ECT on ',
		                                       '02/23/2000 04:26 PM ---------------------------'], 'text': []},
		                       {'from': None,
		                        'to': '  Phillip K Allen/HOU/ECT@ECT, Eric Bass/HOU/ECT@ECT, Sandra F  Brawner/HOU/ECT@ECT, Mike Grigsby/HOU/ECT@ECT, Keith Holst/HOU/ECT@ect, Brian  Hoskins/HOU/ECT@ECT, Dick Jenkins/HOU/ECT@ECT, Peter F Keavey/HOU/ECT@ECT,  Matthew Lenhart/HOU/ECT@ECT, Andrew H Lewis/HOU/ECT@ECT, Thomas A  Martin/HOU/ECT@ECT, Greg McClendon/HOU/ECT@ECT, Brad McKay/HOU/ECT@ECT, Carey  M Metz/HOU/ECT@ECT, Sarah Mulholland/HOU/ECT@ECT, Scott Neal/HOU/ECT@ECT, Eva  Pao/HOU/ECT@ECT, Jim Schwieger/HOU/ECT@ECT, Elizabeth Shim/Corp/Enron@Enron,  Hunter S Shively/HOU/ECT@ECT, Geoff Storey/HOU/ECT@ECT, Fletcher J  Sturm/HOU/ECT@ECT, Patricia Tlapek/HOU/ECT@ECT',
		                        'cc': '  Shirley Crenshaw/HOU/ECT@ECT ', 'sent': None,
		                        'subject': '  RE: Options Training Classes', 'type': 'reply',
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
		                                 '-Brenda', 'x31914', '', '', '']}]"""

	# @profile
	@staticmethod
	def normalize(block):
		block['from'] = Normalizer.normalize_name(block['from'], block['raw_xfrom'])
		block['to'] = Normalizer.normalize_names(block['to'], block['raw_xto'])
		block['cc'] = Normalizer.normalize_names(block['cc'], block['raw_xcc'])
		block['sent'] = Normalizer.normalize_sent(block['sent'])

	@staticmethod
	def construct_name(name, email, raw):
		return {
			'name': name,
			'email': email,
			'raw_name': raw
		}

	# @profile
	@staticmethod
	def normalize_sent(sent):
		""" this is so nested because i found it as performance critical, dateparser takes somehow 0.5 sec per date.."""

		if sent is None or sent == '':
			return sent

		sent = re.sub(r".*(-+)$", "", sent)  # often there is a - at the end

		try:
			# without timezone
			time = datetime.strptime(sent, '%Y-%m-%d %H:%M:%S')

		except ValueError:

			try:
				# other commonly used format
				# 'Friday, October 12, 2001 3:18 PM'
				time = datetime.strptime(sent, '%A, %B %d, %Y %I:%M %p')

			except ValueError:

				try:
					time = dateutil.parser.parse(sent, fuzzy=True)
					if time == '':
						time = Normalizer._parse_time_dateparser(sent)
				except ValueError:
					time = Normalizer._parse_time_dateparser(sent)

		if time is not None and time is not '':
			if time.tzinfo is None:
				time = pytz.utc.localize(time, is_dst=None)
			string = time.astimezone(pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S %Z')
			if string.endswith('+00:00'):
				string = string[:-6]
			return string
		else:
			return ''

	@staticmethod
	def _parse_time_dateparser(time):
		try:
			time = dateparser.parse(time, languages=['en'])
		except RecursionError as r:
			# something went wrong in the blockparser and or time is too long (multiple aggregated)
			print('An exception occurred: {}'.format(r))
			time = ''
		return time

	@staticmethod
	def normalize_names(string, xstring):
		# Buy, Rick

		# Rick Buy, Andrew Miller

		# Shanna Husser/HOU/EES@EES, Kim Chick/HOU/EES@EES, Leon
		# Branom/Corp/Enron@ENRON, Jason Sharp/ENRON_DEVELOPMENT@ENRON_DEVELOPMENt,
		# James Hollman/Corp/Enron@ENRON, Robert B Cothran/Corp/Enron@ENRON, "Meredith"
		# <meredith@friersoncpa.com>, "Zogheib, Lisa A" <Lisa_Zogheib@AIMFUNDS.COM>,

		if string is None:
			# if its none this is intended
			return string
		if string is '':
			return []

		names = []
		xnames = []

		not_empty_regex = """[^ ]*"""

		def not_empty(name):
			if name is None:
				return False
			if not re.match(not_empty_regex, name) or name == '':
				return False
			return True

		if not ';' in string and not ',' in string:
			names = [string]
		elif ';' in string:
			names = string.split(';')
		elif ',' in string:
			commas_outside_of_quotations_regex = """(.*?),(?=(?:[^"]*(")[^(")]*")*[^"]*$)"""
			names = re.split(commas_outside_of_quotations_regex, string + ',')

			names = list(filter(not_empty, names))
			for name in names:
				whitespace_between_words_regex = """.*\S+ +\S+.*"""
				if re.match(whitespace_between_words_regex, name) is None:
					if re.search(Normalizer.EMAIL_REGEX, name) is None:
						# single word and no email@domain
						# don't split since there are no semicolons
						return [Normalizer.normalize_name(string, xstring)]

		if not ';' in xstring and not ',' in xstring:
			xnames = [xstring]
		elif ';' in xstring:
			xnames = xstring.split(';')
		elif ',' in xstring:
			commas_outside_of_quotations_regex = """(.*?),(?=(?:[^"]*(")[^(")]*")*[^"]*$)"""
			xnames = re.split(commas_outside_of_quotations_regex, xstring + ',')

			xnames = list(filter(not_empty, xnames))

		names = list(filter(not_empty, names))
		xnames = list(filter(not_empty, xnames))

		res = []
		for name, xname in zip(names, xnames):
			res.append(Normalizer.normalize_name(name, xname))

		return res

	@staticmethod
	def normalize_name(name, xname):
		if name is None or name == '':
			return Normalizer.construct_name('', '', name)

		name = Normalizer._cleanup_whitespace(name)
		xname = Normalizer._cleanup_whitespace(xname)

		if xname == '' or xname == name:
			xname = ''

		name = Normalizer._extract_name_fields(name, xname)

		return name

	@staticmethod
	def _extract_name_fields(name, xname=''):
		# this could be vastly improved, maybe some ner?
		# for now we assume that names don't contain slashes and everything after the slash doesnt matter

		email_regex = r"([a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
		addresses = re.findall(email_regex, name)

		# todo: test, there are cases where this fails (obviously)

		person_name = ''
		if xname != '':
			person_name = Normalizer._extract_person_name(xname)
		else:
			if len(addresses) > 0:
				name_before_mail = re.sub(r"(([a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+).*)", "", name,
				                          re.IGNORECASE)
				person_name = Normalizer._extract_person_name(name_before_mail)

			if person_name == '':
				person_name = Normalizer._extract_person_name(name)

		person_email = addresses[0] if len(addresses) > 0 else ""
		person_email = person_email.lstrip('\'')
		person_email = person_email.rstrip('\'')

		person_email = Normalizer._cleanup_whitespace(person_email)
		person_name = Normalizer._cleanup_whitespace(person_name)

		return Normalizer.construct_name(person_name, person_email, name)

	@staticmethod
	def _extract_person_name(name):
		person_name = re.sub(r"([a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", "", name, flags=re.IGNORECASE)
		person_name = re.sub("""(<.*>)""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""(\[.*\])""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""(/.*)""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""(@.*)""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""(mailto:?)""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""((Please)? respond to:?)""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""( on:?)""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""(\(?e-mail\)?)""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""(\(?email\)?)""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""(.*-{1,} *forwarded (by)?:?)""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""(.*sent by:?)""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""(-{3,})""", '', person_name, flags=re.IGNORECASE)
		person_name = re.sub("""(http:/?.*)""", '', person_name, flags=re.IGNORECASE)

		person_name = Normalizer._cleanup_whitespace(person_name)

		for character in ["<", ">", "[", "]", "<", ">", "/", "\\", "\"", "?"]:
			person_name = person_name.replace(character, "")

		person_name = person_name.lstrip('\'')
		person_name = person_name.rstrip('\'')

		if len(person_name) > 40:
			return ''

		return person_name

	@staticmethod
	def _cleanup_whitespace(string):
		string = string.lstrip()
		string = string.rstrip()
		return string
