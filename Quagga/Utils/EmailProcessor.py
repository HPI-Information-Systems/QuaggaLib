


class EmailIterator:
	def __init__(self, quagga, emails, working_directory, emails_input, email_func, stage):
		self.quagga = quagga
		self.emails_iter = iter(emails)
		self.working_directory = working_directory
		self.emails_input_iter = iter(emails_input)
		self.email_func = email_func
		self.stage = stage

	def __next__(self):
		try:
			email_input = next(self.emails_iter)
			email_stage_input = next(self.emails_input_iter)
		except StopIteration:
			raise StopIteration
		email_stage_output = self.email_func(email_stage_input, email_input)
		return email_stage_output


class EmailProcessor:
	def __init__(self, quagga, emails, working_directory, emails_input, email_func, stage):
		self.quagga = quagga
		self.emails = emails
		self.working_directory = working_directory
		self.emails_input = emails_input
		self.email_func = email_func
		self.stage = stage

	def __iter__(self):
		return EmailIterator(self.quagga, self.emails, self.working_directory, self.emails_input, self.email_func,
		                     self.stage)
