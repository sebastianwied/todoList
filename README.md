# How to use!
## Setup
Clone this into a directory youd like it to be in. You need python. If on mac, curses should be installed with python. If on windows, run "pip install windows-curses". Run app.py with python and you should be good! All the data is stored in savedData.json.

## Entering text and using buttons
Press on the empty boxes next to labels to enter text. The cursor should appear there. Enter the text you want and then press "ctrl" and "g" to exit. Then press the respective button

## Error handling
Right now there is pretty much no error handling or input checking. If you enter something malformed, it will crash. The tasks are saved every time the task window is changed, but be careful. 
Try to be nice when entering things :). The format for a date goes as follows: year month day. June 21, 2025 is entered as "2025 5 21" or "2025 05 21". Leading zeros don't matter.

## Creating regular tasks:
Enter a name, description, and due date (if no due date selected it just defaults to 1/1/3000 to prevent it from going overdue)
Press the "Create Task" button!

## Creating a recurring task:
Enter a name and description just as before. Don't enter a due date. Enter a date to create it on(determines when it recurs), after how many days to recur, and after how many days to have it due.
Press the 'Create Recurring Task' button!

## Other features
### Completing a task:
Press on a task in the task window and press 'complete task'. It will turn blue. It's just cosmetic.
### Overdue tasks:
When the date passes the date a task is due, it will turn red. The red color takes less priority than the completed blue color.
### Deleting a task:
Press on a task in the task window and press the 'delete task' button. It will disappear forever!!
### Change date button:
This was just for debugging. Enter a date and press the "Current date" button and it will change "todays" date.
### Exiting:
When nothing is selected, press 'q'!
