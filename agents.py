#!/usr/bin/env python
# -*- coding: utf8 -*-

# from resources import Database, Weather

import langdetect, langid, textblob
import nltk, pdb, re, string
from collections import OrderedDict
from utils import spellchecker as sc, postagger as pos
from intellect.Intellect import Intellect, Callable
from facts import *


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
        self.parsed = self.tokenize(self.text_sc)
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
            
            if lang1 == lang2 == lang3:  # If all oh them throws the same result, return it
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
        
        room_types = {"individual", "doble", "suite"}
        
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
       

# Custom intellect to improve the management of facts and policies
class MyIntellect(Intellect):

    def __init__(self):
        Intellect.__init__(self)
        self.goals = []
        self.learn(Reservation())
        self.last_question = None

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

        self.last_question = resp
        return resp
        
    # Get the reservation object from the fact database
    @Callable
    def reservation(self):
        for fact in self.knowledge:
            if type(fact) is Reservation:
                return fact

    # --------------------------------------------------------
    # Support methods for the rules
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

class HotelAgent:
    def __init__(self):
        self.intellect = MyIntellect()
        self.intellect.learn(Intellect.local_file_uri("./policies/hotel.policy"))

    def evaluate(self, input):
        msg = "Language: %s" % input.lang
        msg += "\nSanitized: %s" % input.text_san
        msg += "\nCorrected: %s" % input.text_sc
        msg += "\nTokenized: %s" % input.parsed
            
        resp = None
        
        desires = input.desires(self.intellect.last_question)
        
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
        else:
            self.intellect.clear_last_question()
            
        print(msg)  # Only for testing purposes
        return 1, resp  # trust, response



class InsultsAgent:
    def evaluate(self, input):
        return 0, Response(Response.UNKNOWN_INPUT)  # trust, response
