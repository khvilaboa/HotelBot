#!/usr/bin/env python
# -*- coding: utf8 -*-

from datetime import datetime, timedelta

import langdetect
import langid
import nltk
import re
import string
import textblob
from pymongo import MongoClient

from facts import Response, Goal
from utils import spellchecker as sc, dateparser as dp, postagger as pos


# To encapsulate the client's message and doing preparse tasks
class UserInput:
    VERB = "v"
    NOUN = "n"

    stopwords = nltk.corpus.stopwords.words('spanish')
    stemmer = nltk.stem.SnowballStemmer('spanish')
    non_words = list(string.punctuation) + ['¿', '¡']

    def __init__(self, text):
        self.text = text
        self.text_san = self.sanitize(text)
        self.text_sc = ' '.join([sc.correction(w) if not re.match("[0-9]+", w) else w for w in self.text_san.split()])
        self.lang = self.language(self.text_sc)
        self.dateparsed = dp.parse(self.text_sc)
        self.parsed = self.tokenize(self.dateparsed)
        self.tagged = pos.tag(self.parsed)

    def __str__(self):
        return self.text

    def sanitize(self, text):
        rep = {u'á': 'a', u'é': 'e', u'í': 'i', u'ó': 'o', u'ú': 'u', u'Á': 'A', u'É': 'E', u'Í': 'I', u'Ó': 'O',
               u'Ú': 'U', u'ü': 'u', u'Ü': 'u', u'ñ': 'n', u'Ñ': 'n'}  # temporal
        for k, v in rep.iteritems(): text = text.replace(k, v)
        return ''.join(filter(lambda c: c in string.printable, text))

    def tokenize(self, text):
        # Remove punctuation symbols
        text = ''.join([c for c in text if c not in UserInput.non_words])

        # Separate words
        tokens = nltk.word_tokenize(text)

        try:
            stems = map(lambda token: UserInput.stemmer.stem(token), tokens)
        except Exception as e:
            print(e)
            print(text)
            stems = ['']
        return stems

    def language(self, text):
        try:
            # Try to detect the language with three different packages
            lang1 = langid.classify(text)[0]
            lang2 = langdetect.detect(text)
            lang3 = textblob.TextBlob(text).detect_language()

            print(lang1, lang2, lang3)

            if lang1 == lang2 == lang3:  # If all of them throw the same result, return it
                return lang1
            elif lang1 == 'es' or lang2 == 'es' or lang3 == 'es':  # If at least one detect spanish...
                return 'es'
            else:
                return lang1
        except Exception as e:
            print(e)
            return None  # Insuficient information

    # Generates the desires based on the user input
    def goals(self, last_question=None):
        des = []

        verbs_want = ("queria", "quiero", "qerria", "necesitaba", "necesitaria", "gustaria")
        noun_room = ("habitacion", "reserva", "individual", "doble", "suite")

        room_types = ("individual", "doble", "suite")
        pension_types = ("completa", "parcial", "desayuno")

        afirmations = ("si", "yep", "vale", "nada", "bien")
        denials = ("no", "nope")

        greetings = ("hola", "saludos", "hi")

        # ---------------------
        # RESERVATION GOALS
        # ---------------------
        if (self.has_word(greetings) or \
                    (self.has_word(["buenos"]) and self.has_word(["dias"])) or \
                    (self.has_word(["buenas"]) and self.has_word(["tardes", "noches"]))):
            des.append(Goal(Goal.GREET_USER))

        if (self.has_word(verbs_want, UserInput.VERB) and self.has_word(noun_room,
                                                                        UserInput.NOUN)) or last_question == Response.ASK_ROOM_TYPE:
            room_type = None
            for rt in room_types:
                if self.has_word(rt):
                    room_type = rt

            if room_type is not None:  # Room type specified
                d = Goal(Goal.ESTABLISH_ROOM_TYPE)
                d.data["room_type"] = room_type
                des.append(d)
            else:
                des.append(Goal(Goal.WANT_ROOM))
        if (last_question == Response.ASK_INIT_DATE or self.has_word(
                ["comienzo", "entrada", "empezando", "del", "desde"])) and len(self.dates()) > 0:
            d = Goal(Goal.ESTABLISH_INIT_DATE)
            d.data["init_date"] = self.dates()[0]
            des.append(d)
        if (last_question == Response.ASK_END_DATE and len(self.dates()) > 0) or \
                (self.has_word(["hasta", "al"]) and len(self.dates()) > 1) or \
                (self.has_word(["salida", "hasta"]) and len(self.dates()) > 0):
            d = Goal(Goal.ESTABLISH_END_DATE)
            d.data["end_date"] = self.dates()[-1]
            des.append(d)
        # pdb.set_trace()
        if self.has_word(pension_types):  # last_question == Response.ASK_PENSION_TYPE and
            pension_type = None
            for pt in pension_types:
                if self.has_word(pt):
                    pension_type = pt

            d = Goal(Goal.ESTABLISH_PENSION_TYPE)
            d.data["pension_type"] = pension_type
            des.append(d)
        if last_question == Response.SHOW_INTRO_SUMMARY:
            if self.has_word(afirmations):
                d = Goal(Goal.CONFIRM_RESERVATION)
                d.data["response"] = "yes"
                des.append(d)
            elif self.has_word(denials):
                d = Goal(Goal.CONFIRM_RESERVATION)
                d.data["response"] = "no"
                des.append(d)
        print(last_question, last_question == Response.ASK_SERVICES)
        if last_question == Response.ASK_SERVICES[0]:
            services = []
            if self.has_word(["supletoria"]) or (self.has_word(["cama"]) and self.has_word(["adicional"])):
                services.append("additional_bed")
            if self.has_word(["parking", "aparcamiento"]):
                services.append("parking")
            if self.has_word(["minibar"]):
                services.append("minibar")

            if not services and self.has_word(denials):
                des.append(Goal(Goal.SHOW_SUMMARY))
            elif services or self.has_word(afirmations):
                d = Goal(Goal.ASK_SERVICE)
                d.data["services"] = services
                des.append(d)
        if last_question == Response.ASK_EMAIL and self.mails() is not None:
            d = Goal(Goal.UPDATE_EMAIL)
            d.data["email"] = self.mails()[-1]
            des.append(d)

        # ---------------------
        # INFORMATION GOALS
        # ---------------------
        # pdb.set_trace()
        if (self.has_word(["ensenar", "ensenarme", "mostrar", "mostrarme", "ver"]) and \
                    self.has_word(["habitacion", "habitaciones"]) and \
                    self.has_word(
                        ["contais", "cuentas", "teneis", "tienes", "disponeis", "dispones", "hotel", "tipo"])):
            des.append(Goal(Goal.SHOW_ROOMS))

        return des or None

    # Check if the input have some of the verbs in a list
    def has_word(self, lst, word_type=None):
        if type(lst) is str:
            lst = (lst,)
        lst = map(self.stemmer.stem, lst)
        for word, tag in self.tagged.iteritems():
            if (word_type is None or (tag is not None and tag.startswith(word_type))) and word in lst:
                return True
        return False

    # Check if the input have some of the verbs in a list
    def dates(self):
        dates = []
        for word, tag in self.tagged.iteritems():
            if tag is not None and tag.startswith("dt"):
                dates.append("%s/%s/%s" % (word[:2], word[2:4], word[4:]))
        return dates

    def mails(self):
        mails = []
        for word in self.text_san.split():
            if re.match("^[^@]+@[^@]+\.[^@]+$", word):
                mails.append(word)
        return mails


