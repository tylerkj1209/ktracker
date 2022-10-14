"""This is the interactive file that is meant to be run using the tracked
times folder and the main.py file"""
from main import *

name_set = False
bday_set = True
name = ' '
bday = ' '
fav_creature = ' '


saves_file = 'test saves.txt'

main_lists = read_list(saves_file)
stats = main_lists[0]
entries = main_lists[1]

def tracker_function():
    """Run the period tracker software and loop until the user chooses to quit"""

    leave = False
    while not leave:
        print ("Hi! What would yew like to do  ???")
        option = (input("[1] log period or edit entry \n[2] delete an entry \n[3] check when your next period will happen \n[4] view your past periods \n[5] talk to Knoe \n[6] exit and save"))
        if option in ['1', '2', '3', '4', '5', '6']:
            if option == '1':
                trackday(entries)
            elif option == '2':
                deleteday(entries)
            elif option == '3':
                update_all_stats(stats, entries)
                next_period(entries, stats)
            elif option == '4':
                check_days(entries)
            elif option == '6':
                leave = True
        else:
            print ("Oopsies I didn't get that ")


def trackday(entries_list):
    """Track a day"""
    print ("Is your entry for today??? ")
    allow = input("[y] for yes, [n] for no  \n") == 'y'
    if allow:
        date = None
    else:
        print ("What day do you want to add")
        date = input("Enter the date in the format \nYYYY MM DD\n")
        date = date.split(' ')

        for i in range(len(date)):
            date[i] = int(date[i])
        date = datetime.date(date[0], date[1], date[2])
    print ("On this day, are you having your period?? ")
    period_bool = (input("[y] for yes, [n] for no \n") == 'y')
    add_entry(date, period_bool, entries_list)
    print ("Okay " + name + "!!! I added an entry to your period data! ")
    input("")

def deleteday(entries_list):
    """Remove a day"""
    print ("Here is a list of dates you've had your period ... \n"
           "YYYY, MM, DD, Period?")
    for entry in entries_list:
        print (str(entry))
    print ('\n')
    print ("What date would you like to remove???")
    date = input("Enter the date in the format \nYYYY, MM, DD or press [e] to exit \n")
    if date == 'e':
        print ('Okay!!!')
        return None

    date = date.split(', ')

    for i in range(len(date)):
        date[i] = int(date[i])
    date = datetime.date(date[0], date[1], date[2])
    for item in entries_list:
        if item.date == date:
            entries_list.remove(item)

    print ("I removed the entry!")

def next_period(entries_list, stats_list):
    """Check when the next period will be"""
    for i in range(len(entries_list)):
        if entries_list[-i - 1].period:
            last_date = entries_list[-i - 1]
            break

    update_cycle_len(stats_list, entries_list)

    median_period = median(entries_list)

    cycle_days = stats_list[0]
    next_day = last_date.date + datetime.timedelta(days=cycle_days)
    next_day_low_res = datetime.date(next_day.year, next_day.month, next_day.day)
    print ("\nYour average cycle length is around " + str(cycle_days) + " days long and your next period is expected on " + str(next_day_low_res) + " \nThis prediction might be off by " + str(stats_list[1]) + " days 3 \n You also have a median cycle length of " + str(median_period) + " days \n")
    if median_period > cycle_days:
        print ("I have noticed that you typically also have a late period.\n")
    else:
        print ("I have noticed that you typically also have an early period.\n")

def check_days(entries_list):
    """Print a list of periods"""
    print ("here is a list of every period you have entered into the tracker \n")
    for item in entries_list:
        print (str(item))

tracker_function()



print ("OKay bye bye for now! ")
print ("See you later!!! ")
write_list(saves_file, stats, entries)

