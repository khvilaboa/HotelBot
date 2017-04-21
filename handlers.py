
from pymongo import MongoClient
from facts import Reservation
from datetime import datetime, timedelta
import pdb

class DBHandler:

	ROOM_INDIVIDUAL = "individual"
	ROOM_DOUBLE = "double"
	ROOM_SUITE = "suite"
	
	FIELD_CLIENT_USER = "username"
	FIELD_CLIENT_RESERV = "reservations"

	def __init__(self):
		self.mongo_client = MongoClient()
		self.hotel_db = self.mongo_client.hotelbot
		
		# Collections
		self.hotels = self.hotel_db.hotels
		self.rooms = self.hotel_db.rooms
		self.clients = self.hotel_db.clients
		
	def add_reservation(self, username, reserv):
		reserv_doc = dict()
		reserv_doc["room_type"] = reserv.room_type
		reserv_doc["init_date"] = reserv.init_date
		reserv_doc["end_date"] = reserv.end_date
		reserv_doc["pension_type"] = reserv.pension_type
		
		now = datetime.now()
		reserv_doc["reservation_date"] = now.strftime("%d/%m/%Y")
		reserv_doc["reservation_hour"] = now.strftime("%H:%M:%S")

		room = self.free_room_from_dates(reserv.init_date, reserv.end_date)
		reserv_doc["room"] = room["number"]
		reserv_doc["floor"] = room["floor"]
		
		days = self.dates_in_interval(reserv.init_date, reserv.end_date)
		self.rooms.update({"number": room["number"], "floor": room["floor"]}, \
		                  {"$push": {"reservations": {"$each": days}}})
		
		self.clients.update({DBHandler.FIELD_CLIENT_USER: username}, {"$push": {DBHandler.FIELD_CLIENT_RESERV: reserv_doc}})
		
	def free_room_from_dates(self, init_date, end_date = None, room_type = None):
		days = self.dates_in_interval(init_date, end_date) if end_date else [init_date]
		
		if room_type is None:
			results = self.rooms.find({"reservations": {"$nin": days}})
		else:
			results = self.rooms.find({"reservations": {"$nin": days}, "type": room_type})
		
		return results.next() if results.count() != 0 else None
		
	def dates_in_interval(self, init_date, end_date):
		idt = datetime.strptime(init_date, "%d/%m/%Y")
		edt = datetime.strptime(end_date, "%d/%m/%Y")
		delta = timedelta(days = 1)
		days = []
		
		while idt != edt:
			days.append(idt.strftime("%d/%m/%Y"))
			idt += delta
			
		#days.append(idt.strftime("%d/%m/%Y"))
		return days
		
	
	def check_client(self, username):
		if self.clients.find_one({DBHandler.FIELD_CLIENT_USER: username}) is None:
			self.clients.insert_one({DBHandler.FIELD_CLIENT_USER: username})
		
	# Returns the price of a specific type of room
	def price(self, room_type):
		return self.hotels.find_one()["room_prices"][room_type]