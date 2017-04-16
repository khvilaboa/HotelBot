
from pymongo import MongoClient
from facts import Reservation
import pdb

class DBHandler:

	ROOM_INDIVIDUAL = "individual"
	ROOM_DOUBLE = "double"
	ROOM_SUITE = "suite"
	
	FIELD_CLIENT_USER = "username"
	FIELD_CLIENT_RESERV = "reservations"

	def __init__(self):
		self.mongo_client = MongoClient()
		self.hotel_db = self.mongo_client.hotel
		
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
		
		self.clients.update({DBHandler.FIELD_CLIENT_USER: username}, {"$push": {DBHandler.FIELD_CLIENT_RESERV: reserv_doc}})
		
	def check_client(self, username):
		if self.clients.find_one({DBHandler.FIELD_CLIENT_USER: username}) is None:
			self.clients.insert_one({DBHandler.FIELD_CLIENT_USER: username})
		