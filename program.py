#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import calendar
import datetime
import events


class ChoiceWidget(tk.Frame, object):

    def __init__(self, parent, name, values):
        super().__init__(parent)
        self.config(borderwidth=3, relief=tk.GROOVE)
        tk.Label(self, text=name).pack()

        self.combobox = ttk.Combobox(self, state='readonly')
        self.combobox['values'] = values
        self.combobox['justify'] = 'center'
        self.combobox.current(0)
        self.combobox.pack(pady=(0, 2))

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
        super().__init__(parent)
        self.config(borderwidth=3, relief=tk.GROOVE)
        tk.Label(self, text=name).pack()

        self.entry = tk.Entry(self)
        self.entry.pack(pady=(0, 2))

    def setText(self, text):
        self.entry.delete(0, 'end')
        self.entry.insert(0, text)

    def getInput(self):
        return self.entry.get()


class EventInput(tk.Frame, object):

    def __init__(self, parent):
        super().__init__(parent)
        self.numberOfDays = {2: 28, 4: 30, 6: 30, 9: 30, 11: 30}

        self.year = ChoiceWidget(self, 'rok',
                                 [str(x) for x in range(2001, 2101)])
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

        self.duration = ChoiceWidget(self, 'czas trwania (min)',
                                     [x for x in range(1441)])
        self.duration.grid(row=1, column=2)

        self.priority = ChoiceWidget(self, 'priorytet',
                                     [x for x in range(1, 6)])
        self.priority.grid(row=2, column=2)

        self.name = InputWidget(self, 'nazwa')
        self.name.grid(row=2, column=0, sticky='ew')

        self.category = InputWidget(self, 'kategoria')
        self.category.grid(row=2, column=1, sticky='ew')

        self.button = tk.Button(self, borderwidth=3, relief=tk.GROOVE)
        self.button.grid(row=3, column=0, columnspan=3, sticky='nsew')

    def setValues(self, year, month, day, hour, minute,
                  priority, name, category, duration):
        self.year.setCurrent(year)
        self.month.setCurrent(month)
        self.day.setCurrent(day)
        self.hour.setCurrent(hour)
        self.minute.setCurrent(minute)
        self.priority.setCurrent(priority)
        self.duration.setCurrent(duration)
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
        if calendar.isleap(int(self.year.getChoice())):
            self.numberOfDays[2] = 29
            self.setNumberOfDays()
        else:
            self.numberOfDays[2] = 28
            self.setNumberOfDays()

    def getValues(self):
        date = '-'.join([self.year.getChoice(), self.month.getChoice(),
                        self.day.getChoice()])
        time = ':'.join([self.hour.getChoice(), self.minute.getChoice()])
        datetime = ' '.join([date, time])

        return (datetime, self.name.getInput(), self.category.getInput(),
                int(self.priority.getChoice()), int(self.duration.getChoice()))


