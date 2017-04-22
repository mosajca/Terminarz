import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import events


class Program(tk.Frame, object):

    def __init__(self, parent):
        super(Program, self).__init__(parent)
        self.parent = parent
        self.parent.title('Terminarz')
        self.parent.geometry('1015x300')
        self.grid()
        self.events = events.Events()
        self.numberOfDays = {2: 28, 4: 30, 6: 30, 9: 30, 11: 30}
        self.parent.protocol('WM_DELETE_WINDOW', self.close)
        self.gui()

    def gui(self):
        self.button = tk.Button(self, text='dodaj', command=self.addEvent)
        self.button.grid(row=1, column=3)
        self.delButton = tk.Button(self, text='usuń', command=self.deleteEvent)
        self.delButton.grid(row=1, column=4)

        self.table = ttk.Treeview(self)
        self.table['columns'] = \
            ('id', 'data i godzina', 'nazwa', 'kategoria', 'priorytet')
        self.table['show'] = 'headings'
        self.table.heading('id', text='id')
        self.table.heading('nazwa', text='nazwa')
        self.table.heading('data i godzina', text='data i godzina')
        self.table.heading('kategoria', text='kategoria')
        self.table.heading('priorytet', text='priorytet')
        self.table.grid(row=0, column=0, columnspan=9)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.configure(command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=10, sticky=tk.N+tk.S)

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
        self.monthC.bind("<<ComboboxSelected>>", self.setNumberOfDays)
        self.monthC.grid(row=0, column=3)

        self.year = tk.Label(window, text='rok')
        self.year.grid(row=0, column=4)

        self.yearVar = tk.StringVar()
        self.yearC = \
            ttk.Combobox(window, state='readonly', textvariable=self.yearVar)
        self.yearC['values'] = tuple([x for x in range(2017, 2031)])
        self.yearC.current(0)
        self.yearC.bind("<<ComboboxSelected>>", self.setFebruary)
        self.yearC.grid(row=0, column=5)

        self.hour = tk.Label(window, text='godzina')
        self.hour.grid(row=1, column=0)

        self.hourVar = tk.StringVar()
        self.hourC = \
            ttk.Combobox(window, state='readonly', textvariable=self.hourVar)
        self.hourC['values'] = tuple([self.length2(str(x)) for x in range(24)])
        self.hourC.current(0)
        self.hourC.grid(row=1, column=1)

        self.minute = tk.Label(window, text='minuta')
        self.minute.grid(row=1, column=2)

        self.minuteVar = tk.StringVar()
        self.minuteC = \
            ttk.Combobox(window, state='readonly', textvariable=self.minuteVar)
        self.minuteC['values'] = \
            tuple([self.length2(str(x)) for x in range(60)])
        self.minuteC.current(0)
        self.minuteC.grid(row=1, column=3)

        self.name = tk.Label(window, text='nazwa')
        self.name.grid(row=2, column=0)
        self.nameE = tk.Entry(window)
        self.nameE.grid(row=2, column=1)

        self.category = tk.Label(window, text='kategoria')
        self.category.grid(row=2, column=2)
        self.categoryE = tk.Entry(window)
        self.categoryE.grid(row=2, column=3)

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

    def deleteEvent(self):
        event = self.table.item(self.table.focus()).get('values')
        if len(event) != 0 and \
                msgbox.askyesno("Usuwanie wydarzenia",
                                "Czy na pewno usunąć zaznaczone wydarzenie?"):
            self.events.delete(event[0])
            self.table.delete(*self.table.get_children())
            self.getAll()

    def length2(self, value):
        if len(value) < 2:
            return '0' + value
        else:
            return value

    def setNumberOfDays(self, event=None):
        currentMonth = int(self.monthC.get())
        currentMax = self.numberOfDays.get(currentMonth, 31)
        self.dayC['values'] = tuple([x for x in range(1, currentMax + 1)])
        if int(self.dayC.get()) > currentMax:
            self.dayC.current(currentMax - 1)

    def setFebruary(self, event):
        currentYear = int(self.yearC.get())
        if (currentYear % 4 == 0 and currentYear % 100 != 0) or \
                (currentYear % 400 == 0):
            self.numberOfDays[2] = 29
            self.setNumberOfDays()
        else:
            self.numberOfDays[2] = 28
            self.setNumberOfDays()

    def insert(self):
        date = '-'.join([self.yearC.get(), self.length2(self.monthC.get()),
                        self.length2(self.dayC.get())])
        time = ':'.join([self.hourC.get(), self.minuteC.get()])
        datetime = ' '.join([date, time])
        self.events.add(datetime, self.nameE.get(),
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