class DBHandler:
    ROOM_INDIVIDUAL = "individual"
    ROOM_DOUBLE = "double"
    ROOM_SUITE = "suite"

    PENSION_FULL = "completa"
    PENSION_HALF = "parcial"
    PENSION_BREAKFAST = "desayuno"

    FIELD_CLIENT_USER = "username"
    FIELD_CLIENT_RESERV = "reservations"
    FIELD_CLIENT_EMAIL = "email"

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

        self.clients.update({DBHandler.FIELD_CLIENT_USER: username},
                            {"$push": {DBHandler.FIELD_CLIENT_RESERV: reserv_doc}})

    def free_room_from_dates(self, init_date, end_date=None, room_type=None):
        days = self.dates_in_interval(init_date, end_date) if end_date else [init_date]

        if room_type is None:
            results = self.rooms.find({"reservations": {"$nin": days}})
        else:
            results = self.rooms.find({"reservations": {"$nin": days}, "type": room_type})

        return results.next() if results.count() != 0 else None

    def dates_in_interval(self, init_date, end_date):
        idt = datetime.strptime(init_date, "%d/%m/%Y")
        edt = datetime.strptime(end_date, "%d/%m/%Y")
        delta = timedelta(days=1)
        days = []

        while idt != edt:
            days.append(idt.strftime("%d/%m/%Y"))
            idt += delta

        # days.append(idt.strftime("%d/%m/%Y"))
        return days

    def check_client(self, username):
        if self.clients.find_one({DBHandler.FIELD_CLIENT_USER: username}) is None:
            self.clients.insert_one({DBHandler.FIELD_CLIENT_USER: username})


    def client_email(self, username):
        client = self.clients.find_one({DBHandler.FIELD_CLIENT_USER: username})
        if client is not None and DBHandler.FIELD_CLIENT_EMAIL in client:
            return client[DBHandler.FIELD_CLIENT_EMAIL]
        return None

    def update_email(self, username, email):
        self.clients.update({DBHandler.FIELD_CLIENT_USER: username}, {"$set": {DBHandler.FIELD_CLIENT_EMAIL: email}})


    # Returns the price of a specific type of room
    def price(self, room_type):
        return self.hotels.find_one()["room_prices"][room_type]

    def price_pension(self, pension_type):
        return self.hotels.find_one()["pension_prices"][pension_type]

    def location(self):
        loc = self.hotels.find_one()["location"]
        return (loc["latitude"], loc["longitude"])
