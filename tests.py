#!/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from resources import UserInput
from collections import OrderedDict
from utils import spellchecker


class UserInputTestCase(unittest.TestCase):

    def tests(self):

        # Test text tagging
        i_tag1 = u'hola, quiero una habitación'
        o_tag1 = OrderedDict([(u'hol', 'np'), (u'quier', 'vm'), (u'una', 'di'), (u'habitacion', 'nc')])

        i_tag2 = u'hola, quiero una habitacion'
        o_tag2 = OrderedDict([(u'hol', 'np'), (u'quier', 'vm'), (u'una', 'di'), (u'habitacion', 'nc')])

        self._test_tagging(i_tag1, o_tag1)
        self._test_tagging(i_tag2, o_tag2)

        # Test goal generation
        # ...

    # Test for tagging (when it's tagger all the proccess has been done
    def _test_tagging(self, text, res):
        input = UserInput(text)
        print(input.tagged)
        self.assertEqual(input.tagged, res)


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