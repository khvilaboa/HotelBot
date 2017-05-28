#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
from datetime import datetime, timedelta

numbers = "un|uno|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|trece|catorce|quince|dieciseis|diecisiete|dieciocho|diecinueve|veinte|veintiuno|veintidos|veintitres|veinticuatro|veinticinco|veintiseis|veintisiete|veintiocho|veintinueve|treinta y uno"

days = "lunes|martes|miercoles|jueves|viernes|sabado|domingo"

months = "enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre"

rel_days = "anteayer|ayer|pasado manana|manana"

measures = "dia|semana|mes|ano"

regex1 = re.compile("((%s|[0-9]+)\s+al\s+(%s|[0-9]+)\s+de\s+(%s))" % (numbers, numbers, months), re.IGNORECASE)
regex2 = re.compile("((%s|[0-9]+)\s+de\s+(%s))" % (numbers, months), re.IGNORECASE)
# regex2 = re.compile("(([0-9]+)\s+de\s+(%s))" % (months), re.IGNORECASE)
regex3 = re.compile("((dentro\s+de|en)\s+(%s|[0-9]+)s?\s+(%s)s?)" % (numbers, measures), re.IGNORECASE)
regex4 = re.compile("((el|la)\s+(%s)\s+que\s+viene)" % measures, re.IGNORECASE)

numbersLst = numbers.split("|")
daysLst = days.split("|")
monthsLst = months.split("|")
rel_daysLst = rel_days.split("|")
measuresLst = measures.split("|")
mesuresValuesLst = [1, 2, 30, 365]


def parse(text):
    now = datetime.now()
    # pdb.set_trace()

    matches = regex1.findall(text)
    for data in matches:
        match, numberStart, numberEnd, month = data
        numberStart = max(1, numbersLst.index(numberStart) - 1) if numberStart in numbersLst else int(numberStart)
        numberEnd = max(1, numbersLst.index(numberEnd) - 1) if numberEnd in numbersLst else int(numberEnd)
        month = monthsLst.index(month) + 1
        newStart = datetime(now.year, month, numberStart)
        newEnd = datetime(now.year, month, numberEnd)
        if newStart < now:
            newStart = newStart.replace(year=newStart.year + 1)
        if newEnd < now:
            newEnd = newEnd.replace(year=newEnd.year + 1)
        text = text.replace(match, "%s al %s" % (newStart.strftime("%d/%m/%Y"), newEnd.strftime("%d/%m/%Y")))

    matches = regex2.findall(text)
    for data in matches:
        match, number, month = data
        number = max(1, numbersLst.index(number) - 1) if number in numbersLst else int(number)
        month = monthsLst.index(month) + 1
        new = datetime(now.year, month, number)
        if new < now:
            new = new.replace(year=new.year + 1)
        text = text.replace(match, new.strftime("%d/%m/%Y"))

    matches = regex3.findall(text)
    for data in matches:
        match, _, number, measure = data
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
        elif measure == "ano":
            new = now.replace(year=now.year + number)
        text = text.replace(match, "el %s" % new.strftime("%d/%m/%Y"))

    matches = regex4.findall(text)
    for data in matches:
        match, _, measure = data
        new = now
        if measure == "dia":
            new += timedelta(days=1)
        elif measure == "semana":
            new += timedelta(days=7)
        elif measure == "mes":
            if now.month <= 11:
                new = now.replace(month=now.month + 1)
            else:
                new = now.replace(year=now.year + 1)
                new = now.replace(month=1)
        elif measure == "ano":
            new = now.replace(year=now.year + 1)
        text = text.replace(match, "el %s" % new.strftime("%d/%m/%Y"))

    for rel_day in rel_daysLst:
        if rel_day in text:
            new = now
            if rel_day == "ayer":
                new -= timedelta(days=1)
            elif rel_day == "anteayer":
                new -= timedelta(days=2)
            elif rel_day == "manana":
                new += timedelta(days=1)
            elif rel_day == "pasado manana":
                new += timedelta(days=2)
            text = text.replace(rel_day, "el %s" % new.strftime("%d/%m/%Y"))

    return text


if __name__ == "__main__":
    pass
