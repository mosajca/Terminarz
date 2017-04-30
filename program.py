import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import events


class ChoiceWidget(tk.Frame, object):

    def __init__(self, parent, name, values):
        tk.Frame.__init__(self, parent)
        self.config(borderwidth=3, relief=tk.GROOVE)

        self.label = tk.Label(self, text=name)
        self.label.pack()

        self.combobox = ttk.Combobox(self, state='readonly')
        self.combobox['values'] = values
        self.combobox['justify'] = 'center'
        self.combobox.current(0)
        self.combobox.pack()

    def setValues(self, values):
        self.combobox['values'] = values

    def setCurrent(self, index):
        self.combobox.current(index)

    def setBind(self, handler):
        self.combobox.bind("<<ComboboxSelected>>", handler)

    def getChoice(self):
        return self.combobox.get()


class InputWidget(tk.Frame, object):

    def __init__(self, parent, name):
        tk.Frame.__init__(self, parent)
        self.config(borderwidth=3, relief=tk.GROOVE)

        self.label = tk.Label(self, text=name)
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

    def setText(self, text):
        self.entry.delete(0, 'end')
        self.entry.insert(0, text)

    def getInput(self):
        return self.entry.get()


class EventInput(tk.Frame, object):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.numberOfDays = {2: 28, 4: 30, 6: 30, 9: 30, 11: 30}

        self.year = ChoiceWidget(self, 'rok',
                                 [str(x) for x in range(2017, 2031)])
        self.year.setBind(self.setFebruary)
        self.year.grid(row=0, column=0)

        self.month = ChoiceWidget(self, 'miesiąc',
                                  [str(x).zfill(2) for x in range(1, 13)])
        self.month.setBind(self.setNumberOfDays)
        self.month.grid(row=0, column=1)

        self.day = ChoiceWidget(self, 'dzień',
                                [str(x).zfill(2) for x in range(1, 32)])
        self.day.grid(row=0, column=2)

        self.hour = ChoiceWidget(self, 'godzina',
                                 [str(x).zfill(2) for x in range(24)])
        self.hour.grid(row=1, column=0)

        self.minute = ChoiceWidget(self, 'minuta',
                                   [str(x).zfill(2) for x in range(60)])
        self.minute.grid(row=1, column=1)

        self.priority = ChoiceWidget(self, 'priorytet',
                                     [x for x in range(1, 6)])
        self.priority.grid(row=1, column=2)

        self.name = InputWidget(self, 'nazwa')
        self.name.grid(row=2, column=0, sticky='ew')

        self.category = InputWidget(self, 'kategoria')
        self.category.grid(row=2, column=1, sticky='ew')

        self.button = tk.Button(self, borderwidth=3, relief=tk.GROOVE)
        self.button.grid(row=2, column=2, sticky='nsew')

        self.grid()

    def setValues(self, year, month, day, hour, minute,
                  priority, name, category):
        self.year.setCurrent(year)
        self.month.setCurrent(month)
        self.day.setCurrent(day)
        self.hour.setCurrent(hour)
        self.minute.setCurrent(minute)
        self.priority.setCurrent(priority)
        self.name.setText(name)
        self.category.setText(category)
        self.setFebruary()

    def setButton(self, textOnButton, callback):
        self.button.configure(text=textOnButton, command=callback)

    def setNumberOfDays(self, event=None):
        currentMonth = int(self.month.getChoice())
        currentMax = self.numberOfDays.get(currentMonth, 31)
        self.day.setValues([str(x).zfill(2) for x in range(1, currentMax + 1)])
        if int(self.day.getChoice()) > currentMax:
            self.day.setCurrent(currentMax - 1)

    def setFebruary(self, event=None):
        if self.isLeapYear(int(self.year.getChoice())):
            self.numberOfDays[2] = 29
            self.setNumberOfDays()
        else:
            self.numberOfDays[2] = 28
            self.setNumberOfDays()

    def isLeapYear(self, year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def getValues(self):
        date = '-'.join([self.year.getChoice(), self.month.getChoice(),
                        self.day.getChoice()])
        time = ':'.join([self.hour.getChoice(), self.minute.getChoice()])
        datetime = ' '.join([date, time])

        return (datetime, self.name.getInput(), self.category.getInput(),
                int(self.priority.getChoice()))


class Program(tk.Frame, object):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title('Terminarz')
        self.parent.iconphoto(self.parent, tk.PhotoImage(file='icon.png'))
        self.grid()
        self.events = events.Events()
        self.parent.protocol('WM_DELETE_WINDOW', self.close)
        self.addWindow = None
        self.modifyWindow = None
        self.gui()

    def gui(self):
        self.addButton = tk.Button(self, text='dodaj', command=self.addEvent)
        self.addButton.grid(row=0, column=10, sticky='ew')
        self.modifyButton = tk.Button(self, text='modyfikuj',
                                      command=self.modifyEvent)
        self.modifyButton.grid(row=1, column=10, sticky='ew')
        self.delButton = tk.Button(self, text='usuń', command=self.deleteEvent)
        self.delButton.grid(row=2, column=10, sticky='ew')

        self.table = ttk.Treeview(self)
        self.table['columns'] = \
            ('id', 'data i godzina', 'nazwa', 'kategoria', 'priorytet')
        self.table['show'] = 'headings'
        self.table['displaycolumns'] = \
            ('data i godzina', 'nazwa', 'kategoria', 'priorytet')
        self.table.heading('id', text='id')
        self.table.heading('nazwa', text='nazwa')
        self.table.heading('data i godzina', text='data i godzina')
        self.table.heading('kategoria', text='kategoria')
        self.table.heading('priorytet', text='priorytet')
        self.table.grid(row=0, column=0, rowspan=3, columnspan=9)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.configure(command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=9, rowspan=3, sticky='ns')

        self.getAll()

    def addEvent(self):
        if self.addWindow is None:
            self.addWindow = tk.Toplevel(self)
            self.addWindow.title("Dodaj wydarzenie")
            self.addWindow.protocol('WM_DELETE_WINDOW',
                                    self.addWindow.withdraw)
            self.add = EventInput(self.addWindow)
            self.add.setButton('dodaj',
                               lambda: self.insert(self.add.getValues()))
        else:
            self.add.setValues(0, 0, 0, 0, 0, 0, '', '')
            self.addWindow.deiconify()

    def modifyEvent(self):
        event = self.table.item(self.table.focus()).get('values')
        if(len(event) != 0):
            pPriority = event[4] - 1
            pCategory = event[3]
            pName = event[2]
            tmp = event[1].split('-')
            pMonth = int(tmp[1]) - 1
            tmp2 = tmp[2].split()
            pDay = int(tmp2[0]) - 1
            pYear = int(tmp[0]) - 2017
            tmp3 = tmp2[1].split(':')
            pHour = int(tmp3[0])
            pMinute = int(tmp3[1])
            eId = event[0]
        else:
            return

        if self.modifyWindow is None:
            self.modifyWindow = tk.Toplevel(self)
            self.modifyWindow.title("Modyfikuj wydarzenie")
            self.modifyWindow.protocol('WM_DELETE_WINDOW',
                                       self.modifyWindow.withdraw)
            self.modify = EventInput(self.modifyWindow)
            self.modify.setValues(pYear, pMonth, pDay, pHour, pMinute,
                                  pPriority, pName, pCategory)
            self.modify.setButton('zmień', lambda:
                                  self.update(eId, self.modify.getValues()))
        else:
            self.modify.setValues(pYear, pMonth, pDay, pHour, pMinute,
                                  pPriority, pName, pCategory)
            self.modify.setButton('zmień', lambda:
                                  self.update(eId, self.modify.getValues()))
            self.modifyWindow.deiconify()

    def deleteEvent(self):
        event = self.table.item(self.table.focus()).get('values')
        if len(event) != 0 and \
                msgbox.askyesno("Usuwanie wydarzenia",
                                "Czy na pewno usunąć zaznaczone wydarzenie?"):
            self.events.delete(event[0])
            self.table.delete(*self.table.get_children())
            self.getAll()

    def insert(self, values):
        self.events.add(*values)
        self.table.delete(*self.table.get_children())
        self.getAll()

    def update(self, eId, values):
        self.events.update(*values, eventId=eId)
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
