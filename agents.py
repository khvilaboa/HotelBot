#!/usr/bin/env python
# -*- coding: utf8 -*-

# from resources import Database, Weather
import os
import pdb

import random
from datetime import datetime

from intellect.Intellect import Intellect, Callable

from facts import Goal, Response, Reservation
from resources import DBHandler
# Custom intellect to improve the management of facts and policies
from utils.weather import Weather

# Custom intellect to improve the management of facts and policies
from utils.mail import Email

class MyIntellect(Intellect):
    def __init__(self, username, db):
        Intellect.__init__(self)
        self.goals = []
        self.learn(Reservation())
        self.last_question = None
        self.db = db
        self.username = username

    @Callable  # It can be called form the rules file
    def clear_facts(self):
        self._knowledge = []

    # Returns the responses of the knowledge
    def extract_response(self):
        m = None
        i = 0
        while i < len(self._knowledge):
            fact = self._knowledge[i]
            if type(fact) is Response:
                self._knowledge.remove(fact)
                if m is None:
                    m = fact
                else:
                    m = m.merge(fact)
            else:
                i += 1

        if m is not None and m.next_question:
            next = self.next_question()
            m.append(next)
            if next == Response.ASK_PENSION_TYPE:
                m.keyboard = Response.KEYBOARD_PENSION_TYPES

        return m

    # Add a desire to the facts database 
    def add_desire(self, des):
        # if des.is_goal():
        #    self.goals.append(des.id)
        self.learn(des)

    # Returns the first response of the knowledge
    def clear_desires(self):
        i = 0
        while i < len(self._knowledge):
            fact = self._knowledge[i]
            if type(fact) is Goal:
                self._knowledge.remove(fact)
            else:
                i += 1

    # Forget the last question (when it's already resolved)
    def clear_last_question(self):
        self.last_question = None

    # Returns the next question in the preferred flowchart
    @Callable
    def next_question(self):
        reservation = self.reservation()
        resp = None
        if reservation.room_type is None:
            resp = Response.ASK_ROOM_TYPE
        elif reservation.init_date is None:
            resp = Response.ASK_INIT_DATE
        elif reservation.end_date is None:
            resp = Response.ASK_END_DATE
        elif reservation.pension_type is None:
            resp = Response.ASK_PENSION_TYPE
        elif self.last_question != Response.SHOW_INTRO_SUMMARY:
            resp = Response.ASK_SERVICES
        else:
            price_per_night = self.db.price(reservation.room_type)
            price_pension = self.db.price_pension(reservation.pension_type)
            num_nights = len(self.db.dates_in_interval(reservation.init_date, reservation.end_date))
            db = DBHandler()
            hotel_loc = db.location()
            weather = Weather("86b4bc5747efd019c9d6bf0da2c84813")

            try:
                reservation.weather = weather.codes[weather.get_daily_forecast(*hotel_loc).get_weather_at(datetime.strptime(reservation.init_date, '%d/%m/%Y')).get_weather_code()]
            except:
                reservation.weather = None

            resp = [Response.SHOW_INTRO_SUMMARY]
            resp.append(reservation.summary())
            resp.append(Response.TOTAL_PRICE.format(price=num_nights * (price_per_night + price_pension)))
            resp.append(Response.CONFIRM_BASIC)

        self.last_question = resp if type(resp) is not list else resp[0]
        return resp

    # Get the reservation object from the fact database
    @Callable
    def reservation(self):
        for fact in self.knowledge:
            if type(fact) is Reservation:
                return fact

    # --------------------------------------------------------
    # Return the suitable message based on the last and new (if exists) type of room chosed
    @Callable
    def response_from_room_types(self, last, new):
        reserv = self.reservation()
        print(last, new)
        # It was already specified in the past...
        if last is not None:
            # ... and it matchs with the new info...
            if last == new:
                msg = Response.KNOWN_INFO
            else:
                msg = Response.CHANGE_ROOM_TYPE.replace("{room_type}", last).replace("{new_room_type}", new)
                reserv.room_type = new
        else:
            msg = Response.CONFIRM_ROOM_TYPE.replace("{room_type}", new)
            reserv.room_type = new

        return msg

    @Callable
    def response_from_init_date(self, init_date):
        reserv = self.reservation()
        if self.db.free_room_from_dates(init_date, room_type=reserv.room_type):
            reserv.init_date = init_date
            msg = [Response.CONFIRM_INIT_DATE.replace("{date}", init_date)]
        else:
            room_type = reserv.room_type if reserv.room_type is not None else "habitaciones"
            room_type += "s" if room_type != DBHandler.ROOM_INDIVIDUAL else "es"
            msg = Response.NO_INIT_DATE.format(type=room_type)

        return msg

    # Handle the confirmation response when the bot shows the summary
    @Callable
    def confirm_reservation(self, user_resp):
        db = DBHandler()
        if user_resp == "yes":
            if db.client_email(self.username):
                self.last_question = Response.FINISH_RESERVATION
                self.finish_reservation()
                return Response.FINISH_RESERVATION
            else:
                self.last_question = Response.ASK_EMAIL
                return Response.ASK_EMAIL
        else:
            return Response.ASK_WRONG_INFO

    @Callable
    def show_summary(self):
        self.last_question = Response.SHOW_INTRO_SUMMARY

    # Handle the confirmation response when the bot shows the summary
    @Callable
    def set_services(self, services):
        reserv = self.reservation()
        msg = []

        for service in services:
            if service == "additional_bed":
                msg.append(Response.SERVICE_ADDITIONAL_BED)
                reserv.additional_bed = True
            elif service == "parking":
                msg.append(Response.SERVICE_PARKING)
                reserv.parking = True
            elif service == "minibar":
                msg.append(Response.SERVICE_MINIBAR)

        if msg:
            msg.append(Response.SERVICE_MORE)
        else:
            msg.append(Response.SERVICE_WHAT)

        return msg

    # Save current reservation (finished) in the DB and reset it in the facts base
    @Callable
    def finish_reservation(self):
        reserv = self.reservation()
        self.db.add_reservation(self.username, reserv)

        email = self.db.client_email(self.username)
        if email is not None:
            mail = Email("dasihotelbot@gmail.com", "3m0j1Lun4")
            print(os.getcwd())
            print("images\\%s.jpg" % reserv.room_type)
            print(os.getcwd() + "\\images\\%s.jpg" % reserv.room_type)
            mail.send_email_with_attachments("dasihotelbot@gmail.com", email, "Resumen de reserva", reserv.summary(), ["images/%s.jpg" % reserv.room_type])

        self._knowledge.remove(reserv)
        self.learn(Reservation())

    @Callable
    def update_email(self, email):
        self.db.update_email(self.username, email)

    @Callable
    def reply_to_pois_request(self, pois_types):
        db = DBHandler()
        # Make a method to retrieve the pois in a common format (with a optional param to filter)
        msg = [Response.POIS_PLACES]

        if pois_types:
            for pois_type in pois_types:
                for place in db.get_pois(pois_type):
                    if str(place['pois']['webpage']) is not None:
                        msg.append(
                            '\xF0\x9F\x9A\xA9' + str(place['pois']['name']).encode('utf-8') + '\xF0\x9F\x9A\xA9' +
                            '\n Descripción: ' + str(place['pois']['description']).encode('utf-8') +
                            '\n\n Dirección: ' + str(place['pois']['direction']).encode('utf-8') +
                            '\n\n ¿Cómo llegar?: ' + str(place['pois']['gmaps_url']).encode('utf-8') +
                            '\n\n Página web: ' + str(place['pois']['webpage']).encode('utf-8'))
                    else:
                        msg.append(
                            '\xF0\x9F\x9A\xA9' + str(place['pois']['name']).encode('utf-8') + '\xF0\x9F\x9A\xA9' +
                            '\n Descripción: ' + str(place['pois']['description']).encode('utf-8') +
                            '\n\n Dirección: ' + str(place['pois']['direction']).encode('utf-8') +
                            '\n\n ¿Cómo llegar?: ' + str(place['pois']['gmaps_url']).encode('utf-8'))
        else:
            for place in db.get_pois(limit=5):
                if str(place['pois']['webpage']) is not None:
                    msg.append('\xF0\x9F\x9A\xA9' + str(place['pois']['name']).encode('utf-8') + '\xF0\x9F\x9A\xA9' +
                               '\n Descripción: ' + str(place['pois']['description']).encode('utf-8') +
                               '\n\n Dirección: ' + str(place['pois']['direction']).encode('utf-8') +
                               '\n\n ¿Cómo llegar?: ' + str(place['pois']['gmaps_url']).encode('utf-8') +
                               '\n\n Página web: ' + str(place['pois']['webpage']).encode('utf-8'))
                else:
                    msg.append('\xF0\x9F\x9A\xA9' + str(place['pois']['name']).encode('utf-8') + '\xF0\x9F\x9A\xA9' +
                               '\n Descripción: ' + str(place['pois']['description']).encode('utf-8') +
                               '\n\n Dirección: ' + str(place['pois']['direction']).encode('utf-8') +
                               '\n\n ¿Cómo llegar?: ' + str(place['pois']['gmaps_url']).encode('utf-8'))
        return msg

