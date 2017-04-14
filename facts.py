#!/usr/bin/env python
# -*- coding: utf8 -*-

import random

# To comunicate de client's desires to the intellect
class Desire(object):
	
	WANT_ROOM = "wantRoom"
	ESTABLISH_ROOM_TYPE = "roomType"
	ESTABLISH_INIT_DATE = "initDate"
	ESTABLISH_END_DATE = "endDate"
	
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
		
	def is_goal(self):
		return self.id == Desire.ESTABLISH_ROOM_TYPE

		
# To extract the intellect response
class Response(object):

	ASK_ROOM_TYPE = "Que tipo de habitacion quieres?"
	ASK_INIT_DATE = "Que dia quieres comenzar tu estancia?"
	ASK_END_DATE = "Hasta que dia quieres estar?"
	ASK_PENSION_TYPE = "Que tipo de pension prefieres? (completa, parcial, solo desayuno)"
	
	CONFIRM_ROOM_TYPE = "Una {room_type} pues"
	CHANGE_ROOM_TYPE = "Tenia apuntada una {room_type}... cambio a una {new_room_type}"
	
	CONFIRM_DATE = "Bien, para el {date}"
	
	UNKNOWN_INPUT = "Perdona, pero no te he entendido"
	
	KNOWN_INFO = "Ya, ya me lo habias comentado"
	
	KEYBOARD_ROOM_TYPES = "keyboardRoomTypes"

	def __init__(self, msg, keyboard = None):
		self._msg = [msg] if type(msg) is str else msg
		self._keyboard = keyboard
		
	@property
	def msg(self):
		return self._msg

	@msg.setter
	def msg(self, value):
		self._msg = value
		
	@property
	def keyboard(self):
		return self._keyboard

	@keyboard.setter
	def keyboard(self, value):
		self._keyboard = value
		

class Reservation(object):

	def __init__(self):
		self._room_type = None
		self._pension_type = None
		self._init_date = None
		self._end_date = None

	@property
	def room_type(self):
		return self._room_type

	@room_type.setter
	def room_type(self, value):
		self._room_type = value
		
	@property
	def pension_type(self):
		return self._pension_type

	@pension_type.setter
	def pension_type(self, value):
		self._pension_type = value
		
	@property
	def init_date(self):
		return self._init_date

	@init_date.setter
	def init_date(self, value):
		self._init_date = value
		
	@property
	def end_date(self):
		return self._end_date

	@end_date.setter
	def end_date(self, value):
		self._end_date = value
	
		