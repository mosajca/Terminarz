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
                    name TEXT,
                    category TEXT,
                    priority INTEGER
                )
            '''
        )
        self.connection.commit()

    def add(self, date, name, category, priority):
        self.cursor.execute(
            '''
                INSERT INTO events(date, name, category, priority)
                VALUES (?, ?, ?, ?)
            ''',
            (date, name, category, priority)
        )
        self.connection.commit()

    def update(self, date, name, category, priority, eventId):
        self.cursor.execute(
            '''
                UPDATE events
                SET date = ?,
                    name = ?,
                    category = ?,
                    priority = ?
                WHERE id = ?
            ''',
            (date, name, category, priority, eventId)
        )
        self.connection.commit()

    def delete(self, eventId):
        self.cursor.execute('DELETE FROM events WHERE id=?', (eventId,))
        self.connection.commit()

    def deleteAll(self):
        self.cursor.execute('DELETE FROM events')
        self.connection.commit()

    def selectAll(self):
        self.cursor.execute('SELECT * FROM events ORDER BY datetime(date)')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
