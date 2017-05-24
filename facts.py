#!/usr/bin/env python
# -*- coding: utf8 -*-

# To comunicate de client's desires to the intellect


class Goal(object):

    UPDATE_EMAIL = "updateEmail"
    WANT_ROOM = "wantRoom"
    ESTABLISH_ROOM_TYPE = "roomType"
    ESTABLISH_INIT_DATE = "initDate"
    ESTABLISH_END_DATE = "endDate"
    ESTABLISH_PENSION_TYPE = "pensionType"
    CONFIRM_RESERVATION = "finishReservation"
    ASK_SERVICE = "wantService"
    SHOW_SUMMARY = "showSummary"
    SHOW_ROOMS = "showRooms"
    GREET_USER = "greetUser"

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
        return self.id == Goal.ESTABLISH_ROOM_TYPE


# To extract the intellect response
class Response(object):
    GREETINGS = ["Saludos", "Bienvenido", "Hola"]

    ASK_ROOM_TYPE = "¿Que tipo de habitacion quieres?"
    ASK_INIT_DATE = "¿Que dia quieres comenzar tu estancia?"
    ASK_END_DATE = "¿Hasta que dia quieres estar?"
    ASK_PENSION_TYPE = "¿Que tipo de pension prefieres?"
    SHOW_INTRO_SUMMARY = "Los datos de la reserva son los siguientes:"
    ASK_WRONG_INFO = "Bueno... ¿que quieres cambiar entonces?"
    ASK_SERVICES = ["¿Estas interesado en alguno de nuestros servicios?",
                    "Disponemos de camas supletorias, parking y minibar"]
    # , "Además te puedo hablar de lugares cercanos que te puedan ser de interes"
    FINISH_RESERVATION = "Perfecto, guardo la reserva. Gracias por usar nuestros servicios."

    ASK_EMAIL = "¿Cual es tu direccion de correo electronico? (para enviarte el resumen de la reserva)"

    SHOW_ROOMS = "Disponemos de los siguientes tipos de habitacion:"

    NO_INIT_DATE = "Lo siento, pero no tenemos {type} disponibles para esa fecha"

    CONFIRM_ROOM_TYPE = "Una {room_type} pues"
    CHANGE_ROOM_TYPE = "Tenia apuntada una {room_type}... cambio a una {new_room_type}"

    CONFIRM_INIT_DATE = "Fecha de entrada para el {date}..."
    CONFIRM_END_DATE = "Fecha de salida para el {date}..."
    CONFIRM_PENSION_TYPE = "Bien, {pension_type} entonces"

    CONFIRM_BASIC = "Esta todo correcto?"

    UNKNOWN_INPUT = "Perdona, pero no te he entendido"

    KNOWN_INFO = "Ya, ya me lo habias comentado"

    TOTAL_PRICE = "Precio total: {price} EUR"

    SERVICE_ADITIONAL_BED = "Añado una cama supletoria"
    SERVICE_PARKING = "Añado el servicio de parking"
    SERVICE_MINIBAR = "El minibar se combrará en función de las bebidas que se consuman en la habitacion (2 EUR por bebida)"
    SERVICE_MORE = "¿Algo mas?"
    SERVICE_WHAT = "¿De que servicios quiere disponer?"

    KEYBOARD_ROOM_TYPES = "keyboardRoomTypes"
    KEYBOARD_PENSION_TYPES = "keyboardPensionTypes"

    ACTION_SHOW_ROOMS = "showRooms"

    def __init__(self, msg = [], keyboard = None, next_question = True, action = None):
        #pdb.set_trace()
        msg = [msg] if type(msg) is str else msg
        self._msg = []
        for m in msg:
            if type(m) is list:
                self._msg += m
            else:
                self._msg.append(m)
        self._keyboard = keyboard
        self._next_question = next_question
        self._action = action

    def merge(self, resp):
        for text in resp.msg:
            self._msg.append(text)
        if self.keyboard is None and resp.keyboard is not None:
            self.keyboard = resp.keyboard
        return self

    def append(self, new):
        if type(new) is str:
            self._msg.append(new)
        else:
            for text in new:
                self._msg.append(text)

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

    @property
    def next_question(self):
        return self._next_question

    @next_question.setter
    def next_question(self, value):
        self._next_question = value

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value


class Reservation(object):
    def __init__(self):
        self._room_type = None
        self._pension_type = None
        self._init_date = None
        self._end_date = None
        self._parking = False
        self._additional_bed = False
        self._weather = None

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

    @property
    def parking(self):
        return self._parking

    @parking.setter
    def parking(self, value):
        self._parking = value

    @property
    def additional_bed(self):
        return self._additional_bed

    @additional_bed.setter
    def additional_bed(self, value):
        self._additional_bed = value

    @property
    def weather(self):
        return self._weather

    @weather.setter
    def weather(self, value):
        self._weather = value

    def summary(self):
        summ = ""
        if self.room_type is not None:
            summ += "Tipo de habitacion: %s\n" % self.room_type
        if self.init_date is not None:
            summ += "Fecha de entrada: %s\n" % self.init_date
        if self.end_date is not None:
            summ += "Fecha de salida: %s\n" % self.end_date
        if self.pension_type is not None:
            summ += "Tipo de pension: %s\n" % self.pension_type

        summ += "Cama supletoria: %s\n" % ("Si" if self.additional_bed else "No")
        summ += "Parking: %s\n" % ("Si" if self.parking else "No")
        summ += "Prevision meteorologica: %s\n " % self.weather

        return summ
