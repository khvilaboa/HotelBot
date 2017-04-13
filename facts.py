#!/usr/bin/env python
# -*- coding: utf8 -*-

import random

# To comunicate de client's desires to the intellect
class Desire(object):
	
	WANT_ROOM = "wantRoom"
	ESTABLISH_ROOM_TYPE = "roomType"
	
	def __init__(self, id = None):
		self._id = id
		self._data = {}
		
	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, value):
		self._id = value
		
	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, value):
		self._data = value

		
# To extract the intellect response
class Response(object):

	def __init__(self, msg):
		if type(msg) is list:
			msg = random.choice(msg)
		self._msg = msg
		
	@property
	def msg(self):
		return self._msg

	@msg.setter
	def msg(self, value):
		self._msg = value
		

"""class Reservation(object):

	def __init__(self, roomType = None, pensionType = None):
		self._roomType = roomType
		self._pensionType = pensionType
		self.test = [1, 2, 3, 4, 5]

	@property
	def roomType(self):
		return self._roomType

	@roomType.setter
	def roomType(self, value):
		self._roomType = value
		
	@property
	def pensionType(self):
		return self._pensionType

	@pensionType.setter
	def pensionType(self, value):
		self._pensionType = value"""
		

		
	
		