class HotelAgent:
    def __init__(self, username):

        try:
            self.db = DBHandler()
            self.db.check_client(username)
        except:
            print("The connection with the DB could not be established")

        self.intellect = MyIntellect(username, self.db)
        self.intellect.learn(Intellect.local_file_uri("./policies/hotel.policy"))

    def evaluate(self, input):
        msg = "Language: %s" % input.lang
        msg += "\nSanitized: %s" % input.text_san
        msg += "\nCorrected: %s" % input.text_sc
        msg += "\nDateparser: %s" % input.dateparsed
        msg += "\nTokenized: %s" % input.parsed
        msg += "\nTagged: %s" % input.tagged

        resp = None

        desires = input.goals(self.intellect.last_question)
        if desires is not None:
            print("Desires: ")
            for d in desires: print(d.id)

            for desire in desires:
                self.intellect.add_desire(desire)
            self.intellect.reason()
            #pdb.set_trace()
            resp = self.intellect.extract_response()

            if resp is not None:
                msg += "\nIntellect test: %s" % resp.msg

        self.intellect.clear_desires()  # Remove the current desires

        if resp is None:
            resp = Response(Response.UNKNOWN_INPUT)
        # resp.msg = [msg]
        print(msg)  # Only for testing purposes
        return 1, resp  # trust, response


