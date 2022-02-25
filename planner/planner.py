from distutils.command.config import config
from hashlib import new
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from time import time, sleep
from calendar import *
import pandas as pd
from voiceRec import TaskContentVoiceRec
import re

root = Tk()
root.geometry("1480x900")
root.title("Planner")
root.resizable(width=False, height=False)

### POBIERANIE AKTUALNEJ DATY ###
def getCurrentDate():
    today = date.today()
    year = today.year
    monthv = today.month
    day = today.day
    monthName = today.strftime("%B")
    firstDayOfMonth = pd.Timestamp(f"{year}-{monthv}-1")
    firstDayOfMonth = firstDayOfMonth.day_name()

    numOfDays = monthrange(year, monthv)[1]

    getCurrentDateValues = [today, year, monthv, day, firstDayOfMonth, numOfDays, monthName]

    return getCurrentDateValues

getCurrentDateValues = getCurrentDate()
today = getCurrentDateValues[0]
firstDayOfMonth = getCurrentDateValues[4]
monthName = getCurrentDateValues[6]
year = getCurrentDateValues[1]
numOfDays = getCurrentDateValues[5]
monthv = getCurrentDateValues[2]
#-- POBIERANIE AKTUALNEJ DATY --#

def getDayTitle(filename):
    try:
        with open(f"title/#{filename}title#.txt", "r") as f:
            title = f.read()
            title = title[1:-1]
            return title
    except:
        title = ""

### RENDEROWANIE KALENDARZA ###
def renderCalendar(firstDayOfMonth, monthName, year, numOfDays, monthv, today):
    licznik = 0
    dayNames = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

    if firstDayOfMonth == "Monday":
        xMonthDay = 60   
    if firstDayOfMonth == "Tuesday":
        xMonthDay = 260
    if firstDayOfMonth == "Wednesday":
        xMonthDay = 460
    if firstDayOfMonth == "Thursday":
        xMonthDay = 660
    if firstDayOfMonth == "Friday":
        xMonthDay = 860  
    if firstDayOfMonth == "Saturday":
        xMonthDay = 1060
    if firstDayOfMonth == "Sunday":
        xMonthDay = 1260

    labelsList = []

    yMonthDay = 120
    xDayName = 60
    yDayName = 90

    strToday = str(today)

    actYear = strToday[0:4]
    actMonth = strToday[5:7]
    actDay = strToday[8:10]

    actYear = int(actYear)
    actMonth = int(actMonth)
    actDay = int(actDay)
    
    lMonthAnDYear = Label(root, text=f"{monthName} {year}", width=60, height=16, font='Helvetica 30 bold', anchor="n", borderwidth=1, relief="groove")
    lMonthAnDYear.place(x=20, y=20)
    for day in dayNames:                #renderowanie dni tygodnia
        lDayName = Label(root, text=day, width=20, font='Helvetica 10 bold')
        lDayName.place(x=xDayName, y=yDayName)
        xDayName += 200
    for i in range(int(numOfDays)):     #renderowanie przycisków
        licznik += 1
        i = Label(root, text=f"{i+1}", width=20, height=5, anchor="nw", padx=5, pady=8, font='Helvetica 10', borderwidth=1, relief="groove")
        i.place(x=xMonthDay, y=yMonthDay)
        i = Button(root, text=f"Dodaj", command=lambda m=licznik: NewWindow(year, monthv, m))
        i.place(x=xMonthDay+125, y=yMonthDay+5)

        ### przekształcanie daty ###
        dateMonth = monthv
        dateDay = licznik
        dateYear = year
        dateMonth = str(dateMonth)
        dateDay = str(dateDay)
        dateYear = str(dateYear)

        if len(dateMonth) == 1:
            dateMonth = f"0{dateMonth}"
            
        if len(dateDay) == 1:
            dateDay = f"0{dateDay}"

        date = f"{dateYear}-{dateMonth}-{dateDay}"

        tempDate = today
        tempDate = str(tempDate)
        #-- przekształcanie daty --#    

        title = getDayTitle(date)

        labelRenderTitle = Label(root, text=title, foreground = "blue", width=20, font='Helvetica 10')
        labelRenderTitle.place(x=xMonthDay+2, y=yMonthDay+40)

        if date == tempDate:
            labActDay = Label(root, text="Aktualny dzień", foreground = "red", width=20, padx = 5, font='Helvetica 10', borderwidth=1, relief="groove")
            labActDay.place(x=xMonthDay, y=yMonthDay+81)
        labelsList.append(i)
        xMonthDay += 200
        if xMonthDay == 1460:
            yMonthDay += 100
            xMonthDay = 60

    renderCalendarReturn = [labelsList, lMonthAnDYear]

    return renderCalendarReturn

