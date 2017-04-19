import os


class ToDoList(object):

    def __init__(self):
        self.toDoList = []
        self.toDoListFile = 'todo.txt'

    def save(self):
        with open(self.toDoListFile, 'w') as f:
            f.write('\n'.join(self.toDoList))

    def load(self):
        if os.path.isfile(self.toDoListFile):
            with open(self.toDoListFile) as f:
                self.toDoList = f.readlines()

    def delete(self, index):
        if index in range(len(self.toDoList)):
            del self.toDoList[index]

    def swap(self, index1, index2):
        index = index1 if index1 > index2 else index2
        if index in range(len(self.toDoList)):
            self.toDoList[index1], self.toDoList[index2] = \
                self.toDoList[index2], self.toDoList[index1]

    def add(self, text):
        self.toDoList.append(text)

    def clear(self):
        self.toDoList = []

    def get(self):
        return self.toDoList
