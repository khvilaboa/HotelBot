import sys

from pymongo import MongoClient

NUM_FLOORS = 5
NUM_ROOMS_PER_FLOOR = 10

print("Conectando con la base de datos...")
try:
    client = MongoClient('hotelbot_mongodb')
except:
    print("\nFallo al conectar.")
    sys.exit(1)

hotel = client.hotelbot

hotels = hotel.hotels
rooms = hotel.rooms
# clients = hotel.clients

print("Limpiando datos anteriores...")
hotels.remove()
rooms.remove()

pois = {
    {"name": "Museo Nacional del Prado", "category": "museum",
     "description": "Colección de obras de arte de los siglos XII a XIX y obras maestras de Velázquez, Goya y el Greco",
     "direction": "Paseo del Prado, s/n, 28014 Madrid",
     "image_url": "https://lh5.googleusercontent.com/-QG6bCog6rkc/V7lwShQLv7I/AAAAAAAAOqA/BbZ198r0cBUTgZyxGppfEdnjmvNcG8mfACLIB/w408-h229-k-no/",
     "gmaps_url": "https://www.google.es/maps/place/Museo+Nacional+del+Prado/@40.4131548,-3.6946385,17.56z/data=!4m12!1m6!3m5!1s0xd422629b5775fad:0x1bca8445c2598f5c!2sLa+Tragant%C3%BAa!8m2!3d40.4117985!4d-3.69542!3m4!1s0x0:0x1094f07d93ad885a!8m2!3d40.413782!4d-3.6921271",
     "webpage": "http://museodelprado.es"},
    {"name": "CaixaForum Madrid", "category": "museum",
     "description": "Centro artístico diseñado por Herzog & de Meuron y antigua central eléctrica, con exposiciones y actuaciones",
     "direction": "Paseo del Prado, 36, 28014 Madrid",
     "image_url": "https://lh5.googleusercontent.com/-LlVOhGKDSbU/WNzAOdCKBMI/AAAAAAAAAK4/x2jOGiXyJ9YzSluIBphICOtdiPZYp6JcACLIB/w408-h263-k-no/",
     "gmaps_url": "https://www.google.es/maps/place/CaixaForum+Madrid/@40.4125021,-3.6943334,17.56z/data=!3m1!5s0xd42262864fde11b:0xe730d349041d5df7!4m12!1m6!3m5!1s0xd422629b5775fad:0x1bca8445c2598f5c!2sLa+Tragant%C3%BAa!8m2!3d40.4117985!4d-3.69542!3m4!1s0x0:0x69896fe32fd5b83b!8m2!3d40.4111123!4d-3.6935708",
     "webpage": "http://madrid.caixaforum.com"},
    {"name": "Museo Thyssen-Bornemisza", "category": "museum",
     "description": "Museo que alberga obras maestras europeas del s. XIII al XX, desde el Renacimiento hasta el Arte pop",
     "direction": "Paseo del Prado, 8, 28014 Madrid",
     "image_url": "https://lh5.googleusercontent.com/-ArP14SKRuTE/WPnvaJg_nEI/AAAAAAAAABs/zSi9Nje70NYBvQtMkpKBO9t9HzS0Zbi_wCLIB/w408-h383-k-no/",
     "gmaps_url": "https://www.google.es/maps/place/Museo+Thyssen-Bornemisza/@40.4147478,-3.6963748,17.56z/data=!4m12!1m6!3m5!1s0xd422629b5775fad:0x1bca8445c2598f5c!2sLa+Tragant%C3%BAa!8m2!3d40.4117985!4d-3.69542!3m4!1s0x0:0x5a934a7882cb528f!8m2!3d40.4160406!4d-3.6949253",
     "webpage": "http://museothyssen.org"},
    {"name": "Congreso de los Diputados", "category": "building", "description": "Oficina de la administración",
     "direction": "Calle de Floridablanca, S/N, 28071 Madrid",
     "image_url": "https://lh6.googleusercontent.com/-y3wneaVtNN8/V6nj_gnv7II/AAAAAAAAeeM/pNAGp_QwLycBEAoNzilRNGZ-TBOemJv0gCLIB/w408-h306-k-no/",
     "gmaps_url": "https://www.google.es/maps/place/Congreso+de+los+Diputados/@40.4157986,-3.6973197,18.08z/data=!4m12!1m6!3m5!1s0xd422629b5775fad:0x1bca8445c2598f5c!2sLa+Tragant%C3%BAa!8m2!3d40.4117985!4d-3.69542!3m4!1s0x0:0xdb2be4f41b46e600!8m2!3d40.4161478!4d-3.6966587",
     "webpage": "http://congreso.es"},
    {"name": "Fuente de Neptuno", "category": "building", "description": "Fuente",
     "direction": "Plaza Cánovas del Castillo, s/n, 28014 Madrid",
     "image_url": "https://lh3.googleusercontent.com/-Y4_6D3-QTrs/V71voU7Tq9I/AAAAAAAABFY/MpFv8BHaLyA6JDmre5VIj3eV7ZxlR0d5gCLIB/w408-h229-k-no/",
     "gmaps_url": "https://www.google.es/maps/place/Fuente+de+Neptuno/@40.4157175,-3.6955213,18z/data=!4m12!1m6!3m5!1s0xd422629b5775fad:0x1bca8445c2598f5c!2sLa+Tragant%C3%BAa!8m2!3d40.4117985!4d-3.69542!3m4!1s0x0:0xaaed4254d9f36ea0!8m2!3d40.4152651!4d-3.6941629",
     "webpage": "https://www.esmadrid.com/informacion-turistica/fuente-de-neptuno"},
    {"name": "Fuente de Cibeles", "category": "building", "description": "Atracción turistica",
     "direction": "Calle de Alcalá, 3, 28014 Madrid",
     "image_url": "https://lh6.googleusercontent.com/-ZrOfINEoKsM/WEqNKufi7oI/AAAAAAAAZQo/rgYYFeUslVkztzmd9jadEhKkv8uQ2PEHgCLIB/w408-h272-k-no/",
     "gmaps_url": "https://www.google.es/maps/place/Fuente+de+Cibeles/@40.4192833,-3.694007,18z/data=!4m5!3m4!1s0x0:0x325f7e929ee22f72!8m2!3d40.419337!4d-3.6930833",
     "webpage": "https://www.esmadrid.com/informacion-turistica/fuente-de-la-cibeles"},
    {"name": "Basílica de Jesús de Medinaceli", "category": "church", "description": "Lugar de culto",
     "direction": "Plaza Jesús, 2, 28014 Madrid",
     "image_url": "https://lh6.googleusercontent.com/proxy/hvkD32UvhpOxFpOdNYnca30xQxWAPyPTL5Q0_3QgiKHSryGgWaIeGWwVv5SU-975ni8n7-h2xMwLhL8D56VFlyWwhVamrpg=w408-h518-k-no",
     "gmaps_url": "https://www.google.es/maps/place/Bas%C3%ADlica+de+Jes%C3%BAs+de+Medinaceli/@40.4149353,-3.6959863,17.48z/data=!4m5!3m4!1s0x0:0x21b9c5b25fc9db62!8m2!3d40.4142333!4d-3.6955208",
     "webpage": "http://archimadrid.es/jesusmedinaceli/"},
    {"name": "Convento de las Trinitarias Descalzas de San Ildefonso", "category": "church", "description": "Convento",
     "direction": "Calle Lope de Vega, 18, 28014 Madrid",
     "image_url": "https://lh3.googleusercontent.com/-GONxKWIIvVs/WHgw8XOzqcI/AAAAAAAAK_k/SWpTUVIkigEulZDlFY6UbT784OIBvuJOQCLIB/w408-h229-k-no/",
     "gmaps_url": "https://www.google.es/maps/place/Convento+de+las+Trinitarias+Descalzas+de+San+Ildefonso/@40.4139045,-3.6996747,16.12z/data=!4m8!1m2!2m1!1slugar+de+culto!3m4!1s0x0:0x528f43e730d69a51!8m2!3d40.4136911!4d-3.6975606",
     "webpage": None},
    {"name": "Teatro de la Zarzuela", "category": "theater",
     "description": "Zarzuela, danza y conciertos en un emblemático teatro de fachada clásica construido a mediados del siglo XIX.",
     "direction": "Calle de Jovellanos, 4, 28014 Madrid",
     "image_url": "https://lh3.googleusercontent.com/proxy/_auldWmrH3ZlxdIWOcrbPFwPbi8Y8ZI12XWze87ru8XEmM15F235BR7mQVAUK33OIi2_kbq8eBA-5nAdt6C0gLky2XmeQufyMb0FxEmdPpeiN5JwRlDCDvQvezCOI3rCm1XGKRxWAAqPXJ0O3JXBbInZfQ=w408-h272-k-no",
     "gmaps_url": "https://www.google.es/maps/place/Teatro+de+la+Zarzuela/@40.4165943,-3.6992026,17.12z/data=!4m8!1m2!2m1!1slugar+de+culto!3m4!1s0x0:0xa6446797bd4dab2f!8m2!3d40.4171893!4d-3.6969906",
     "webpage": "https://teatrodelazarzuela.mcu.es"}
}

print("\nIntroduciendo datos del hotel...")
hotels.insert_one({"room_prices": {"individual": 20, "doble": 35, "suite": 60}, \
                   "pension_prices": {"completa": 10, "parcial": 6, "desayuno": 3}, \
                   "location": {"latitude": 40.4124689, "longitude": -3.6971957}, "pois": pois})

room_types = ("individual", "doble", "suite")
ind = 0
print("\nIntroduciendo datos de las habitaciones...")
for floor in range(1, NUM_FLOORS + 1):
    for room in range(1, NUM_ROOMS_PER_FLOOR + 1):
        rooms.insert({"floor": floor, "number": room, "type": room_types[ind]})
        ind = (ind + 1) % len(room_types)

print("\n\nBase de datos iniciada con exito :)")
