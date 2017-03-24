#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#from resources import Database, Weather

import nltk, string

class AgentUtils:
	stopwords = nltk.corpus.stopwords.words('spanish')
	stemmer = nltk.stem.SnowballStemmer('spanish')
	non_words = list(string.punctuation) + ['¿', '¡']
	
	@staticmethod
	def tokenize(text):
		# Remove punctuation symbols
		text = ''.join([c for c in text if c not in AgentUtils.non_words])

		# Separate words
		tokens =  nltk.word_tokenize(text)

		
		try:
			stems = map(lambda token: AgentUtils.stemmer.stem(token), tokens)
		except Exception as e:
			print(e)
			print(text)
			stems = ['']
		return stems
		

class HotelAgent:
	def evaluate(self, text):
		tokenized = str(AgentUtils.tokenize(text))
		return 1, tokenized # trust, response 

		
class InsultsAgent:
	def evaluate(self, text):
		return 0, text.lower() # trust, response