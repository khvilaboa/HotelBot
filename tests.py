#!/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from collections import OrderedDict

from facts import Goal
from resources import UserInput
from utils import spellchecker


class UserInputTestCase(unittest.TestCase):
    def tests(self):

        # Test text tagging
        i_tag1 = u'hola, quiero una habitación individual'
        o_tag1 = OrderedDict(
            [(u'hol', 'np'), (u'quier', 'vm'), (u'una', 'di'), (u'habitacion', 'nc'), (u'individual', 'nc')])

        i_tag2 = u'me gustaría realizar una reserva, por favor'
        o_tag2 = OrderedDict(
            [(u'me', 'pp'), (u'gustari', 'vm'), (u'realiz', 'vm'), (u'una', 'di'), (u'reserv', 'nc'), (u'por', 'sp'),
             (u'favor', 'aq')])

        i_tag3 = u'mmmh.. me vlae con una individual (voy a estar solo)'
        o_tag3 = OrderedDict(
            [(u'mmmh', None), (u'me', 'pp'), (u'val', 'aq'), (u'con', 'sp'), (u'una', 'di'), (u'individual', 'nc'),
             (u'voy', 'vm'), (u'a', 'sp'), (u'estar', 'vm'), (u'sol', 'nc')])

        i_tag4 = u'pues.. creo qeu prefiero una doble.. lo siento por cambiar de opinión'
        o_tag4 = OrderedDict(
            [(u'pues', 'cs'), (u'cre', 'vm'), (u'que', 'pr'), (u'prefier', 'vm'), (u'una', 'di'), (u'dobl', 'aq'),
             (u'lo', 'pp'), (u'sient', 'vm'), (u'por', 'sp'), (u'cambi', 'vm'), (u'de', 'sp'), (u'opinion', 'nc')])

        i_tag5 = u'pues.. el 24 de enero me viene bien'
        o_tag5 = OrderedDict(
            [(u'pues', 'cs'), (u'el', 'pp'), (u'24012018', 'dt'), (u'me', 'pp'), (u'vien', 'vm'), (u'bien', 'rg')])

        i_tag6 = u'quiero estar en el hotel hasta el 7 de octubre'
        o_tag6 = OrderedDict(
            [(u'quier', 'vm'), (u'estar', 'vm'), (u'en', 'sp'), (u'el', 'pp'), (u'hotel', 'nc'), (u'hast', 'rg'),
             (u'07102017', 'dt')])

        i_tag7 = u'quiero salir del hotel pasado mañana'
        o_tag7 = OrderedDict(
            [(u'quier', 'vm'), (u'sal', 'vm'), (u'del', 'sp'), (u'hotel', 'nc'), (u'pas', 'vm'), (u'manan', 'nc')])

        i_tag8 = u'solo quiero el desayuno, ya comeré fuera en algún sitio'
        o_tag8 = OrderedDict(
            [(u'sol', 'nc'), (u'quier', 'vm'), (u'el', 'pp'), (u'desayun', 'vm'), (u'ya', 'rg'), (u'comer', 'vm'),
             (u'fuer', 'vs'), (u'en', 'sp'), (u'algun', 'di'), (u'siti', 'nc')])

        i_tag9 = u'no estoy interesado en ninguno de esos servicios'
        o_tag9 = OrderedDict(
            [(u'no', 'rn'), (u'estoy', 'vm'), (u'interes', 'aq'), (u'en', 'sp'), (u'ningun', 'di'), (u'de', 'sp'),
             (u'esos', 'dd'), (u'servici', 'nc')])

        i_tag10 = u'si, quisiera disponer de aparcamiento'
        o_tag10 = OrderedDict([(u'sic', 'np'), (u'quis', 'vm'), (u'dispon', 'vm'), (u'de', 'sp'), (u'abarc', 'vm')])

        i_tag11 = u'una cama adicional no me vendría mal'
        o_tag11 = OrderedDict(
            [(u'una', 'di'), (u'cam', 'nc'), (u'adicional', 'rg'), (u'no', 'rn'), (u'me', 'pp'), (u'vendri', 'vm'),
             (u'mal', 'aq')])

        i_tag12 = u'esa información es falsa'
        o_tag12 = OrderedDict([(u'esa', 'dd'), (u'informacion', 'nc'), (u'es', 'vs'), (u'fals', 'vm')])

        i_tag13 = u'eso no es correcto'
        o_tag13 = OrderedDict([(u'eso', 'pd'), (u'no', 'rn'), (u'es', 'vs'), (u'correct', 'rg')])

        i_tag14 = u'me parece bien'
        o_tag14 = OrderedDict([(u'me', 'pp'), (u'parec', 'vm'), (u'bien', 'rg')])

        i_tag15 = u'mi correo es eresunbot@gmail.com'
        o_tag15 = OrderedDict([(u'mi', 'dp'), (u'corre', 'nc'), (u'es', 'vs'),
                               (u'eresunbotgmailcom', None)])  # the email extraction is done by the mails() method

        i_tag16 = u'muy bien, hasta la proxima!! :)'
        o_tag16 = OrderedDict([(u'muy', 'rg'), (u'bien', 'rg'), (u'hast', 'rg'), (u'la', 'da'), (u'proxim', 'rg')])

        self._test_tagging(i_tag1, o_tag1)
        self._test_tagging(i_tag2, o_tag2)
        self._test_tagging(i_tag3, o_tag3)
        self._test_tagging(i_tag4, o_tag4)
        self._test_tagging(i_tag5, o_tag5)
        self._test_tagging(i_tag6, o_tag6)
        self._test_tagging(i_tag7, o_tag7)
        self._test_tagging(i_tag8, o_tag8)
        self._test_tagging(i_tag9, o_tag9)
        self._test_tagging(i_tag1, o_tag1)
        self._test_tagging(i_tag11, o_tag11)
        self._test_tagging(i_tag12, o_tag12)
        self._test_tagging(i_tag13, o_tag13)
        self._test_tagging(i_tag14, o_tag14)
        self._test_tagging(i_tag15, o_tag15)
        self._test_tagging(i_tag16, o_tag16)

        # Test languages
        i_lang1 = u'hola, quiero una habitación individual'
        i_lang2 = u'tienes una pizza?'
        i_lang3 = u'dame la habitación grande'
        i_lang4 = u'no la quiero para ese dia'
        i_lang5 = u'porqué no me saludas todos los días?'
        i_lang6 = u'es un viaje de trabajo'
        i_lang7 = u'me da igual, dormiré debajo de la cama :S'
        i_lang8 = u'no la quiero para ese dia'
        o_lang_es = 'es'

        i_lang9 = u'where I am?'
        i_lang10 = u'i\'m bored, tell me something'
        i_lang11 = u'do you talk in english?'
        i_lang12 = u'my email is the following:'
        o_lang_en = 'en'

        i_lang13 = u'Ich möchte eine Reservierung vornehmen'
        i_lang14 = u'keine Parkplätze gibt?'
        i_lang15 = u'Nichts mehr, dank'
        o_lang_de = 'de'

        i_lang16 = u'Niente di più, grazie'
        i_lang17 = u'Mi piace fare molto male'
        i_lang18 = u'buon giorno, si ha a disposizione una camera singola?'
        o_lang_it = 'it'

        self._test_language(i_lang1, o_lang_es)
        self._test_language(i_lang2, o_lang_es)
        self._test_language(i_lang3, o_lang_es)
        self._test_language(i_lang4, o_lang_es)
        self._test_language(i_lang5, o_lang_es)
        self._test_language(i_lang6, o_lang_es)
        self._test_language(i_lang7, o_lang_es)
        self._test_language(i_lang8, o_lang_es)

        self._test_language(i_lang9, o_lang_en)
        self._test_language(i_lang10, o_lang_en)
        self._test_language(i_lang11, o_lang_en)
        self._test_language(i_lang12, o_lang_en)

        self._test_language(i_lang13, o_lang_de)
        self._test_language(i_lang14, o_lang_de)
        self._test_language(i_lang15, o_lang_de)

        self._test_language(i_lang16, o_lang_it)
        self._test_language(i_lang17, o_lang_it)
        self._test_language(i_lang18, o_lang_it)

        # Test goal generation
        i_goals1 = u'Solo pasaba por aquí'
        o_goals1 = None

        i_goals2 = u'Quiero una habitación'
        o_goals2 = [Goal.WANT_ROOM]

        i_goals3 = u'buenos días'
        o_goals3 = [Goal.GREET_USER]

        i_goals4 = u'saludos, quiero una habitación'
        o_goals4 = [Goal.GREET_USER, Goal.WANT_ROOM]

        self._test_goals(i_goals1, o_goals1)
        self._test_goals(i_goals2, o_goals2)
        self._test_goals(i_goals3, o_goals3)
        self._test_goals(i_goals4, o_goals4)

    # Test for tagging (when it's tagger all the proccess has been done
    def _test_tagging(self, text, res):
        input = UserInput(text)
        self.assertEqual(input.tagged, res)

    # Test for tagging (when it's tagger all the proccess has been done
    def _test_language(self, text, lang):
        input = UserInput(text)
        self.assertEqual(input.lang, lang)

    # Test for tagging (when it's tagger all the proccess has been done
    def _test_goals(self, text, goals):
        input_goals = UserInput(text).goals()
        if input_goals is None and goals is None:
            return

        self.assertIsNotNone(input_goals)
        self.assertIsNotNone(goals)

        input_goals = map(lambda x: x.id, input_goals)

        for goal in input_goals:
            self.assertIn(goal, goals)


