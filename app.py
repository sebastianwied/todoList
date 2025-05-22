import appSetup as setup
import cursesUtils as cUtils
import TaskFunctionality as taskFuncs
import curses
from datetime import date, timedelta

def main(stdscr):
    todoList = taskFuncs.ToDoList()
    todoList.readTasks()

    windowManager, yTL, ySUB = setup.setupTodoApp(stdscr, todoList, date.today())
    
    windowManager.refreshWindows()

    setup.mainLoop(stdscr, windowManager, todoList, yTL, ySUB, date.today())
   

curses.wrapper(main)
