from cursesUtils import *
from TaskFunctionality import *
import curses as c
from datetime import date, timedelta

def drawTasks(todoList, taskWin, selectedLine):
    tasks = todoList.tasks

    taskWin.clear()
    ylim, xlim = taskWin.getmaxyx()
    textpad.rectangle(taskWin, 0, 0, ylim-2, xlim-2)
    yInfoTL = dict()
    yInfoSUB = dict()
    i = 1
    for task in tasks:
        label, attrs = task.label()
        cattr = 0
        if i-1 == selectedLine:
            attrs.append(c.A_STANDOUT)
        for attr in attrs: cattr |= attr
        taskWin.addstr(i, 1, label, cattr)
        yInfoTL[i-1] = task
        i += 1

        for child in task.children:
            label, attrs = child.label()
            cattr = 0
            if i-1 == selectedLine:
                attrs.append(c.A_STANDOUT)
            for attr in attrs: cattr |= attr
            taskWin.addstr(i, 4, label, cattr)
            yInfoSUB[i-1] = child
            i += 1

    return taskWin, yInfoTL, yInfoSUB

def setupTodoApp(stdscr, todoList, today):
    c.init_pair(1, c.COLOR_RED, c.COLOR_BLACK)
    c.init_pair(2, c.COLOR_BLUE, c.COLOR_BLACK)
    c.curs_set(0)
    c.mousemask(c.ALL_MOUSE_EVENTS)
    todoList.checkTasksDue(today, stdscr)

    windowManager = CursesObjectHandler(stdscr)

    label = f'Current date:'
    title, tl, bounds = createLabel(0, 0, label)
    windowManager.assign('dateInpLabel', 1, title, bounds, None, tl, rect=False)

    win, tl, tbox, bounds = createInputBox(0, len(label)+3, 3, 20, stdscr)
    windowManager.assign('dateInput', 1, win, bounds, tbox, tl)

    titleLabel = f'To-do List on date {today}'
    title, tl, _ = createLabel(0, (c.COLS//2)-(len(titleLabel)//2), titleLabel, rect=False)
    windowManager.assign('title', 1, title, None, None, tl)

    taskwin, tl, taskbounds = createBox(3, 0, 30, (c.COLS*2)//3)
    taskwin, yTL, ySUB = drawTasks(todoList, taskwin, -1)
    windowManager.assign('tasks', 1, taskwin, taskbounds, None, tl)
    
    label = 'New Task Name (ctrl+g to quit):'
    newTaskName, tl, _ = createLabel(3, ((c.COLS*5)//6)-(len(label)//2), label, rect=False)
    windowManager.assign('newTaskName', 1, newTaskName, None, None, tl)

    win, tl, tbox, bounds = createInputBox(6, (c.COLS*2)//3, 5, c.COLS//3, stdscr)
    windowManager.assign('newNameInput', 1, win, bounds, tbox, tl)

    label = 'New Task Description:'
    win, tl, _ = createLabel(11, ((c.COLS*5)//6)-(len(label)//2), label, rect=False)
    windowManager.assign('newTaskDesc', 1, win, None, None, tl)

    win, tl, tbox, bounds = createInputBox(14, ((c.COLS*2)//3), 5, c.COLS//3, stdscr)
    windowManager.assign('newDescInput', 1, win, bounds, tbox, tl)
    
    labelDue = 'Due Date:'
    win, tl, _ = createLabel(19, (c.COLS*2)//3 + 1, labelDue, rect=False)
    windowManager.assign('newTaskDue', 1, win, None, None, tl)

    win, tl, tbox, bounds = createInputBox(19, ((c.COLS*2)//3)+4+len(labelDue), 3, (c.COLS//3)-4-len(labelDue), stdscr)
    windowManager.assign('newDueInput', 1, win, bounds, tbox, tl)

    stdscr.hline(22, (c.COLS*2)//3, c.ACS_HLINE, c.COLS//3-1)

    labelCreateOn = 'Create Task On: (yyyy mm dd)'
    win, tl, _ = createLabel(23, (c.COLS*2)//3 + 1, labelCreateOn, rect=False)
    windowManager.assign('createOnLabel', 1, win, None, None, tl)

    win, tl, tbox, bounds = createInputBox(23, ((c.COLS*2)//3)+4+len(labelCreateOn), 3, (c.COLS//3)-4-len(labelCreateOn), stdscr)
    windowManager.assign('createOnInput', 1, win, bounds, tbox, tl)

    labelRecur = 'Recur every x days:'
    win, tl, _ = createLabel(26, (c.COLS*2)//3 + 1, labelRecur, rect=False)
    windowManager.assign('recurLabel', 1, win, None, None, tl)

    win, tl, tbox, bounds = createInputBox(26, ((c.COLS*2)//3)+4+len(labelRecur), 3, (c.COLS//3)-4-len(labelRecur), stdscr)
    windowManager.assign('recurInput', 1, win, bounds, tbox, tl)

    labelDueEvery = 'Due x days after:'
    win, tl, _ = createLabel(29, (c.COLS*2)//3 + 1, labelDueEvery, rect=False)
    windowManager.assign('dueEveryLabel', 1, win, None, None, tl)

    win, tl, tbox, bounds = createInputBox(29, ((c.COLS*2)//3)+4+len(labelDueEvery), 3, (c.COLS//3)-4-len(labelDueEvery), stdscr)
    windowManager.assign('dueEveryInput', 1, win, bounds, tbox, tl)

    label = 'Create New Recurring Task'
    win, tl, bounds = createLabel(33, (c.COLS*2)//3 + 1, label)
    windowManager.assign('newRecurringTaskButton', 1, win, bounds, None, tl)

    label = 'Create New Task'
    win, tl, bounds = createLabel(33, ((c.COLS*2)//3)-len(label)-4, label)
    windowManager.assign('newTaskButton', 1, win, bounds, None, tl)

    labelDel = 'Delete Selected Task'
    win, tl, bounds = createLabel(33, 4, labelDel)
    windowManager.assign('deleteButton', 1, win, bounds, None, tl)

    labelComplete = 'Complete Selected Task'
    win, tl, bounds = createLabel(33, 4+len(labelDel)+5, labelComplete)
    windowManager.assign('completeButton', 1, win, bounds, None, tl)

    return windowManager, yTL, ySUB

def mainLoop(stdscr, windowManager: CursesObjectHandler, todoList: ToDoList, yTL, ySUB, today):
    selected = -1
    changedTaskWin = False
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            todoList.saveTasks()
            break
        if key == c.KEY_MOUSE:
            mID, mx, my, _, mbstate = c.getmouse()
            clicked = windowManager.checkBounds(mx, my)
            # Clicked task window
            if clicked == 'tasks':

                # Select clicked task, and check if checkbox pressed
                ty, tx = windowManager.topleft[clicked]
                selected = my - ty - 1
                # checkbox locations are x == 1 and x == 4 for subtasks
                if (selected in yTL.keys()) and (mx-tx) == 1:
                    checked = yTL[selected]
                    checked.swapChecked()
                    index = todoList.tasks.index(checked)
                    todoList.tasks[index] = checked
                if (selected in ySUB.keys()) and (mx-tx) == 4:
                    checked = ySUB[selected]
                    checked.swapChecked()
                    parent = checked.parent
                    index = todoList.tasks.index(parent)
                    todoList.tasks[index] = parent
                # update
                changedTaskWin = True
            # Clicked input box
            if clicked in ['newNameInput', 'newDescInput', 'newDueInput', 'dateInput',
                            'createOnInput', 'recurInput', 'dueEveryInput']:
                ty, tx = windowManager.topleft[clicked]
                c.curs_set(1)
                stdscr.move(ty+1, tx+1)
                stdscr.refresh()
                windowManager.tboxes[clicked].edit()
                c.curs_set(0)
            if clicked == 'dateInpLabel':
                try:
                    currDate = windowManager.tboxes['dateInput'].gather().strip().split(' ')
                    today = date(*list(map(int,currDate)))
                    windowManager.windows['title'].addstr(1,1,f'To-do List on date {today}')
                    todoList.checkTasksDue(today, stdscr)
                except:
                    pass
                changedTaskWin = True
                windowManager.windows['dateInput'].clear()
            # Clicked buttons
            if clicked == 'newRecurringTaskButton':
                name = windowManager.tboxes['newNameInput'].gather().strip()
                desc = windowManager.tboxes['newDescInput'].gather().strip()
                createOn = windowManager.tboxes['createOnInput'].gather().strip()
                createOn = date(*map(int, createOn.split(' ')))
                recurSpacing = int(windowManager.tboxes['recurInput'].gather().strip())
                dueSpacing = int(windowManager.tboxes['dueEveryInput'].gather().strip())
                stdscr.addstr(41,0,f'{createOn}, {recurSpacing}, {dueSpacing}')
                if name != '' and desc != '':
                    newTask = TaskObject(name, desc)
                    newTask.setRecurring(createOn, recurSpacing, dueSpacing)
                    todoList.addTask(newTask)
                    windowManager.windows['newNameInput'].clear()
                    windowManager.windows['newDescInput'].clear()
                    windowManager.windows['createOnInput'].clear()
                    windowManager.windows['recurInput'].clear()
                    windowManager.windows['dueEveryInput'].clear()
                    changedTaskWin = True
                    selected = len(yTL) + len(ySUB)
            if clicked == 'newTaskButton':
                name = windowManager.tboxes['newNameInput'].gather().strip()
                desc = windowManager.tboxes['newDescInput'].gather().strip()
                due = windowManager.tboxes['newDueInput'].gather().strip()
                if name != '' and desc != '':
                    newTask = TaskObject(name, desc)
                    if due != '':
                        due = due.split(' ')
                        if len(due) == 3:
                            newTask.setDue(date(int(due[0]), int(due[1]), int(due[2])))
                            newTask.checkDue(today)
                    if selected in yTL.keys():
                        parent = yTL[selected]
                        index = todoList.tasks.index(parent)
                        parent.addSubtask(newTask)
                        todoList.tasks[index] = parent
                    elif selected in ySUB.keys():
                        parent = ySUB[selected].parent
                        index = todoList.tasks.index(parent)
                        parent.addSubtask(newTask)
                        todoList.tasks[index] = parent
                    else:
                        todoList.addTask(newTask)
                    windowManager.windows['newNameInput'].clear()
                    windowManager.windows['newDescInput'].clear()
                    windowManager.windows['newDueInput'].clear()
                    changedTaskWin = True
                    selected = len(yTL) + len(ySUB)
            if clicked == 'deleteButton':
                if selected in yTL.keys():
                    todoList.deleteTask(yTL[selected])
                if selected in ySUB.keys():
                    toDel = ySUB[selected]
                    parent = toDel.parent
                    parent.deleteSubtask(toDel)
                changedTaskWin = True
            if clicked == 'completeButton':
                if selected in yTL.keys():
                    completed = yTL[selected]
                    completed.swapCompleted()
                    index = todoList.tasks.index(completed)
                    todoList.tasks[index] = completed
                if selected in ySUB.keys():
                    completed = ySUB[selected]
                    completed.swapCompleted()
                    parent = completed.parent
                    index = todoList.tasks.index(parent)
                    todoList.tasks[index] = parent
        if changedTaskWin:
            todoList.checkTasksDue(today, stdscr)
            _, yTL, ySUB = drawTasks(todoList, windowManager.windows['tasks'], selected)
            todoList.saveTasks()

        windowManager.refreshWindows()
        c.doupdate()









