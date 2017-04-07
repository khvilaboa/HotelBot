#!/usr/bin/env python
# -*- coding: utf8 -*-

#from resources import Database, Weather

import langdetect, langid, textblob
import nltk, pdb, utils.spellchecker as sc, string
from intellect.Intellect import Intellect, Callable
from facts import *

# To encapsulate the client's message and doing preparse tasks
class UserInput:
	stopwords = nltk.corpus.stopwords.words('spanish')
	stemmer = nltk.stem.SnowballStemmer('spanish')
	non_words = list(string.punctuation) + ['¿', '¡']
	
	def __init__(self, text):
		self.text = text
		self.text_san = self.sanitize(text)
		self.text_sc = ' '.join([sc.correction(w) for w in self.text_san.split()])
		self.lang = self.language(self.text_sc)
		self.parsed = self.tokenize(self.text_sc)
		
	def __str__(self):
		return self.text
		
	def sanitize(self, text):
		rep = {u'á': 'a', u'é': 'e', u'í': 'i', u'ó': 'o', u'ú': 'u', u'Á': 'A', u'É': 'E', u'Í': 'I', u'Ó': 'O', u'Ú': 'U', u'ü': 'u', u'Ü': 'u', u'ñ': 'n', u'Ñ': 'n'}   # temporal
		for k, v in rep.iteritems(): text = text.replace(k, v)
		return ''.join(filter(lambda c: c in string.printable, text))
	
	def tokenize(self, text):
		# Remove punctuation symbols
		text = ''.join([c for c in text if c not in UserInput.non_words])

		# Separate words
		tokens =  nltk.word_tokenize(text)
		
		try:
			stems = map(lambda token: UserInput.stemmer.stem(token), tokens)
		except Exception as e:
			print(e)
			print(text)
			stems = ['']
		return stems
		
	def language(self, text):
		try:
			# Try to detect the language with three different packages
			lang1 = langid.classify(text)[0]
			lang2 = langdetect.detect(text)
			lang3 = textblob.TextBlob(text).detect_language()
			
			print(lang1, lang2, lang3)
			
			if lang1 == lang2 == lang3:  # If all oh them throws the same result, return it
				return lang1
			elif lang1 == 'es' or lang2 == 'es' or lang3 == 'es':  # If at least one detect spanish...
				return 'es'
			else: 
				return lang1 
		except Exception as e:
			print(e)
			return None  # Insuficient information


# Custom intellect to improve the management of facts and policies
class MyIntellect(Intellect):
	@Callable
	def test(self):
		print(">>>>>>>>>>>>>>  called MyIntellect's bar method as it was decorated as callable.")

	@Callable  # It can be called form the rules file
	def clear_facts(self):
		self._knowledge = []
	
	# Returns the first response of the knowledge
	def extract_response(self):
		for fact in self.knowledge:
			if type(fact) is Response:
				return fact
		return None

class HotelAgent:

	def __init__(self):
		self.intellect = MyIntellect()
		self.intellect.learn(Intellect.local_file_uri("./policies/hotel.policy"))

	def evaluate(self, input):
		resp = "Language: %s" % input.lang
		resp += "\nSanitized: %s" % input.text_san
		resp += "\nCorrected: %s" % input.text_sc
		resp += "\nTokenized: %s" % input.parsed
		
		self.intellect.learn(Desire(Desire.ESTABLISH_ROOM_TYPE))  # Example
		self.intellect.reason()
		r = self.intellect.extract_response()
		
		if r is not None:
			resp += "\nIntellect test: %s" % r.msg
		
		return 1, resp # trust, response 

		
class InsultsAgent:
	def evaluate(self, input):
		return 0, input.text.upper() # trust, response