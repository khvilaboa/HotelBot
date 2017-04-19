#!/usr/bin/env python
# -*- coding: utf8 -*-

# from resources import Database, Weather

import langdetect, langid, textblob
import nltk, pdb, pymongo, re, string
from collections import OrderedDict
from utils import spellchecker as sc, postagger as pos, dateparser as dp
from intellect.Intellect import Intellect, Callable
from facts import Desire, Response, Reservation
from handlers import DBHandler
from datetime import datetime


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
        self.text_sc = ' '.join([sc.correction(w) for w in self.text_san.split()])
        self.lang = self.language(self.text_sc)
        self.dateparsed = dp.parse(self.text_sc)
        self.parsed = self.tokenize(self.dateparsed)
        self.tagged = pos.tag(self.parsed)
        
    def __str__(self):
        return self.text
        
    def sanitize(self, text):
        rep = {u'á': 'a', u'é': 'e', u'í': 'i', u'ó': 'o', u'ú': 'u', u'Á': 'A', u'É': 'E', u'Í': 'I', u'Ó': 'O', u'Ú': 'U', u'ü': 'u', u'Ü': 'u', u'ñ': 'n', u'Ñ': 'n'}   # temporal
        for k, v in rep.iteritems(): text = text.replace(k, v)
        return ''.join(filter(lambda c: c in string.printable, text))
    
    def tokenize(self, text):
        # Remove punctuation symbols
        text = ''.join([c for c in text if c not in UserInput.non_words])

        # Separate words
        tokens =  nltk.word_tokenize(text)
        
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
    def desires(self, last_question = None):
        des = []
        
        verbs_want = ("queria", "quiero", "qerria", "necesitaba", "necesitaria", "gustaria")
        noun_room = ("habitacion", "reserva")
        
        room_types = ("individual", "doble", "suite")
        pension_types = ("completa", "parcial", "desayuno")
        
        afirmations = ("si", "vale")
        
        if (self.has_word(verbs_want, UserInput.VERB) and self.has_word(noun_room, UserInput.NOUN)) or last_question == Response.ASK_ROOM_TYPE:
            room_type = None
            for rt in room_types:
                if self.has_word(rt):
                    room_type = rt
      
            if room_type is not None:  # Room type specified
                d = Desire(Desire.ESTABLISH_ROOM_TYPE)
                d.data["room_type"] = room_type 
                des.append(d)
            elif last_question != Response.ASK_ROOM_TYPE:
                des.append(Desire(Desire.WANT_ROOM))
        if last_question == Response.ASK_INIT_DATE and len(self.dates()) > 0:
            d = Desire(Desire.ESTABLISH_INIT_DATE)
            d.data["init_date"] = self.dates()[0] 
            des.append(d)
        if last_question == Response.ASK_END_DATE and len(self.dates()) > 0:
            d = Desire(Desire.ESTABLISH_END_DATE)
            d.data["end_date"] = self.dates()[0] 
            des.append(d)
        #pdb.set_trace()
        if last_question == Response.ASK_PENSION_TYPE and self.has_word(pension_types):
            pension_type = None
            for pt in pension_types:
                if self.has_word(pt):
                    pension_type = pt
                    
            d = Desire(Desire.ESTABLISH_PENSION_TYPE)
            d.data["pension_type"] = pension_type
            des.append(d)
        if last_question == Response.SHOW_INTRO_SUMMARY and self.has_word(afirmations):
            des.append(Desire(Desire.FINISH_RESERVATION))
        
        return des or None
        
    # Check if the input have some of the verbs in a list
    def has_word(self, lst, word_type = None):
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

    # Returns the first response of the knowledge
    def extract_response(self):
        for fact in self.knowledge:
            if type(fact) is Response:
                self._knowledge.remove(fact)
                return fact
        return None
        
    # Add a desire to the facts database 
    def add_desire(self, des):
        #if des.is_goal():
        #    self.goals.append(des.id)
        self.learn(des)
        
    # Returns the first response of the knowledge
    def clear_desires(self):
        for fact in self.knowledge:
            if type(fact) is Desire:
                self._knowledge.remove(fact)
                
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
        else:
            resp = [Response.SHOW_INTRO_SUMMARY]
            resp.append(reservation.summary())
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
        
        desires = input.desires(self.intellect.last_question)
        #pdb.set_trace()
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
            
        print(msg)  # Only for testing purposes
        return 1, resp  # trust, response



class InsultsAgent:
    def evaluate(self, input):
        return 0, Response(Response.UNKNOWN_INPUT)  # trust, response
