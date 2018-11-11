import re


class BlockCleaner:
	def __init__(self):
		pass

	def clean(self, block):
		block['from'] = self.cleanup_string(block['raw_from'])
		block['to'] = self.cleanup_string(block['raw_to'])
		block['cc'] = self.cleanup_string(block['raw_cc'])
		block['sent'] = self.cleanup_string(block['raw_sent'])
		block['subject'] = self.cleanup_string(block['raw_subject'])

	def cleanup_string(self, string):
		if string is None:
			return None
		string = self.cleanup_escapes(string)
		string = self.cleanup_whitespace(string)
		string = self.cleanup_dashes(string)
		return string

	def cleanup_escapes(self, string):
		string = string.replace("\n", "")
		string = string.replace("\t", "")
		string = string.replace("\r", "")
		return string

	def cleanup_whitespace(self, string):
		string = string.lstrip()
		string = string.rstrip()
		return string

	def cleanup_dashes(self, string):
		dash_regex = r"(^(-+)|(-+)$)"
		string = re.sub(dash_regex, "", string)
		return string