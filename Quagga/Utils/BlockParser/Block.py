

class Block:

	def __init__(self, sender=None, to=None, cc=None, sent=None, subject=None, type=None, raw_header=None,
		text=None):

		raw_header = [] if raw_header is None else raw_header
		text = [] if text is None else text
		type = 'root' if type not in ['root', 'forward', 'reply'] else type

		self.sender = sender
		self.raw_sender = sender

		self.to = to
		self.raw_to = to

		self.cc = cc
		self.raw_cc = cc

		self.sent = sent
		self.raw_sent = sent

		self.subject = subject
		self.raw_subject = subject

		self.type = type

		self.raw_header = raw_header

		self.text = text

	def set_raw_sender(self, sender):
		self.raw_sender = sender
		self.sender = sender

	def set_raw_to(self, to):
		self.raw_to = to
		self.to = to

	def set_raw_cc(self, cc):
		self.raw_cc = cc
		self.cc = cc

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
			'to': self.to,
			'raw_to': self.raw_to,
			'cc': self.cc,
			'raw_cc': self.raw_cc,
			'sent': self.sent,
			'raw_sent': self.raw_sent,
			'subject': self.subject,
			'raw_subject': self.raw_subject,
			'type': self.type,  # root, forward, reply
			'raw_header': self.raw_header,
			'text': self.text
		}