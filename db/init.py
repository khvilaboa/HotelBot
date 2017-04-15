
from pymongo import MongoClient
import sys

NUM_FLOORS = 5
NUM_ROOMS_PER_FLOOR = 10

print("Conectando con la base de datos...")
try:
	client = MongoClient()
except:
	print("\nFallo al conectar.")
	raw_input()
	sys.exit(1)

hotel = client.hotelbot

hotels = hotel.hotels
rooms = hotel.rooms
#clients = hotel.clients

print("\nIntroduciendo datos del hotel...")
hotels.insert_one({"price_individual": 20, "price_double": 35, "price_suite": 60})

print("\nIntroduciendo datos de las habitaciones...")
for floor in range(1, NUM_FLOORS + 1):
	for room in range(NUM_ROOMS_PER_FLOOR + 1):
		rooms.insert({"floor": floor, "number": room})

print("\n\nBase de datos iniciada con exito :)")
raw_input()