renderCalendarReturn = renderCalendar(firstDayOfMonth, monthName, year, numOfDays, monthv, today)
labelsList = renderCalendarReturn[0]
lMonthAnDYear = renderCalendarReturn[1]

#-- RENDEROWANIE KALENDARZA --#

### RENDEROWANIE OKNA DATY ###
DayTitle = StringVar()

TaskTitle = StringVar()
TaskTitleColour = StringVar()
TaskCategory = StringVar()

colourList = ["black", "red", "orange", "green", "blue", "pink"]
categoryList = ["szkoła", "praca", "dom", "inne"]

def NewWindow(year, month, day):
    day = str(day)
    month = str(month)
    if len(day) == 1:
        day = f"0{day}"             
    if len(month) == 1:
        month = f"0{month}" 
    date = f"{year}-{month}-{day}"  #zmiana formatu daty

    title = getDayTitle(date)

    configWindow = Toplevel(root)
    configWindow.title(f"{day}-{month}-{year} | {title}")
    configWindow.geometry("800x600")
    configWindow.resizable(width=False, height=False)

    labelEntrytitleDescription = Label(configWindow, text="Wpisz tytuł dnia: ", width=45, height=5, anchor="nw", padx=10, pady=10, font='Helvetica 10', borderwidth=1, relief="groove")
    labelEntrytitleDescription.place(x=10, y=10)

    entryDayTitle = Entry(configWindow, textvariable = DayTitle, width = 20, font='Helvetica 10')
    entryDayTitle.place(x=20, y=50)

    buttonSubmitDayTitle = Button(configWindow, text = "Zapisz", command = lambda: writeDayTitle(f"title/#{date}title#.txt", entryDayTitle))
    buttonSubmitDayTitle.place(x=20, y=80)

    labelEntryTaskBackground = Label(configWindow, width=54, height=30, borderwidth=1, relief="groove")
    labelEntryTaskBackground.place(x=10, y=130)

    labelEntryTaskDescription = Label(configWindow, text="Treść zadania", width=47, pady=5, anchor="n", font='Helvetica 10 bold', borderwidth=1, relief="groove")
    labelEntryTaskDescription.place(x=11, y=130)

    labelEntryTaskTitle = Label(configWindow, text="Tytuł", font='Helvetica 10')
    labelEntryTaskTitle.place(x=20, y=180)

    entryTaskTitle = Entry(configWindow, textvariable=TaskTitle, width = 40, font='Helvetica 10')
    entryTaskTitle.place(x=20, y=205)

    labelEntryTaskContent = Label(configWindow, text="Treść", font='Helvetica 10')
    labelEntryTaskContent.place(x=20, y=240)

    textTaskContent = Text(configWindow, width=40, height=10, font='Helvetica 10')
    textTaskContent.place(x=20, y=265)

    buttonStartVoiceRec = Button(configWindow, text="    Użyj 🎙️", command = lambda: TaskContentVoiceRec(configWindow, 10, 130, textTaskContent))
    buttonStartVoiceRec.place(x=310, y=265)

    labelTaskTitleColourDecription = Label(configWindow, text="Kolor", font='Helvetica 10')
    labelTaskTitleColourDecription.place(x=20, y=445)

    comboTaskTitleColour = ttk.Combobox(configWindow, textvariable=TaskTitleColour, values = colourList)
    comboTaskTitleColour.current(1)
    comboTaskTitleColour.place(x=20, y=470)

    labelTaskTitleColour = Label(configWindow, text="Kategoria", font='Helvetica 10')
    labelTaskTitleColour.place(x=200, y=445)

    comboTaskCategory = ttk.Combobox(configWindow, textvariable=TaskCategory, values = categoryList)
    comboTaskCategory.current(1)
    comboTaskCategory.place(x=200, y=470)

    buttonGetTask = Button(configWindow, text="Dodaj zadanie", command = lambda: saveTask(textTaskContent, date, entryTaskTitle, configWindow))
    buttonGetTask.place(x=20, y=500)

    try: 
        renderTaskList(date, configWindow)
    except:
        labelNoTasksInfo = Label(configWindow, text="nie ma jeszcze żadnych zadań tego dnia")
        labelNoTasksInfo.place(x=500, y=100)

