#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import re
from datetime import datetime, timedelta

numbers = "un|uno|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|quince|dieciseis|diecisiete|dieciocho|diecinueve|veinte|veintiuno|veintidos|veintitres|veinticuatro|veinticinco|veintiseis|veintisiete|veintiocho|veintinueve|treinta y uno"

days = "lunes|martes|miercoles|jueves|viernes|sabado|domingo"

months = "enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre"

rel_days = "ayer|anteayer|mañana|pasado mañana"

measures = "dia|semana|mes|año"

regex1 = re.compile("((%s|[0-9]+)\s+de\s+(%s))" % (numbers, months), re.IGNORECASE)
# regex2 = re.compile("(([0-9]+)\s+de\s+(%s))" % (months), re.IGNORECASE)
# regex3 = re.compile("(el|la)\s+(%s)\s+que\s+viene" % (measures), re.IGNORECASE)
regex2 = re.compile("(dentro\s+de\s+(%s|[0-9]+)s?\s+(%s)s?)" % (numbers, measures), re.IGNORECASE)

numbersLst = numbers.split("|")
daysLst = days.split("|")
monthsLst = months.split("|")
measuresLst = measures.split("|")
mesuresValuesLst = [1, 2, 30, 365]


def parse(text):
    now = datetime.now()
    # pdb.set_trace()

    matches = regex1.findall(text)
    for data in matches:
        match, number, month = data
        number = max(1, numbersLst.index(number) - 1) if number in numbersLst else int(number)
        month = monthsLst.index(month) + 1
        new = datetime(now.year, month, number)
        if new < now:
            new = new.replace(year=new.year + 1)
        text = text.replace(match, new.strftime("%d/%m/%Y"))

    matches = regex2.findall(text)
    for data in matches:
        match, number, measure = data
        number = max(1, numbersLst.index(number) - 1) if number in numbersLst else int(number)
        new = now
        if measure == "dia":
            new += timedelta(days=number)
        elif measure == "semana":
            new += timedelta(days=7 * number)
        elif measure == "mes":
            if number <= 12 - now.month:
                new = now.replace(month=now.month + number)
            else:
                number -= 12 - now.month - 1
                new = now.replace(year=now.year + 1 + number / 12)
                new = now.replace(month=1 + number - 12 * (number / 12))
        elif measure == "año":
            new = now.replace(year=now.year + number)
        text = text.replace(match, "el %s" % new.strftime("%d/%m/%Y"))

    return text


if __name__ == "__main__":
    pass
