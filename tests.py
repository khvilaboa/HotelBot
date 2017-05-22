#!/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from resources import UserInput
from collections import OrderedDict

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
        pass

class DateParserTestCase(unittest.TestCase):

    def tests(self):
        pass



if __name__ == '__main__':
    unittest.main()