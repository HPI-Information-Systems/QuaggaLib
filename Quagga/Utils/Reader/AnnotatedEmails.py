import os

from Quagga.Utils.Reader.AnnotatedEmail import AnnotatedEmail


class AnnotatedEmails:
	def __init__(self, folder, feature_function, skip_blank=False, perturbation=0.0):
		self.skip_blank = skip_blank  # TODO
		self.feature_function = feature_function
		self.perturbation = perturbation
		self.emails_train = []
		self.emails_test = []
		self.emails_eval = []

		for root, _, files in os.walk(folder):
			for file in files:
				if file.endswith('.ann'):
					fname = os.path.join(root, file)
					if 'eval' in fname:
						self.emails_eval.append(AnnotatedEmail(fname, skip_blank, perturbation=self.perturbation))
					elif 'test' in fname:
						self.emails_test.append(AnnotatedEmail(fname, skip_blank, perturbation=self.perturbation))
					else:
						self.emails_train.append(AnnotatedEmail(fname, skip_blank, perturbation=self.perturbation))
		print('train:', len(self.emails_train))
		print('test', len(self.emails_test))
		print('eval:', len(self.emails_eval))

	@property
	def train_set(self):
		return self.emails_train

	@property
	def test_set(self):
		return self.emails_test

	@property
	def eval_set(self):
		return self.emails_eval

	@property
	def full_set(self):
		return self.train_set + self.test_set + self.eval_set

	@property
	def features(self):
		return ([self.feature_function(m) for m in self.train_set],
		        [self.feature_function(m) for m in self.test_set],
		        [self.feature_function(m) for m in self.eval_set])

	@property
	def features_full(self):
		return [self.feature_function(m) for m in self.full_set]

	@property
	def two_zones_labels(self):
		return ([m.two_zones_labels for m in self.train_set],
		        [m.two_zones_labels for m in self.test_set],
		        [m.two_zones_labels for m in self.eval_set])

	@property
	def two_zones_labels_full(self):
		return [m.two_zones_labels for m in self.full_set]

	@property
	def two_zones_labels_numeric(self):
		return ([m.two_zones_labels_numeric for m in self.train_set],
		        [m.two_zones_labels_numeric for m in self.test_set],
		        [m.two_zones_labels_numeric for m in self.eval_set])

	@property
	def two_zones_labels_numeric_full(self):
		return [m.two_zones_labels_numeric for m in self.full_set]

	@property
	def three_zones_labels(self):
		return ([m.three_zones_labels for m in self.train_set],
		        [m.three_zones_labels for m in self.test_set],
		        [m.three_zones_labels for m in self.eval_set])

	@property
	def three_zones_labels_full(self):
		return [m.three_zones_labels for m in self.full_set]

	@property
	def three_zones_labels_numeric(self):
		return ([m.three_zones_labels_numeric for m in self.train_set],
		        [m.three_zones_labels_numeric for m in self.test_set],
		        [m.three_zones_labels_numeric for m in self.eval_set])

	@property
	def three_zones_labels_numeric_full(self):
		return [m.three_zones_labels_numeric for m in self.full_set]

	@property
	def five_zones_labels(self):
		return ([m.five_zones_labels for m in self.train_set],
		        [m.five_zones_labels for m in self.test_set],
		        [m.five_zones_labels for m in self.eval_set])

	@property
	def five_zones_labels_full(self):
		return [m.five_zones_labels for m in self.full_set]

	@property
	def five_zones_labels_numeric(self):
		return ([m.five_zones_labels_numeric for m in self.train_set],
		        [m.five_zones_labels_numeric for m in self.test_set],
		        [m.five_zones_labels_numeric for m in self.eval_set])

	@property
	def five_zones_labels_numeric_full(self):
		return [m.five_zones_labels_numeric for m in self.full_set]


class AnnotatedEmailsIterator:
	def __init__(self, folder):
		self.folder = folder

	def _iterator(self, split):
		for root, _, files in os.walk(self.folder):
			for file in files:
				if file.endswith('.ann'):
					fname = os.path.join(root, file)
					if split in fname:
						yield AnnotatedEmail(fname, False)

	@property
	def test(self):
		return self._iterator('test')

	@property
	def eval(self):
		return self._iterator('eval')

	@property
	def train(self):
		return self._iterator('train')
