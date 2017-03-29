#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#from resources import Database, Weather

import langdetect, langid, nltk, string, textblob

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
		
	@staticmethod
	def language(text):
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
	def evaluate(self, text):
		resp = "Language: %s" % AgentUtils.language(text)
		resp += "\nTokenized: %s" % AgentUtils.tokenize(text)
		return 1, resp # trust, response 

		
class InsultsAgent:
	def evaluate(self, text):
		return 0, text.lower() # trust, response