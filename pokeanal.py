#!/usr/bin/env python

import os
import sqlite3 as lite

from pokemon import Pokemon
from constants import pokemon_names

con = None
pokemon_list = []

#
# If you have a Google Maps API key, put it in a file named google_maps_api_key.txt. This will
# ensure it gets populated in the html file properly. If you don't have one, the key string
# will not be included but the map should still load (maybe?).
#
key = ''
try:
    f = open('google_maps_api_key.txt', 'r')
    key = '?key={}'.format(f.readline())
    f.close()
except:
    pass

print '[+] Google Maps API Key string: {}'.format(key)

# Get the file names for all the database files in the directory.
db_names = []
dir_contents = os.listdir('./db/')
for dc in dir_contents:
    if '.db' in dc:
        db_names.append('db/{}'.format(dc))

# Connect to each database file and pull out the contents of the pokemon table.
for db in db_names:
    print '[+] Extracting data from {}'.format(db)
    con = lite.connect(db)

    with con:
        cur = con.cursor()
        cur.execute('SELECT `_rowid_`,* FROM `pokemon` ORDER BY `_rowid_` ASC;')
        rows = cur.fetchall()

        for row in rows:
            p = Pokemon(row)
            pokemon_list.append(p)

print '[+] Generating JSON data file containing {} pokemon sightings'.format(len(pokemon_list))

# Create the JSON file containing all the pokemon instances from the databases.
json = open('data.json', 'w')
json.write('var data = {{ "count": {},\n'.format(len(pokemon_list)))
json.write('"pokemon": [')

for p in pokemon_list:
    json.write('{{"pokemon_id": {}, "pokemon_name": "{}", "latitude": {}, "longitude": {}, "disappear_time": "{}"}},\n'.format(p.pokemon_id, pokemon_names[p.pokemon_id], p.location.lat, p.location.lon, p.disappear_time))

json.write(']}\n')
json.close()

print '[+] Generating HTML display file'

# Create an html string containing all the drop down box options for pokemon.
pid_options = ''
for p in sorted(pokemon_names):
    pid_options += '<option value="{}">{}</option>\n'.format(pokemon_names.index(p), p)

# Replace template placeholders with the correct data.
fc = ''
for line in open('display_template.html'):
    line = line.replace('%PID_OPTIONS%', '{}'.format(pid_options))
    line = line.replace('%COUNT%', '{}'.format(len(pokemon_list)))
    line = line.replace('%KEY%', key)
    fc += line

# Write out the display HTML file.
out_name = 'pokemon_display.html'
fout = open(out_name, 'w')
fout.write(fc)
fout.close()

print '[+] Completed'
print '\n[+] Open {} in your preferred browser'.format(out_name)
