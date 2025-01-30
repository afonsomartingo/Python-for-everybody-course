'''Musical Track Database
This application will read an iTunes export file in CSV format and produce a properly normalized database with this structure:

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
If you run the program multiple times in testing or with different files, make sure to empty out the data before each run.

You can use this code as a starting point for your application: http://www.py4e.com/code3/tracks.zip. The ZIP file contains the tracks.csv file to be used for this assignment. You can export your own tracks from iTunes and create a database, but for the database that you turn in for this assignment, only use the tracks.csv data that is provided. You can adapt the tracks_csv.py application in the zip file to complete the assignment.

To grade this assignment, the program will run a query like this on your uploaded database and look for the data it expects to see:

SELECT Track.title, Artist.name, Album.title, Genre.name 
    FROM Track JOIN Genre JOIN Album JOIN Artist 
    ON Track.genre_id = Genre.ID and Track.album_id = Album.id 
        AND Album.artist_id = Artist.id
    ORDER BY Artist.name LIMIT 3'''

import sqlite3
import csv

# Connect to the database
conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Drop existing tables
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, 
    rating INTEGER, 
    count INTEGER
)
''')

# Open the CSV file
fname = 'tracks.csv'
with open(fname) as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    
    for row in reader:
        title = row[0]
        artist = row[1]
        album = row[2]
        genre = row[3]
        length = row[4]
        rating = row[5]
        count = row[6]

        # Insert or ignore Artist
        cur.execute('''INSERT OR IGNORE INTO Artist (name) 
            VALUES (?)''', (artist,))
        cur.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
        artist_id = cur.fetchone()[0]

        # Insert or ignore Genre
        cur.execute('''INSERT OR IGNORE INTO Genre (name) 
            VALUES (?)''', (genre,))
        cur.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
        genre_id = cur.fetchone()[0]

        # Insert or ignore Album
        cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
            VALUES (?, ?)''', (album, artist_id))
        cur.execute('SELECT id FROM Album WHERE title = ?', (album,))
        album_id = cur.fetchone()[0]

        # Insert Track
        cur.execute('''INSERT OR IGNORE INTO Track 
            (title, album_id, genre_id, len, rating, count) 
            VALUES (?, ?, ?, ?, ?, ?)''', 
            (title, album_id, genre_id, length, rating, count))

# Commit the changes
conn.commit()

# Test the database with the required query
cur.execute('''
SELECT Track.title, Artist.name, Album.title, Genre.name 
FROM Track JOIN Genre JOIN Album JOIN Artist 
    ON Track.genre_id = Genre.ID and Track.album_id = Album.id 
    AND Album.artist_id = Artist.id
ORDER BY Artist.name LIMIT 3''')

# Print results
for row in cur:
    print(row)

# Close the connection
cur.close()