class ShowWidget(tk.Frame, object):

    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text='Pokaż wydarzenia:').grid(row=0, column=0)

        self.SQL = {
            1: '''SELECT * FROM events WHERE strftime("%j", date) = {} AND
                    strftime("%Y", date) = {} ORDER BY datetime(date)''',
            2: '''SELECT * FROM events WHERE strftime("%W", date) = {} AND
                    strftime("%Y", date) = {} ORDER BY datetime(date)''',
            3: '''SELECT * FROM events WHERE strftime("%m", date) = {} AND
                    strftime("%Y", date) = {} ORDER BY datetime(date)''',
            4: '''SELECT * FROM events WHERE strftime("%Y", date) = {}
                    ORDER BY datetime(date)''',
            5: '''SELECT * FROM events ORDER BY datetime(date)'''
        }

        self.var = tk.IntVar()
        self.query = tk.StringVar()

        self.thisDay = tk.Radiobutton(self, text='dzień',
                                      variable=self.var, value=1)
        self.thisDay.grid(row=0, column=1)

        tk.Radiobutton(self, text='tydzień', variable=self.var,
                       value=2).grid(row=0, column=2)
        tk.Radiobutton(self, text='miesiąc', variable=self.var,
                       value=3).grid(row=0, column=3)
        tk.Radiobutton(self, text='rok', variable=self.var,
                       value=4).grid(row=0, column=4)
        tk.Radiobutton(self, text='wszystkie', variable=self.var,
                       value=5).grid(row=0, column=5)

        self.var.trace('w', self.setQuery)

        self.prevEvents = tk.Button(self, text='poprzednie',
                                    command=lambda: self.setModifiedQuery(-1))
        self.prevEvents.grid(row=0, column=6, padx=(15, 5))
        self.nextEvents = tk.Button(self, text='następne'.center(10),
                                    command=lambda: self.setModifiedQuery(1))
        self.nextEvents.grid(row=0, column=7)

    def setQuery(self, *args):
        self.choice = self.var.get()
        currentDatetime = datetime.datetime.now()
        self.formatDict = {
            1: [repr(currentDatetime.strftime("%j")),
                repr(currentDatetime.strftime("%Y"))],
            2: [repr(currentDatetime.strftime("%W")),
                repr(currentDatetime.strftime("%Y"))],
            3: [repr(currentDatetime.strftime("%m")),
                repr(currentDatetime.strftime("%Y"))],
            4: [repr(currentDatetime.strftime("%Y"))]
        }

        if self.choice == 5:
            self.prevEvents['state'] = 'disabled'
            self.nextEvents['state'] = 'disabled'
            self.query.set(self.SQL[self.choice])
        else:
            self.prevEvents['state'] = 'normal'
            self.nextEvents['state'] = 'normal'
            self.lastValues = self.formatDict[self.choice]
            self.query.set(self.SQL[self.choice].
                           format(*self.formatDict[self.choice]))

    def setNewValues(self, v):
        if self.choice == 1:
            dayOfYear = int(eval(self.lastValues[0]))
            year = int(eval(self.lastValues[1]))
            lastDay = 366 if calendar.isleap(year) else 365
            if dayOfYear == 1 and v == -1:
                if year - 1 != 2000:
                    self.newValues = \
                        [repr(str(366 if calendar.isleap(year - 1) else 365)),
                         repr(str(year - 1))]
            elif dayOfYear == lastDay and v == 1:
                if year + 1 != 2101:
                    self.newValues = [repr('001'), repr(str(year + 1))]
            else:
                self.newValues = [repr(str(dayOfYear + v).zfill(3)),
                                  self.lastValues[1]]

        elif self.choice == 2:
            weekOfYear = int(eval(self.lastValues[0]))
            year = int(eval(self.lastValues[1]))
            firstWeek = int(datetime.datetime(year, 1, 1).strftime("%W"))
            lastWeek = int(datetime.datetime(year, 12, 31).strftime("%W"))
            if weekOfYear == firstWeek and v == -1:
                if year - 1 != 2000:
                    self.newValues = \
                        [repr(datetime.datetime(year - 1, 12, 31).
                         strftime("%W")), repr(str(year - 1))]
            elif weekOfYear == lastWeek and v == 1:
                if year + 1 != 2101:
                    self.newValues = \
                        [repr(datetime.datetime(year + 1, 1, 1).
                         strftime("%W").zfill(2)), repr(str(year + 1))]
            else:
                self.newValues = \
                    [repr(str(weekOfYear + v).zfill(2)), self.lastValues[1]]

        elif self.choice == 3:
            month = int(eval(self.lastValues[0]))
            year = int(eval(self.lastValues[1]))
            if month == 1 and v == -1:
                if year - 1 != 2000:
                    self.newValues = [repr('12'), repr(str(year - 1))]
            elif month == 12 and v == 1:
                if year + 1 != 2101:
                    self.newValues = [repr('01'), repr(str(year + 1))]
            else:
                self.newValues = \
                    [repr(str(month + v).zfill(2)), self.lastValues[1]]

        elif self.choice == 4:
            year = int(eval(self.lastValues[0]))
            newYear = year + v
            if newYear > 2000 and newYear < 2101:
                self.newValues = [repr(str(newYear))]

    def setModifiedQuery(self, x):
        self.setNewValues(x)
        for i, v in enumerate(self.newValues):
            self.lastValues[i] = v
        self.query.set(self.SQL[self.choice].format(*self.newValues))

    def start(self):
        self.thisDay.select()

    def getQuery(self):
        return self.query


