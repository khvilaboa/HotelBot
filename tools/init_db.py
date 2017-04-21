
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

print("Limpiando datos anteriores...")
hotels.remove()
rooms.remove()

print("\nIntroduciendo datos del hotel...")
hotels.insert_one({"room_prices": {"individual": 20, "double": 35, "suite": 60}})

room_types = ("individual", "double", "suite") 
ind = 0
print("\nIntroduciendo datos de las habitaciones...")
for floor in range(1, NUM_FLOORS + 1):
	for room in range(1, NUM_ROOMS_PER_FLOOR + 1):
		rooms.insert({"floor": floor, "number": room, "type": room_types[ind]})
		ind = (ind + 1) % len(room_types)

print("\n\nBase de datos iniciada con exito :)")
raw_input()