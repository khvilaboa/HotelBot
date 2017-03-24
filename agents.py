#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#from resources import Database, Weather

class HotelAgent:
	def evaluate(self, text):
		return 1, text.upper() # trust, response 

		
class InsultsAgent:
	def evaluate(self, text):
		return 0, text.lower() # trust, response