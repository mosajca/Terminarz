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
        self.button = tk.Button(self, text='dodaj', command=self.addEvent)
        self.button.grid(row=1, column=4)

        self.table = ttk.Treeview(self)
        self.table['columns'] = \
            ('id', 'data', 'nazwa', 'kategoria', 'priorytet')
        self.table['show'] = 'headings'
        self.table.heading('id', text='id')
        self.table.heading('nazwa', text='nazwa')
        self.table.heading('data', text='data')
        self.table.heading('kategoria', text='kategoria')
        self.table.heading('priorytet', text='priorytet')
        self.table.grid(row=0, column=0, columnspan=9)
        self.getAll()

    def addEvent(self):
        window = tk.Toplevel()
        window.title("Dodaj wydarzenie")

        self.day = tk.Label(window, text='dzień')
        self.day.grid(row=0, column=0)

        self.dayVar = tk.StringVar()
        self.dayC = \
            ttk.Combobox(window, state='readonly', textvariable=self.dayVar)
        self.dayC['values'] = tuple([x for x in range(1, 32)])
        self.dayC.current(0)
        self.dayC.grid(row=0, column=1)

        self.month = tk.Label(window, text='miesiąc')
        self.month.grid(row=0, column=2)

        self.monthVar = tk.StringVar()
        self.monthC = \
            ttk.Combobox(window, state='readonly', textvariable=self.monthVar)
        self.monthC['values'] = tuple([x for x in range(1, 13)])
        self.monthC.current(0)
        self.monthC.grid(row=0, column=3)

        self.year = tk.Label(window, text='rok')
        self.year.grid(row=0, column=4)

        self.yearVar = tk.StringVar()
        self.yearC = \
            ttk.Combobox(window, state='readonly', textvariable=self.yearVar)
        self.yearC['values'] = tuple([x for x in range(2017, 2031)])
        self.yearC.current(0)
        self.yearC.grid(row=0, column=5)

        self.name = tk.Label(window, text='nazwa')
        self.name.grid(row=1, column=0)
        self.nameE = tk.Entry(window)
        self.nameE.grid(row=1, column=1)

        self.category = tk.Label(window, text='kategoria')
        self.category.grid(row=1, column=2)
        self.categoryE = tk.Entry(window)
        self.categoryE.grid(row=1, column=3)

        self.priority = tk.Label(window, text='priorytet')
        self.priority.grid(row=1, column=4)

        self.priorityVar = tk.StringVar()
        self.priorityC = \
            ttk.Combobox(window, state='readonly',
                         textvariable=self.priorityVar)
        self.priorityC['values'] = tuple([x for x in range(1, 6)])
        self.priorityC.current(0)
        self.priorityC.grid(row=1, column=5)

        self.addB = tk.Button(window, text='dodaj', command=self.insert)
        self.addB.grid(row=2, column=5)

    def length2(self, value):
        if len(value) < 2:
            return '0'+value
        else:
            return value

    def insert(self):
        date = '-'.join([self.yearC.get(), self.length2(self.monthC.get()),
                        self.length2(self.dayC.get())])
        self.events.add(date, self.nameE.get(),
                        self.categoryE.get(), self.priorityC.get())
        self.table.delete(*self.table.get_children())
        self.getAll()

    def getAll(self):
        self.listOfEvents = self.events.selectAll()
        for event in self.listOfEvents:
            self.table.insert('', 'end', values=event)

    def close(self):
        self.events.close()
        self.parent.destroy()

root = tk.Tk()
program = Program(root)
root.mainloop()
