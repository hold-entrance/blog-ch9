# Make the initial database for soccer records
import sqlite3

with sqlite3.connect("soccer.db") as connection:
    c = connection.cursor()
    c.execute('CREATE TABLE soccer_stats (season TEXT, player TEXT, club TEXT, competition TEXT, goals INT, assists INT)')
    
