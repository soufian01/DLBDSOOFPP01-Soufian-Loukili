from sys import argv, exit
from datetime import date
from datetime import time
from datetime import datetime
import sqlite3
import functools
import operator
from collections import Counter
import unittest
import habtest


# Creating the main function to introduce the program and understand the user's needs, then calling the class to be used.
def main():
    print("Habit tracker software (by Soufian Loukili)")
    print("Welcome to the habit tracker software program, you can create(1) a new habit, check(2) in or off habits, analyse(3), test(4), and delete habits(5)")
    print()
    operator = int(input("Please indicate what would you like to do using numbers 1(create), 2(check), 3(analyse), 4(test), 5(delete) -> "))

    if operator == 1: 
        # If the input is equal to 1, it means that the user wants to create a new habit. At this point the periodicity is asked.   
        period = period_quest(operator)     
        habit_name = input("Indicate the name of the habit that you want to create -> ")
        print()
        name_check = habit_check(habit_name, period)    # Checks if the name of the habit already exists.
        if name_check == False:
            crete_habit = habit(habit_name, period)
            crete_habit.create()
        else:
            comerror(5)

    elif operator == 2:   
        # If the input is equal to 2, it means that the user wants to do a habit check.
        period = period_quest(operator)     
        print_habit(period)     
        chab_name = input(f"Indicate wich habit {period} would you like to check in or off -> ")
        print()
        # Check if input name exists (calling habit_check func).
        habitName_check = habit_check(chab_name, period)    
        if habitName_check == True:
            check_habit = habit(chab_name, period)  
            check_habit.check()
        else:
            comerror(6)     
            exit(0)
        

    elif operator == 3:     
        # If the input is equal to 3, it means that the user wants to analyze habits.
        period = period_quest(operator)
        habit_analyse = habit(None, period)
        habit_analyse.analyse()

    
    elif operator == 4:    
        # If the input is equal to 4, it means the user wants to test.
        test_habit = habit()
        test_habit.hab_test()

    elif operator == 5:      
        # If the input is equal to 5, it means that the user wants to eliminate a habit.
        period = period_quest(operator)
        print_habit(period)     
        deleleteHabit_name = input(f"Indicate wich habit {period} would you like to delete -> ")   
        print()
        deleteName_check = habit_check(deleleteHabit_name, period)      
        if deleteName_check == True:
            confirm = input(f"Please confirm that you want to delete {deleleteHabit_name} type yes/no -> ")      
            print()
            if confirm == "yes":    
                print(f"{deleleteHabit_name} {period} habit deleted")
                delete_habit = habit(deleleteHabit_name, period)
                delete_habit.delete()
            elif confirm == "no":   
                print(f"{deleleteHabit_name} habit not deleted")
            else:
                print("Invalid command: Please type yes or no")
            
        else:
            comerror(6)
            exit(0)

       
    else:
        comerror(1)


# Creating the class "habit" wich has two attributes: name and period, and five methods: create, check, delete, analyse and test
class habit:
    # Constructor function
    def __init__(self, name = None, period = None):     
        self.name = name
        self.period = period
        
    # Method for creating habits.
    def create(self):   
        name = self.name
        period = self.period
        day = ftime(period)

        # Open connection to db.
        db = sqlite3.connect("../habit/habit.db")
        cur = db.cursor()

        # Save changes to db.
        cur.execute(f"INSERT INTO {period} ('name', 'first') VALUES ('{name}',{day})")

        db.commit()     
        cur.close()     
        db.close() # Close connection to db.
    
        print(f"{name} {period} habit created")
    
    # Method for checking in/off habits.
    def check(self):    
        name = self.name
        period = self.period
        in_or_off = input(f"Would you like to check in or off the {name} habit? type in/off -> ")
        if in_or_off == "in":    
            habit_checkin(period, name)
        elif in_or_off == "off":
            habit_checkoff(period, name)
        else:
            comerror(4)
            exit(0)

    # Method for analysing habits.        
    def analyse(self):      
        period = self.period
        print(f"Below there is the analysis of {period} habits")
        print("It need to be checked in six times daily or weekly after creation to succesfully male a daily and weekly habit\n")
        print("It needs to be checked in five times monthly after creation to succesfully make a monthly habit\n")
        analyse_habit(period)  
    
    # Method for deleting habits.
    def delete(self):       
        name = self.name
        period = self.period
        # Open connection to db.
        db = sqlite3.connect("../habit/habit.db")
        cur = db.cursor()
    
        cur.execute(f"DELETE FROM {period} WHERE name = '{name}'") # Delete habit from db.
    
        db.commit()
        cur.close()
        db.close() # Close connection to db.
    
    def hab_test(self): 
        test_en = unittest.TestLoader().loadTestsFromModule(habtest)
        unittest.TextTestRunner(verbosity=1).run(test_en)
        
