import appSetup as setup
import cursesUtils as cUtils
import TaskFunctionality as taskFuncs
import curses
from datetime import date, timedelta

def main(stdscr):
    todoList = taskFuncs.ToDoList()

    windowManager = setup.setupTodoApp(stdscr, todoList, date.today())

    setup.mainLoop(stdscr, windowManager, todoList, date.today())
   

curses.wrapper(main)
