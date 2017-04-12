#!/usr/bin/env python
# -*- coding: utf8 -*-
import datetime
import googlemaps


class Directions:
    def __init__(self, api_key):
        self.gmaps = googlemaps.Client(key=api_key)

    def geocode_address(self, address):
        """
        Geocoding is the process of converting addresses
        (like ``"1600 Amphitheatre Parkway, Mountain View, CA"``) into geographic
        coordinates (like latitude 37.423021 and longitude -122.083739), which you
        can use to place markers or position the map. 
        """
        geocode_result = self.gmaps.geocode(address)
        return geocode_result

    def reverse_geocoding(self, latitude, longitude):
        """
        Reverse geocoding is the process of converting geographic coordinates into a
        human-readable address.
        """
        reverse_geocode_result = self.gmaps.reverse_geocode((latitude, longitude))
        return reverse_geocode_result

    def get_driving_directions(self, from_address, to_address):
        now = datetime.now()
        directions_result = self.gmaps.directions(from_address,
                                                  to_address,
                                                  departure_time=now)
        return directions_result

    def get_walking_directions(self, from_address, to_address):
        now = datetime.now()
        directions_result = self.gmaps.directions(from_address,
                                                  to_address,
                                                  mode="walking",
                                                  departure_time=now)
        return directions_result

    def get_public_transit_directions(self, from_address, to_address):
        now = datetime.now()
        directions_result = self.gmaps.directions(from_address,
                                                  to_address,
                                                  mode="transit",
                                                  departure_time=now)
        return directions_result

    def get_bike_directions(self, from_address, to_address):
        now = datetime.now()
        directions_result = self.gmaps.directions(from_address,
                                                  to_address,
                                                  mode="bike",
                                                  departure_time=now)
        return directions_result

    def get_driving_directions(self, from_address, to_address, departure_time):
        directions_result = self.gmaps.directions(from_address,
                                                  to_address,
                                                  departure_time=departure_time)
        return directions_result

    def get_walking_directions(self, from_address, to_address, departure_time):
        directions_result = self.gmaps.directions(from_address,
                                                  to_address,
                                                  mode="walking",
                                                  departure_time=departure_time)
        return directions_result

    def get_public_transit_directions(self, from_address, to_address, departure_time):
        directions_result = self.gmaps.directions(from_address,
                                                  to_address,
                                                  mode="transit",
                                                  departure_time=departure_time)
        return directions_result

    def get_bike_directions(self, from_address, to_address, departure_time):
        directions_result = self.gmaps.directions(from_address,
                                                  to_address,
                                                  mode="bike",
                                                  departure_time=departure_time)
        return directions_result