# This function asks the user about the periodicity of the habit.          
def period_quest(operator):     
    period_list = ["daily", "weekly", "monthly"]
    if operator == 'check':
        period = input("Indicate period to check in or off daily, weekly or monthly -> ")
    else:
        period  = input("Indicate period to work on daily weekly or monthly -> ")

    if period in period_list:
        return period
    else:
        comerror(3)
        exit(0)

# This function checks is a habit already exists.
def habit_check(in_name, period):
    # Open connection to db.  
    db = sqlite3.connect("../habit/habit.db")   
    cur = db.cursor()
    data = []  
    cur.execute(f"SELECT name FROM {period}")   
    for row in cur:    
        rowe = functools.reduce(operator.add, (row))  
        data.append(f"{rowe}")

    if in_name in data:     # Check if name already exists in db.
        return True
    else:
        return False

    cur.close()  
    db.close() # Close connection to db.

# This function print all habits in indicated periodicity.
def print_habit(period): 
    # Open connection to db.
    db = sqlite3.connect("../habit/habit.db")   
    cur = db.cursor()
    # Save changes to db.
    cur.execute(f"SELECT name FROM {period}") 
    
    i = 1
    for row in cur:
        names = functools.reduce(operator.add, (row))   
        print(f"{i}.) {names}")
        i+=1

    cur.close()    
    db.close() # Close connection to db.
 
# This function check habits called from class.
def habit_checkin(period, name):      
    chevalue = ftime(period) 
    # Open connection to db.   
    db = sqlite3.connect("../habit/habit.db")
    cur = db.cursor()
    data =[]

    # Save changes to db.
    cur.execute(f"SELECT comp FROM {period} WHERE name = '{name}'")     
    for row in cur:     
        data = row
        choff = functools.reduce(operator.add, (row))   #
        conf = choff
        #print(data)
    
    if conf == 'yes': 
        print(f"{name} habit already checked off")
          
    else: 
        # Save changes to db.
        cur.execute(f"SELECT first FROM {period} WHERE name = '{name}'")
    
        for row in cur:
            rowe = functools.reduce(operator.add, (row))
            first_date = rowe
    
        currdate = chevalue - first_date    
    
        if period == 'monthly': 
            checkInsertmon(period, currdate, chevalue, name)
        elif period == 'weekly':
            checkInsert(period, currdate, chevalue, name)
        else:
            checkInsert(period, currdate, chevalue, name)
    
    db.commit()
    cur.close()
    db.close() # Close connection to db.

# This function allowa to check off a habit.
def habit_checkoff(period, name): 
    # Open connection to db.  
    db = sqlite3.connect("../habit/habit.db")
    cur = db.cursor()
    
    # Save changes to db.
    cur.execute(f"SELECT comp FROM {period} WHERE name = '{name}'")   
    
    for row in cur:     
        rowe = functools.reduce(operator.add, (row))
        con = rowe
    
    if con == 'yes':  
        print(f"{name} habit already checked off")
        
    else:
        # Save changes to db.
        cur.execute(f"UPDATE {period} SET comp = 'yes' WHERE name = '{name}'")
    
    
    db.commit()
    cur.close()
    db.close() # Close connection to db.

# This function inserts monthly check in into a monthly table.
def checkInsertmon(period, cdate, invalue, name):
    chevalue = ftime(period)  
    # Open connection to db. 
    db = sqlite3.connect("../habit/habit.db")
    cur = db.cursor()
    
    if cdate == 0:
        print("Check in not possible. Already checked in")
    elif cdate == 1:
        cur.execute(f"UPDATE {period} SET second = {invalue} WHERE name = '{name}'") # Save changes to db.
    elif cdate == 2:
        cur.execute(f"UPDATE {period} SET third = {invalue} WHERE name = '{name}'") # Save changes to db.
    elif cdate == 3:
        cur.execute(f"UPDATE {period} SET forth = {invalue} WHERE name = '{name}'") # Save changes to db.
    elif cdate == 4: 
        cur.execute(f"UPDATE {period} SET fifth = {invalue} WHERE name = '{name}'") # Save changes to db.
    elif cdate == 5:
        cur.execute(f"UPDATE {period} SET sixth = {invalue} WHERE name = '{name}'") # Save changes to db.
    else:
        print("Incorrect Check-in: Check-in beyond recommended time -> This means that if checkin is not complete at this time then this habit is not a success ")
        
    db.commit()
    cur.close()
    db.close() # Close connection to db.
    
