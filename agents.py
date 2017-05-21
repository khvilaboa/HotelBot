#!/usr/bin/env python
# -*- coding: utf8 -*-

# from resources import Database, Weather

from intellect.Intellect import Intellect, Callable
from facts import Goal, Response, Reservation
from resources import DBHandler
import pdb, random


# Custom intellect to improve the management of facts and policies
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

        next = self.next_question()
        if m is not None and m.next_question:
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
        if user_resp == "yes":
            self.last_question = Response.FINISH_RESERVATION
            self.finish_reservation()
            return Response.FINISH_RESERVATION
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
            if service == "aditional_bed":
                msg.append(Response.SERVICE_ADITIONAL_BED)
                reserv.aditional_bed = True
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
        self._knowledge.remove(reserv)
        self.learn(Reservation())


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

        pdb.set_trace()
        desires = input.goals(self.intellect.last_question)
        if desires is not None:
            print("Desires: ")
            for d in desires: print(d.id)

            for desire in desires:
                self.intellect.add_desire(desire)
            self.intellect.reason()
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
    RACIST = ["negrata", "sudaca", "moro", "esclavo"];
    MACHIST = ["zorra", "esclava", "maricon"];
    GENERICS = ["puta", "puto", "cabron", "cabrona", "gilipollas"];
    RESPONSE = ["No puedo seguir la conversación en este tono ", "La educación es lo primero",
                "Por favor, no utilice palabras malsonantes",
                "El tono de la conversación no debe seguir por este camino", "Hable con educacion",
                "No utilice lenguaje soez"];

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
