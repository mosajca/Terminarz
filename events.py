#!/usr/bin/env python3

import sqlite3


class Events(object):

    def __init__(self):
        self.database = 'database.db'
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''
                CREATE TABLE IF NOT EXISTS events(
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    name TEXT COLLATE NOCASE,
                    category TEXT COLLATE NOCASE,
                    priority INTEGER,
                    duration INTEGER
                )
            '''
        )
        self.connection.commit()

    def insert(self, date, name, category, priority, duration):
        self.cursor.execute(
            '''
                INSERT INTO events(date, name, category, priority, duration)
                VALUES (?, ?, ?, ?, ?)
            ''',
            (date, name, category, priority, duration)
        )
        self.connection.commit()

    def update(self, date, name, category, priority, duration, eventId):
        self.cursor.execute(
            '''
                UPDATE events
                SET date = ?,
                    name = ?,
                    category = ?,
                    priority = ?,
                    duration = ?
                WHERE id = ?
            ''',
            (date, name, category, priority, duration, eventId)
        )
        self.connection.commit()

    def delete(self, eventId):
        self.cursor.execute('DELETE FROM events WHERE id=?', (eventId,))
        self.connection.commit()

    def execute(self, query, fetchall=False, commit=False):
        self.cursor.execute(query)
        if commit:
            self.connection.commit()
        if fetchall:
            return self.cursor.fetchall()

    def close(self):
        self.connection.close()
