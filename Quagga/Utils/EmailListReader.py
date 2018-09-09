from Quagga.Utils.Email import EmailMessage, EmailBody
from email import parser as ep

class ListReaderIterator:
	def __init__(self, text, output_func):
		self.text = text
		self.iter = iter(text)
		self.output_func = output_func
		self.index = -1
	def __next__(self):
		self.index += 1
		return self.output_func(next(self.iter), self.index)

class ListReaderExtractedBodies:
	def __init__(self, body_texts):
		self.body_texts = body_texts

	def __iter__(self):
		return ListReaderIterator(self.body_texts, lambda email, _: EmailBody(email))


class ListReaderRawEmailTexts():
	def __init__(self, raw_texts):
		self.mail_parser = ep.Parser()
		self.raw_texts = raw_texts

	def __iter__(self):
		# in case no name is available just count
		return ListReaderIterator(self.raw_texts, lambda email, i: EmailMessage('', str(i), self.mail_parser.parsestr(email)))