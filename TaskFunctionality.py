import json
import curses as c
from datetime import date, timedelta
import calendar

class TaskObject:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.hasChildren = False
        self.children = []
        self.parent = None
        self.checked = False
        self.dueDate = date(3000,1,1)
        self.overdue = False
        self.completed = False
        self.recurring = False
        self.currentCreatedOn = 0

    def setRecurring(self, createOn, recurrenceFreq, dueDateSpacing):
        self.recurring = [createOn, recurrenceFreq, dueDateSpacing]
        self.setDue(createOn + timedelta(days=dueDateSpacing))
        self.currentCreatedOn = createOn

    def addSubtask(self, task):
        self.hasChildren = True
        self.children.append(task)
        task.setParent(self)

    def deleteSubtask(self, task):
        tasks = []
        for child in self.children:
            if child != task: tasks.append(child)
        self.children = tasks

    def swapChecked(self):
        self.checked = not self.checked
        return self.checked

    def swapCompleted(self):
        self.completed = not self.completed
        return self.completed

    def setParent(self, parent):
        self.parent = parent

    def setDue(self, date):
        self.dueDate = date

    def checkDue(self, date):
        self.overdue = date > self.dueDate
        return self.overdue

    def checkRecurring(self, today, stdscr):
        stdscr.addstr(40, 0, str(today))
        daysSinceDue = (today-self.dueDate)
        daysSinceCreated = (today-self.currentCreatedOn).days
        if daysSinceCreated >= self.recurring[1]:
            createNewOn = today-timedelta(days=(daysSinceCreated - (daysSinceCreated%self.recurring[1]) - self.recurring[1]))
            newDue = createNewOn+timedelta(days=self.recurring[2])
            self.setDue(newDue)
            self.currentCreatedOn = createNewOn
            self.completed = False
            self.checked = False

    def label(self):
        box = chr(int('0x2612',16)) if self.checked else chr(int('0x25A1',16))
        attrs = []
        if self.overdue: attrs = [c.color_pair(1)]
        if self.completed: attrs = [c.color_pair(2)]
        label = f'{box}  {self.name}: {self.desc}, due on {self.dueDate}'
        if self.recurring: label += f', recur on {self.currentCreatedOn + timedelta(days=self.recurring[1])}'
        return label, attrs

    def returnJson(self):
        if self.recurring == False:
            recur = False
        else:
            recur = [self.recurring[0].year,self.recurring[0].month,self.recurring[0].day,self.recurring[1],self.recurring[2]]
        return {'name':self.name,
                'desc':self.desc,
                'haschildren':self.hasChildren,
                'children':[task.returnJson() for task in self.children],
                'checked':self.checked,
                'completed':self.completed,
                'duedate':[self.dueDate.year, self.dueDate.month, self.dueDate.day],
                'recurring':recur,
                'currentCreatedOn':[self.currentCreatedOn.year,self.currentCreatedOn.month,self.currentCreatedOn.day]}

class ToDoList:
    def __init__(self):
        self.tasks = []

    def readTasks(self):
        with open('savedData.json', 'r') as data:
            tasks = list(json.loads(data.read()).values())
            for task in tasks:
                self.tasks.append(self.createTaskFromJson(task))

    def createTaskFromJson(self, entry):
        task = TaskObject(entry['name'], entry['desc'])
        task.checked = entry['checked']
        task.completed = entry['completed']
        duey, duem, dued = entry['duedate']
        task.setDue(date(duey, duem, dued))
        if entry['recurring'] != False:
            yr,mm,dd,recurFreq,dueEvery = entry['recurring']
            createdOn = entry['currentCreatedOn']
            createdOn = date(createdOn[0],createdOn[1],createdOn[2])
            task.recurring = [createdOn, recurFreq, dueEvery]
            task.currentCreatedOn = createdOn
        if entry['haschildren']:
            task.hasChildren = True
            for child in entry['children']:
                task.addSubtask(self.createTaskFromJson(child))
        return task

    def saveTasks(self):
        items = dict()
        counter = 0
        for task in self.tasks:
            items[counter] = task.returnJson()
            counter += 1
        with open('savedData.json', 'w') as file:
            json.dump(items, file)

    def addTask(self, task):
        self.tasks.append(task)

    def deleteTask(self, toDel):
        self.tasks.remove(toDel)

    def checkTasksDue(self, today,stdscr):
        for task in self.tasks:
            if task.recurring != False: task.checkRecurring(today, stdscr)
            task.checkDue(today)
            for child in task.children:
                if child.recurring != False: child.checkRecurring(today, stdscr)
                child.checkDue(today)





