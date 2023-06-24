import unittest
import sqlite3

# Defining the habit test class.
class habit_Test(unittest.TestCase):
    # This method test the analysis function and completed daily habits.
    def test_comp_dailyhab(self):
        i = 'reading'
        check_count = anal_hab('daily', i)
        message = "Habit is not complete"
        self.assertEqual(check_count, 7, message)

    def test_incomp_dailyhab(self):
    # This method test the analysis function and incomplete daily habits.
        i = 'swimming'
        check_count = anal_hab('daily', i)
        message = "Habit is complete"
        self.assertNotEqual(check_count, 7, message)

    def test_comp_weeklyhab(self):
        # This method test the analysis function and completed weekly habits.
        i = 'jogging'
        check_count = anal_hab('weekly', i)
        message = "Habit is not complete"
        self.assertEqual(check_count, 7, message)

    def test_incomp_weeklyhab(self):
    # This method test the analysis function and incompleted weekly habits.
        i = 'hiking'
        check_count = anal_hab('weekly', i)
        message = "Habit is complete"
        self.assertNotEqual(check_count, 7, message)

    def test_comp_monthlyhab(self):
        # This method test the analysis function and completed monthly habits.
        i = 'gaming'
        check_count = anal_hab('monthly', i)
        message = "Habit is not complete"
        self.assertEqual(check_count, 6, message)

    def test_dailyperiod_quest(self):

        per = 'daily'

        check_per = period_quest('daily')
        message = "Period is not correct"
        self.assertEqual(check_per, per, message)

    def test_weeklylyperiod_quest(self):

        per = 'weekly'

        check_per = period_quest('weekly')
        message = "Period is not correct"
        self.assertEqual(check_per, per, message)

    def test_monthlyperiod_quest(self):

        per = 'monthly'

        check_per = period_quest('monthly')
        message = "Period is not correct"
        self.assertEqual(check_per, per, message)

# Func for hab anal
def anal_hab(period, name):  
    # Connects to the db.
    db = sqlite3.connect("../habit/habittest.db") 
    cur = db.cursor()
    ana_dict = {}

    # Taking data from db.
    cur.execute(f"SELECT * FROM {period} WHERE name = '{name}'")
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
            counts = anal_count(period, comp, count)
            if counts == 6:
                print(f"{name} {period} habit checked in completly {counts - 1} times consecutively after creation, {name} is successfully made an habit")

            elif counts != 6 and comp == 'yes':
                print(f"{name} {period} habit checked in {counts - 1} times after creation, but already marked as complete")

            else:
                print(f"{name} {period} habit checked in {counts - 1} times after creation, {name} habit not made yet")

        else:
            comp = row[9]
            counts = anal_count(period, comp, count)
            if counts == 7:
                print(f"{name} {period} habit checked in completly {counts - 1} times consequtively after creation, {name} is successfully made an habit")
            elif counts != 7 and comp == 'yes':
                print(f"{name} {period} habit checked in {counts - 1} times after creation, but already marked as complete")

            else:
                print(f"{name} {period} habit checked in {counts - 1} times after creation, {name} habit not made yet")


    # Close db connection.
    cur.close()
    db.close()
    return counts

# This function calculate the total of check-in's.
def anal_count(period, comp, count):
    if period == 'monthly':    
        count_hab = 7 - count
        if comp == 'yes':
            count_hab = count_hab - 1
            return count_hab
        else:
            count_hab = count_hab
            return count_hab

    else:
        count_hab = 8 - count
        if comp == 'yes':
            count_hab = count_hab - 1
            return count_hab
        else:
            count_hab = count_hab
            return count_hab

def period_quest(oper):     
    per_list = ["daily", "weekly", "monthly"]

    if oper in per_list:
        return oper
    else:
        exit(0)