class Program(tk.Frame, object):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.title('Terminarz')
        self.parent.iconphoto(self.parent, tk.PhotoImage(file='icon.png'))
        self.grid()
        self.events = events.Events()
        self.parent.protocol('WM_DELETE_WINDOW', self.close)
        self.addWindow = None
        self.modifyWindow = None
        self.prevColumn = ''
        self.prevPrevColumn = ''
        self.gui()

    def gui(self):
        tk.Button(self, text='dodaj', command=self.addEvent). \
            grid(row=0, column=10, sticky='ew', padx=5)
        tk.Button(self, text='modyfikuj', command=self.modifyEvent). \
            grid(row=1, column=10, sticky='ew', padx=5)
        tk.Button(self, text='usuń', command=self.deleteEvent). \
            grid(row=2, column=10, sticky='ew', padx=5)
        tk.Button(self, text='usuń wszystkie', command=self.deleteAll). \
            grid(row=3, column=10, sticky='ew', padx=5)

        self.table = ttk.Treeview(self)
        self.table['columns'] = ('id', 'data i godzina', 'nazwa', 'kategoria',
                                 'priorytet', 'czas trwania (min)')
        self.table['show'] = 'headings'
        self.table['displaycolumns'] = ('data i godzina', 'czas trwania (min)',
                                        'nazwa', 'kategoria', 'priorytet')
        self.table.heading('id', text='id')
        self.table.heading('nazwa', text='nazwa',
                           command=lambda: self.executeSelect(column='name'))
        self.table.heading('data i godzina', text='data i godzina',
                           command=lambda:
                               self.executeSelect(column='datetime(date)'))
        self.table.heading('kategoria', text='kategoria',
                           command=lambda:
                               self.executeSelect(column='category'))
        self.table.heading('priorytet', text='priorytet',
                           command=lambda:
                               self.executeSelect(column='priority'))
        self.table.heading('czas trwania (min)', text='czas trwania (min)',
                           command=lambda:
                               self.executeSelect(column='duration'))
        self.table.column('priorytet', width=100)
        for name in ('data i godzina', 'nazwa', 'kategoria',
                     'priorytet', 'czas trwania (min)'):
            self.table.column(name, anchor=tk.CENTER)
        self.table.grid(row=0, column=0, rowspan=4, columnspan=9)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.configure(command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=9, rowspan=4, sticky='ns')

        self.show = ShowWidget(self)
        self.show.grid(row=4, column=0, columnspan=9, pady=5)
        self.query = self.show.getQuery()
        self.query.trace('w', self.executeSelect)
        self.show.start()

    def addEvent(self):
        currentTime = datetime.datetime.now()
        if self.addWindow is None:
            self.addWindow = tk.Toplevel(self)
            self.addWindow.title("Dodaj wydarzenie")
            self.addWindow.protocol('WM_DELETE_WINDOW',
                                    self.addWindow.withdraw)
            self.addWindow.resizable(tk.FALSE, tk.FALSE)
            self.add = EventInput(self.addWindow)
            self.add.grid()
            self.add.setButton('dodaj',
                               lambda: self.insert(self.add.getValues()))
        else:
            self.addWindow.deiconify()

        self.add.setValues(currentTime.year - 2001, currentTime.month - 1,
                           currentTime.day - 1, currentTime.hour,
                           currentTime.minute, 0, '', '', 0)

    def modifyEvent(self):
        event = self.table.item(self.table.focus()).get('values')
        if(len(event) != 0):
            prevPriority = event[4] - 1
            prevCategory = event[3]
            prevName = event[2]
            tmp = event[1].split('-')
            prevMonth = int(tmp[1]) - 1
            tmp2 = tmp[2].split()
            prevDay = int(tmp2[0]) - 1
            prevYear = int(tmp[0]) - 2001
            tmp3 = tmp2[1].split(':')
            prevHour = int(tmp3[0])
            prevMinute = int(tmp3[1])
            prevDuration = event[5]
            eId = event[0]
        else:
            return

        if self.modifyWindow is None:
            self.modifyWindow = tk.Toplevel(self)
            self.modifyWindow.title("Modyfikuj wydarzenie")
            self.modifyWindow.protocol('WM_DELETE_WINDOW',
                                       self.modifyWindow.withdraw)
            self.modifyWindow.resizable(tk.FALSE, tk.FALSE)
            self.modify = EventInput(self.modifyWindow)
            self.modify.grid()
        else:
            self.modifyWindow.deiconify()

        self.modify.setValues(prevYear, prevMonth, prevDay, prevHour,
                              prevMinute, prevPriority, prevName,
                              prevCategory, prevDuration)
        self.modify.setButton('zmień', lambda:
                              self.update(eId, self.modify.getValues()))

    def deleteEvent(self):
        event = self.table.item(self.table.focus()).get('values')
        if len(event) != 0 and \
                msgbox.askyesno("Usuwanie wydarzenia",
                                "Czy na pewno usunąć zaznaczone wydarzenie?"):
            self.events.delete(event[0])
            self.executeSelect()

    def deleteAll(self):
        if len(self.table.get_children()) != 0 and \
               msgbox.askyesno("Usuwanie wydarzeń",
                               "Czy na pewno usunąć wszystkie widoczne " +
                               "wydarzenia?"):
            query = 'DELETE FROM events' + self.query.get()[20:-23]
            self.events.execute(query, commit=True)
            self.executeSelect()

    def insert(self, values):
        self.events.insert(*values)
        self.executeSelect()

    def update(self, eId, values):
        self.events.update(*values, eventId=eId)
        self.executeSelect()

    def executeSelect(self, *args, column=None):
        self.table.delete(*self.table.get_children())
        query = self.query.get()
        if column is not None:
            query = query[:-14] + column
            if self.prevColumn == column and self.prevPrevColumn != column:
                query += ' DESC'
                self.prevPrevColumn = self.prevColumn
            else:
                self.prevPrevColumn = ''
            self.prevColumn = column
        self.listOfEvents = self.events.execute(query, fetchall=True)
        for event in self.listOfEvents:
            self.table.insert('', 'end', values=event)

    def close(self):
        self.events.close()
        self.parent.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    program = Program(root)
    root.mainloop()
