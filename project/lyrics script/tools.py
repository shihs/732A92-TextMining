import unicodedata
import re


def transfer_text(text):
	'''Transfer the text format. Delete all text except alphabet and numbers, 
		and transfer all latin alphabet to english alphabet. Becasue this is how the link needed.
	
	args:
		text: string, the text that wants to be transfer
	retrun:
		link_text: string, the transfered format
	'''
	# only keep alphabet and numbers
	combine = re.sub('[^A-Za-z0-9]', '', text).lower()
	# transfer latin alphabet to english alphabet
	link_text = ''.join(char for char in unicodedata.normalize('NFKD', combine) if unicodedata.category(char) != 'Mn')
	return link_text