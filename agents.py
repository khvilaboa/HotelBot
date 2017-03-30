#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#from resources import Database, Weather

import langdetect, langid, nltk, string, textblob, unicodedata

class UserInput:
	stopwords = nltk.corpus.stopwords.words('spanish')
	stemmer = nltk.stem.SnowballStemmer('spanish')
	non_words = list(string.punctuation) + ['¿', '¡']
	
	def __init__(self, text):
		self.text = text
		self.lang = self.language(text)
		self.parsed = self.tokenize(text_san)
		
	def __str__(self):
		return self.text
	
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

class HotelAgent:
	def evaluate(self, input):
		resp = "Language: %s" % input.lang
		resp += "\nTokenized: %s" % input.parsed
		return 1, resp # trust, response 

		
class InsultsAgent:
	def evaluate(self, input):
		return 0, str(input).upper() # trust, response