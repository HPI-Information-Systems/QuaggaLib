class Block:

	def __init__(self, sender=None, to=None, cc=None, sent=None, subject=None, type=None, raw_header=None,
	             text=None):
		raw_header = [] if raw_header is None else raw_header
		text = [] if text is None else text
		type = 'root' if type not in ['root', 'forward', 'reply'] else type

		self.sender = sender
		self.raw_sender = sender
		self.raw_xsender = sender

		self.to = to
		self.raw_to = to
		self.raw_xto = to

		self.cc = cc
		self.raw_cc = cc
		self.raw_xcc = cc

		self.sent = sent
		self.raw_sent = sent

		self.subject = subject
		self.raw_subject = subject

		self.type = type

		self.raw_header = raw_header

		self.text = text

	def set_raw_from(self, sender):
		self.raw_sender = sender
		self.raw_xsender = sender
		self.sender = sender

	def set_raw_xfrom(self, sender):
		self.raw_xsender = sender

	def set_raw_to(self, to):
		self.raw_to = to
		self.raw_xto = to
		self.to = to

	def set_raw_cc(self, cc):
		self.raw_cc = cc
		self.raw_xcc = cc
		self.cc = cc

	def set_raw_xto(self, xto):
		self.raw_xto = xto

	def set_raw_xcc(self, xcc):
		self.raw_xcc = xcc

	def set_raw_sent(self, sent):
		self.raw_sent = sent
		self.sent = sent

	def set_raw_subject(self, subject):
		self.raw_subject = subject
		self.subject = subject

	def serialize(self):
		return {
			'from': self.sender,
			'to': self.to,
			'cc': self.cc,
			'sent': self.sent,
			'subject': self.subject,
			'type': self.type,  # root, forward, reply
			'raw_header': self.raw_header,
			'text': self.text
		}

	def serialize_with_raw(self):
		return {
			'from': self.sender,
			'raw_from': self.raw_sender,
			'raw_xfrom': self.raw_xsender,
			'to': self.to,
			'raw_to': self.raw_to,
			'raw_xto': self.raw_xto,
			'cc': self.cc,
			'raw_cc': self.raw_cc,
			'raw_xcc': self.raw_xcc,
			'sent': self.sent,
			'raw_sent': self.raw_sent,
			'subject': self.subject,
			'raw_subject': self.raw_subject,
			'type': self.type,  # root, forward, reply
			'raw_header': self.raw_header,
			'text': self.text
		}
