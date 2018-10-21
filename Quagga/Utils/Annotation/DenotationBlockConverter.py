from Quagga.Utils.BlockParser.Block import Block


class DenotationBlockConverter:

	@staticmethod
	def convert(denotations):
		denotations.sort(key=lambda x: x['end'])
		denotation_blocks = []
		current_denotation_details = []
		for denotation in denotations:
			if denotation['type'] not in ['Header', 'Body']:
				current_denotation_details.append(denotation)
			else:
				denotation_blocks.append({'block': denotation,
				                          'details': current_denotation_details})
				current_denotation_details = []

		if len(denotation_blocks) <= 0:
			print("did not find any denotations")
			return

		blocks = []
		current_block = Block(type='root')

		for i, denotation in enumerate(denotation_blocks):

			if denotation['block']['type'] == 'Header':
				if i != 0:
					# append block and parse new header
					blocks.append(current_block)
					current_block = Block(type='reply')  # forward header = single reply block
				cc = []
				sender = ''
				to = []
				sent = ''
				subject = ''
				for detail_denotation in denotation['details']:
					if detail_denotation['type'] == 'Header/Person/Cc': # todo maybe include bcc here
						cc.append(detail_denotation['text'])
					if detail_denotation['type'] == 'Header/Person/From':
						sender = detail_denotation['text']
					if detail_denotation['type'] == 'Header/Person/To':
						to.append(detail_denotation['text'])
					if detail_denotation['type'] == 'Header/Sent/Date':
						sent = sent + ' ' + detail_denotation['text']
					if detail_denotation['type'] == 'Header/Sent/Time':
						sent = sent + ' ' + detail_denotation['text']
					if detail_denotation['type'] == 'Header/Subject':
						subject = subject + detail_denotation['text']

				current_block.set_raw_cc(cc)
				current_block.set_raw_sender(sender)
				current_block.set_raw_to(to)
				current_block.set_raw_sent(sent)
				current_block.raw_header = denotation['block']['text']

			else:
				# append info to current block
				current_block.text = denotation['block']['text'].split('\n')

		blocks.append(current_block)

		blocks = list(map(lambda x: x.serialize_with_raw(), blocks))

		blocks = {'blocks': blocks}

		return blocks
