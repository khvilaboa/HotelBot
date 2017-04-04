#!/usr/bin/env python
# -*- coding: utf8 -*-

import pyowm


class Weather:
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
