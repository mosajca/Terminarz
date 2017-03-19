import sqlite3

class Events(object):
	
	def __init__(self):
		self.database = 'database.db'
		self.connection = sqlite3.connect(self.database)
		self.cursor = self.connection.cursor()
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS events
							(id INTEGER PRIMARY KEY, date TEXT, name TEXT, category TEXT, priority INTEGER)''')
		self.connection.commit()
		
							
	def add(self, date, name, category, priority):
		self.cursor.execute('INSERT INTO events(date, name, category, priority) VALUES (?, ?, ?, ?)',
							(date, name, category, priority))
		self.connection.commit()

	def delete(self, id):
		self.cursor.execute('DELETE FROM events WHERE id=?', (id,))
		self.connection.commit()
		
	def deleteAll(self):
		self.cursor.execute('DELETE FROM events')
		self.connection.commit()
		
	def selectAll(self):
		self.cursor.execute('SELECT * FROM events ORDER BY datetime(date)')
		return self.cursor.fetchall()

	def close(self):
		self.connection.close()
