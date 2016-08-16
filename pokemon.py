#!/usr/bin/env python

import LatLon
import dateutil.parser


class Pokemon:

    def __init__(self, s):
        self.encounter_id = s[1]
        self.spawnpoint_id = s[2]
        self.pokemon_id = s[3]

        self.location = LatLon.LatLon(float(s[4]), float(s[5]))
        # self.latitude = float(s[4])
        # self.longitude = float(s[5])
        self.disappear_time = dateutil.parser.parse(s[6])

    def __str__(self):
        s = '{}, {}, {}, {}, {}, {}'.format(self.encounter_id, self.spawnpoint_id, self.pokemon_id,
                                            self.location.lat, self.location.lon, self.disappear_time)
        return s
