from email import parser as ep
import os
import json

from Quagga.Utils.Reader.Email import EmailMessage, Email


class DirectoryIterator:
	def __init__(self, maildir, limit=None, skip=0, file_func=lambda _: True, reader_func=lambda path, filename, file: (path, filename, file),
	             transform_func=None):
		self.limit = limit
		self.skip = skip
		self.file_func = file_func
		self.reader_func = reader_func

		self.maildir = maildir

		self.run = 0

		self.os_walker = os.walk(self.maildir)
		self.current_dirs = []
		self.current_files = iter([])
		self.current_root_dir = ''

		if transform_func is None:
			self.transform_func = lambda name, root_dir, root_dir_stripped: root_dir + "/" + name
		else:
			self.transform_func = transform_func

		for i in range(self.skip):
			self.run += 1
			self._next_file(skipmode=True)

	@property
	def current_root_dir_stripped(self):
		return self.current_root_dir[len(self.maildir):]

	def _next_file(self, skipmode=False):
		try:
			filename = next(self.current_files)

			if not self.file_func(filename):
				return self._next_file()


			# save some effort when result is dumped anyway during skip-ahead
			if not skipmode:
				processed_filename = self.transform_func(filename, self.current_root_dir, self.current_root_dir_stripped)
				with open(processed_filename, "r", errors='ignore') as f:
					self.run += 1
					file = f.read() # todo read on client side so you can avoid it if not needed

					return self.current_root_dir_stripped, filename, file
		except StopIteration:
			self._next_dir()
			return self._next_file()


	def _next_dir(self):
		self.current_root_dir, self.current_dirs, files = next(self.os_walker)
		if len(files) > 0:
			self.current_files = iter(files)
		else:
			self._next_dir()

	def __next__(self):
		if self.limit is not None and (self.limit + self.skip) <= self.run:
			raise StopIteration()

		return self.reader_func(*self._next_file())



class DirectoryReader:
	def __init__(self, maildir, limit=None, skip=0, file_func=lambda filename: True, output_func=lambda path, filename, file: (path, filename, file)):
		self.maildir = maildir
		self.limit = limit
		self.skip = skip
		self.file_func = file_func
		self._file_func = lambda filename: '.DS_Store' not in filename and self.file_func(filename)
		self.email_func = output_func

	def __iter__(self):
		return DirectoryIterator(self.maildir, self.limit, self.skip, self._file_func, self.email_func)


"""
reads previously by quagga created results
assumes that they are non-hierachic in the tempdir folder
traverses the original email files and converts their names to the ones we assume in tempdir
so don't alter the names
"""
class TempQuaggaReader(DirectoryReader):
	def __init__(self, stage, maildir, tempdir, limit=None, skip=0, output_func=lambda x:x):
		super().__init__(maildir, limit, skip)
		self.tempdir = tempdir
		self.stage = stage
		self.file_func = lambda filename: True
		self.email_func = lambda path, filename, file: output_func(json.loads(file)[self.stage])
		self.filename_transform = lambda filename, root_dir, root_dir_stripped: self.tempdir + "/" + Email.filename_underscores(root_dir_stripped, filename) + "." + stage + ".json"

	def __iter__(self):
		return DirectoryIterator(self.maildir, self.limit, self.skip, self._file_func, self.email_func, self.filename_transform)


class EmailDirectoryReader(DirectoryReader):
	def __init__(self, maildir, limit=None, skip=0, file_func=lambda x: True):
		super().__init__(maildir, limit, skip)
		self.email_parser = ep.Parser()
		self.file_func = lambda filename: '.quagga.' not in filename and file_func(filename)
		self.email_func = lambda path, filename, file: EmailMessage(path, filename, self.email_parser.parsestr(file))
		self.length = sum([len(files) for r, d, files in os.walk(self.maildir)])