class SpellCheckerTestCase(unittest.TestCase):
    def tests(self):
        # Test edits1(word): All edits that are one edit away from `word`.

        i_word1_edits = 'hoal'
        o_word1_edits = 'hola'
        self.assertIn(o_word1_edits, spellchecker.edits1(i_word1_edits))

        i_word2_edits = 'abitacion'
        o_word2_edits = 'habitacion'
        self.assertIn(o_word2_edits, spellchecker.edits1(i_word2_edits))

        i_word3_edits = 'saluds'
        o_word3_edits = ['saludos', 'saludo']
        self.assertTrue(set(o_word3_edits) <= spellchecker.edits1(i_word3_edits))

        i_word4_edits = 'canta'
        o_word4_edits = ['cantas', 'cantar', 'canto']
        self.assertTrue(set(o_word4_edits) <= spellchecker.edits1(i_word4_edits))

        i_word5_edits = 'dicembre'
        o_word5_edits = 'diciembre'
        self.assertIn(o_word5_edits, spellchecker.edits1(i_word5_edits))

        # Test known(words): "The subset of `words` that appear in the dictionary of WORDS."

        i_words1_known = ['hola', 'ola', 'hloa', 'hoal']
        o_words1_known = ['hola', 'ola']
        self.assertEqual(set(o_words1_known), spellchecker.known(i_words1_known))

        i_words2_known = ['habitacion', 'abitacion', 'havitacion', 'agitacion']
        o_words2_known = ['habitacion', 'agitacion']
        self.assertEqual(set(o_words2_known), spellchecker.known(i_words2_known))

        i_words3_known = ['saludos', 'saludo', 'salidos', 'slaudos', 'saluds']
        o_words3_known = ['saludos', 'saludo', 'salidos']
        self.assertEqual(set(o_words3_known), spellchecker.known(i_words3_known))

        i_words4_known = ['reserva', 'reserba', 'reservs', 'reservado', 'rservar', 'reservar']
        o_words4_known = ['reserva', 'reservado', 'reservar']
        self.assertEqual(set(o_words4_known), spellchecker.known(i_words4_known))

        i_words5_known = ['enero', 'febrero', 'marzo', 'april', 'mallo', 'junio', 'julio']
        o_words5_known = ['enero', 'febrero', 'marzo', 'junio', 'julio']
        self.assertEqual(set(o_words5_known), spellchecker.known(i_words5_known))

        # Test candidates(word): "Generate possible spelling corrections for word."

        i_word1_candidates = 'hoal'
        o_word1_candidates = 'hola'
        self.assertIn(o_word1_candidates, spellchecker.candidates(i_word1_candidates))

        i_word2_candidates = 'abitacion'
        o_word2_candidates = ['habitacion', 'agitacion']
        self.assertTrue(set(o_word2_candidates) <= spellchecker.candidates(i_word2_candidates))

        i_word3_candidates = 'saluds'
        o_word3_candidates = ['saludo', 'saluda', 'saludes', 'salude', 'saludas', 'saludos', 'salud']
        self.assertTrue(set(o_word3_candidates) <= spellchecker.candidates(i_word3_candidates))

        i_word4_candidates = 'reserba'
        o_word4_candidates = 'reserva'
        self.assertIn(o_word4_candidates, spellchecker.candidates(i_word4_candidates))

        i_word5_candidates = 'agostoo'
        o_word5_candidates = ['agosto', 'agostos']
        self.assertTrue(set(o_word5_candidates) <= spellchecker.candidates(i_word5_candidates))

        # Test correction(word): "Most probable spelling correction for word."

        i_word1_correction = 'hoal'
        o_word1_correction = 'hola'
        self.assertEqual(o_word1_correction, spellchecker.correction(i_word1_correction))

        i_word2_correction = 'havitacion'
        o_word2_correction = 'habitacion'
        self.assertEqual(o_word2_correction, spellchecker.correction(i_word2_correction))

        i_word3_correction = 'sludos'
        o_word3_correction = 'saludos'
        self.assertEqual(o_word3_correction, spellchecker.correction(i_word3_correction))

        i_word4_correction = 'reserv'
        o_word4_correction = 'reserva'
        self.assertEqual(o_word4_correction, spellchecker.correction(i_word4_correction))

        i_word5_correction = 'semama'
        o_word5_correction = 'semana'
        self.assertEqual(o_word5_correction, spellchecker.correction(i_word5_correction))


class DateParserTestCase(unittest.TestCase):
    def tests(self):
        pass


if __name__ == '__main__':
    unittest.main()