# This function inserts daily and weekly check in into daily and weekly tables.
def checkInsert(period, cdate, invalue, name):
    chevalue = ftime(period) 
    # Open connection to db. 
    db = sqlite3.connect("../habit/habit.db")
    cur = db.cursor()
    
    if cdate == 0:
        print("Check in not possible. Already checked in")
    elif cdate == 1:
        cur.execute(f"UPDATE {period} SET second = {invalue} WHERE name = '{name}'") # Save changes to db.
    elif cdate == 2:
        cur.execute(f"UPDATE {period} SET third = {invalue} WHERE name = '{name}'") # Save changes to db.
    elif cdate == 3:
        cur.execute(f"UPDATE {period} SET forth = {invalue} WHERE name = '{name}'") # Save changes to db.
    elif cdate == 4:
        cur.execute(f"UPDATE {period} SET fifth = {invalue} WHERE name = '{name}'") # Save changes to db.
    elif cdate == 5:
        cur.execute(f"UPDATE {period} SET sixth = {invalue} WHERE name = '{name}'") # Save changes to db.
    elif cdate == 6:
        cur.execute(f"UPDATE {period} SET seventh = {invalue} WHERE name = '{name}'") # Save changes to db.
    else:
        print("Incorrect Check-in: Check-in beyond recommended time -> This means that if checkin is not complete at this time then this habit is not a success ")
        
    db.commit()
    cur.close()
    db.close() # Close connection to db.
 
# This function analyzes habit, by calculating how many times it has been checked.
def analyse_habit(period):    
    # Open connection to db.
    db = sqlite3.connect("../habit/habit.db")   
    cur = db.cursor()
    ana_dict = {}

    # Save changes to db.
    cur.execute(f"SELECT * FROM {period}")
    k = 1
    for row in cur:
        data = row
        name = row[1]
        count = 0
        
        for i in row:   
            if i is not None:
                count = count + 0
            else:
                count = count + 1
        
        if period == 'monthly':
            comp = row[8]
            counts = analyse_count(period, comp, count)    
            if counts == 6:
                print(f"{k}.) {name} {period} habit checked in completly {counts - 1} times consecutively after creation, {name} is successfully made an habit")
                
            elif counts != 6 and comp == 'yes':
                print(f"{k}.) {name} {period} habit checked in {counts - 1} times after creation, but already marked as complete")
            
            else:
                print(f"{k}.) {name} {period} habit checked in {counts - 1} times after creation, {name} habit not made yet")
                
        else:
            comp = row[9]
            counts = analyse_count(period, comp, count)       
            if counts == 7:
                print(f"{k}.) {name} {period} habit checked in completly {counts - 1} times consequtively after creation, {name} is successfully made an habit")
            elif counts != 7 and comp == 'yes':
                print(f"{k}.) {name} {period} habit checked in {counts - 1} times after creation, but already marked as complete")
                
            else:
                print(f"{k}.) {name} {period} habit checked in {counts - 1} times after creation, {name} habit not made yet")
        
        k+=1           
        
    cur.close()
    db.close() # Close connection to db.

# This function calculate the number of check in.
def analyse_count(period, comp, count):
    if period == 'monthly':     
        counts = 7 - count
        if comp == 'yes':
            counts = counts - 1
            return counts    
        else:
            counts = counts
            return counts
    
    else:
        counts = 8 - count
        if comp == 'yes':
            counts = counts - 1
            return counts
        else:
            counts = counts
            return counts

# This function print error based on the error value.   
def comerror(val):  
    if val == 1:
        print("Invalid entry: please type the number of the function that you want to use 1, 2, 3, 4, 5")
    elif val == 2:
        print("Command line error, methods are: create, check, analyse and delete")
    elif val == 3:
        print("Invalid entry: please input daily, weekly or monthly")
    elif val == 4:
        print("Invalid entry: please input in or off")
    elif val == 5:
        print("Habit already exists")
    elif val == 6:
        print("Habit doesn't exist")


def ftime(period): 
    t = date.today()   
    day = t.day     
    week = t.isocalendar()[1]  
    mon = t.month
    if period == "daily":
        return day
    elif period == "weekly":
        return week
    else:
        return mon

main()



