#!/usr/bin/env python
# -*- coding: utf8 -*-

import pyowm
import pdb

class Weather:
    codes = {
        200: "Tormenta con lluvia ligera",
        201: "Tormenta con lluvia",
        202: "Tormenta con lluvia intensa",
        210: "Tormenta breve",
        211: "Tormenta",
        212: "Tormenta intensa",
        221: "Tormenta a intervalos",
        230: "Tormenta con llovizna ligera",
        231: "Tormenta con llovizna",
        232: "Tormenta con llovizna intensa",
        300: "Llovizna ligera",
        301: "Llovizna",
        302: "Llovizna intensa",
        310: "Llovizna ligera",
        311: "LLovizna",
        312: "LLovizna intensa",
        313: "Llovizna",
        314: "LLovizna intensa",
        321: "Llovizna",
        500: "Lluvia ligera",
        501: "Lluvia moderada",
        502: "Lluvia intensa",
        503: "Lluvia muy intensa",
        504: "Lluvia extremadamente intensa",
        511: "Lluvia helada",
        520: "Lluvia ligeramente intensa",
        521: "Aguacero",
        522: "Aguacero intenso",
        531: "Aguacero interminente",
        600: "Nevada ligera",
        601: "Nevada",
        602: "Nevada intensa",
        611: "Aguanieve",
        612: "Aguanieve intenso",
        615: "Aguanieve ligero",
        616: "Lluvia  y nieve",
        620: "Nieve ligera",
        621: "Nieve",
        622: "Nieve intensa",
        701: "Niebla",
        711: "Humo",
        721: "Calina",
        731: "Arena, remolinos de polvo",
        741: "Niebla",
        751: "Arena",
        761: "Polvo",
        762: "Ceniza volcánica",
        771: "Chubascos",
        781: "Tornado",
        800: "Cielo despejado",
        801: "Pocas nubes",
        802: "Nubes dispersas",
        803: "Nubes rotas",
        804: "Nublado",
        900: "Tornado",
        901: "Tormenta tropical",
        902: "Huracan",
        903: "Frio",
        904: "Calor",
        905: "Vendaval",
        906: "Granizo",
        951: "Tranquilo",
        952: "Brisa ligera",
        953: "Brisa suave",
        954: "Brisa moderada",
        955: "Brisa fresca",
        956: "Fuerte brisa",
        957: "Vendaval ligero",
        958: "Vendaval",
        959: "Vendaval intenso",
        960: "Tormenta",
        961: "Tormenta violenta",
        962: "Huracan"
    }

    def __init__(self, api_key):
        self.owm = pyowm.OWM(api_key)

    def get_current_weather(self, address):
        return self.owm.weather_at_place(address).get_weather()

    def get_daily_forecast(self, address):
        return self.owm.daily_forecast(address)

    def get_wind(self, address):
        return self.owm.weather_at_place(address).get_weather().get_wind()

    def get_humidity(self, address):
        return self.owm.weather_at_place(address).get_weather().get_humidity()

    def get_celsius_temperature(self, address):
        return self.owm.weather_at_place(address).get_weather().get_temperature('celsius')

    def get_fahrenheit_temperature(self, address):
        return self.owm.weather_at_place(address).get_weather().get_temperature('fahrenheit')

    def get_current_weather(self, lat, lon):
        return self.owm.weather_at_coords(lat,lon).get_weather()

    def get_daily_forecast(self, lat, lon):
        return self.owm.daily_forecast_at_coords(lat,lon)

    def get_wind(self, lat, lon):
        return self.owm.weather_at_coords(lat,lon).get_weather().get_wind()

    def get_humidity(self, lat, lon):
        return self.owm.weather_at_coords(lat,lon).get_weather().get_humidity()

    def get_celsius_temperature(self, lat, lon):
        return self.owm.weather_at_coords(lat,lon).get_weather().get_temperature('celsius')

    def get_fahrenheit_temperature(self, lat, lon):
        return self.owm.weather_at_coords(lat,lon).get_weather().get_temperature('fahrenheit')