def saveTask(textbox, date, entryTaskTitle, list):
    TaskTitleTemp = TaskTitle.get()
    TaskTitleColourTemp = TaskTitleColour.get()
    TaskCategoryTemp = TaskCategory.get()
    INPUT = textbox.get("1.0", "end-1c")
    TaskContent = INPUT

    entryTaskTitle.delete(0, END)
    textbox.delete("1.0","end")

    if len(TaskTitleTemp) > 0:
        with open(f"tasklist/#{date}task#.txt", "a") as f:
            f.write(f"{TaskTitleTemp}|{TaskContent}|{TaskTitleColourTemp}|{TaskCategoryTemp}\n")
    else: 
        messagebox.showinfo("Planner", "Zadanie musi zawierać tytuł")

def renderTaskList(date, window):
    f = open(f"tasklist/#{date}task#.txt", "r")
    lines = f.readlines()
    yTask = 10
    widgetList = []

    taskScrollbar = Scrollbar(root)
    taskScrollbar.pack(side = RIGHT, fill = Y)

    for line in lines:
        splittedLine = line.split("|")
        title = splittedLine[0]
        content = splittedLine[1]
        colour = splittedLine[2]
        category = splittedLine[3]

        line = Label(window, width = 50, height = 8, borderwidth=1, relief="groove")
        line.place(x=420, y=yTask)

        line = Label(window, text=f"{title} | {category}", foreground = colour, font='Helvetica 10 bold')
        line.place(x=430, y=yTask+10)

        line = Text(window, font='Helvetica 10', width = 47, height = 4)
        line.place(x=430, y=yTask+40)

        line.insert(END, content)

        line.configure(state="disabled")

        widgetList.append(line)
        print(widgetList)

        yTask += 130

def writeDayTitle(filename, entryName=""):
    title = DayTitle.get()
    entryName.delete(0, END)
    if len(title) > 1:
        with open(f"{filename}", "w") as f:
            f.write(f"%{title}%")
    else:
        messagebox.showinfo("Planner", "Zbyt krótki tytuł")
        
    changeDate()
#-- RENDEROWANIE OKNA DATY --#


### CZYŚCI POLE KALENDARZA ###
def destroyCalendar():
    lMonthAnDYear.destroy()
    for label in labelsList:
        label.destroy()

#-- CZYŚCI POLE KALENDARZA --#        

monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
yearList = [*range(1, 3000)]

def getNewMonth():
    monthName = newMonth.get()
    return monthName

def getNewYear():
    year = newYear.get()
    year = int(year)
    return year

def changeDate():
    destroyCalendar()
    monthName = getNewMonth()
    year = getNewYear()
    if monthName == "January":
        monthv = 1

    if monthName == "February":
        monthv = 2

    if monthName == "March":
        monthv = 3

    if monthName == "April":
        monthv = 4

    if monthName == "May":
        monthv = 5

    if monthName == "June":
        monthv = 6

    if monthName == "July":
        monthv = 7

    if monthName == "August":
        monthv = 8

    if monthName == "September":
        monthv = 9

    if monthName == "October":
        monthv = 10

    if monthName == "November":
        monthv = 11

    if monthName == "December":
        monthv = 12

    firstDayOfMonth = pd.Timestamp(f"{year}-{monthv}-1")
    firstDayOfMonth = firstDayOfMonth.day_name()
    numOfDays = monthrange(year, monthv)[1]
    renderCalendarReturn = renderCalendar(firstDayOfMonth, monthName, year, numOfDays, monthv, today)

newMonth = StringVar()
newYear = StringVar()

comboMonth = ttk.Combobox(root, textvariable=newMonth, values = monthList)
comboMonth.current(monthv-1)
comboMonth.place(x=20, y=780)

comboYear = ttk.Combobox(root, textvariable=newYear, values = yearList)
comboYear.current(year-1)
comboYear.place(x=20, y=810)

butChangeDate = Button(root, text="Zmień datę", command = changeDate)
butChangeDate.place(x=20, y=840)

root.mainloop()