class InsultsAgent:
    RACIST = ["negrata", "sudaca", "moro", "esclavo"]
    MACHIST = ["zorra", "esclava", "maricon"]
    GENERICS = ["puta", "puto", "cabron", "cabrona", "gilipollas"]
    RESPONSE = ["No puedo seguir la conversación en este tono ", "La educación es lo primero",
                "Por favor, no utilice palabras malsonantes",
                "El tono de la conversación no debe seguir por este camino", "Hable con educacion",
                "No utilice lenguaje soez"]

    def evaluate(self, input):
        if input.has_word(InsultsAgent.RACIST) or input.has_word(InsultsAgent.MACHIST) or input.has_word(
                InsultsAgent.GENERICS):
            return 1, Response(random.choice(InsultsAgent.RESPONSE))
        return 0, Response(Response.UNKNOWN_INPUT)


class LanguagesAgent:
    def evaluate(self, input):

        if input.lang == "en":
            return 1, Response("I only talk in spanish")  # trust, response
        elif input.lang == "de":
            return 1, Response("Ich spreche nur Spanisch")  # trust, response
        elif input.lang == "it":
            return 1, Response("Io solo parliamo spagnolo")  # trust, response
        elif input.lang == "fr":
            return 1, Response("Je parle seulement espagnol")  # trust, response
        elif input.lang == "pt":
            return 1, Response("Eu só falo espanhol")  # trust, response

        return 0, Response(Response.UNKNOWN_INPUT)
