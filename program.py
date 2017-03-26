import tkinter as tk
import tkinter.ttk as ttk
import events

class Program(tk.Frame, object):
	
	def __init__(self, parent):
		super(Program, self).__init__(parent)
		self.parent = parent
		self.parent.title('Terminarz')
		self.parent.geometry('1000x300')
		self.grid()
		self.events = events.Events()
		self.parent.protocol('WM_DELETE_WINDOW', self.close)
		self.gui()
		
		
	def gui(self):
		self.label1 = tk.Label(self, text = 'data');
		self.label1.grid(row = 0, column = 0)
		self.entry1 = tk.Entry(self)
		self.entry1.grid(row = 0, column = 1)
		
		self.label2 = tk.Label(self, text = 'nazwa');
		self.label2.grid(row = 0, column = 2)
		self.entry2 = tk.Entry(self)
		self.entry2.grid(row = 0, column = 3)
		
		self.label3 = tk.Label(self, text = 'kategoria');
		self.label3.grid(row = 0, column = 4)
		self.entry3 = tk.Entry(self)
		self.entry3.grid(row = 0, column = 5)
		
		self.label4 = tk.Label(self, text = 'priorytet');
		self.label4.grid(row = 0, column = 6)
		self.entry4 = tk.Entry(self)
		self.entry4.grid(row = 0, column = 7)
		
		self.button1 = tk.Button(self, text = 'dodaj', command = self.insert)
		self.button1.grid(row = 0, column = 8)
		
		self.table = ttk.Treeview(self)
		self.table['columns'] = ('id', 'data', 'nazwa', 'kategoria', 'priorytet')
		self.table['show'] = 'headings'
		self.table.heading('id', text='id')
		self.table.heading('nazwa', text='nazwa')
		self.table.heading('data', text='data')
		self.table.heading('kategoria', text='kategoria')
		self.table.heading('priorytet', text='priorytet')
		self.table.grid(row = 1, column = 0, columnspan = 9)
		self.getAll()
		
		
	def insert(self):
		self.events.add(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.entry4.get())
		self.table.delete(*self.table.get_children())
		self.getAll()
		
		
	def getAll(self):
		self.listOfEvents = self.events.selectAll()
		for event in self.listOfEvents:
			self.table.insert('','end', values = event)
		
		
	def close(self):
		self.events.close()
		self.parent.destroy()
		
		
root = tk.Tk()
program = Program(root)
root.mainloop()
