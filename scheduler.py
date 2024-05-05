#!/usr/bin/env python3
import subprocess
import datetime
import time
import os
import sys
import re
import atexit
import getpass
from crontab import CronTab

functions = sys.argv[1] if len(sys.argv) > 1 else None
macroname = sys.argv[2] if len(sys.argv) > 2 else None
macrotime = sys.argv[3] if len(sys.argv) > 3 else None
macroday = sys.argv[4] if len(sys.argv) > 4 else None
args = sys.argv[5] if len(sys.argv) > 5 else None


macros_dir = "/etc/hppymacros"
valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Every"]
cronpath = os.path.join(macros_dir, "scheduler.py")
cronlog = os.path.join(macros_dir, "cronschedule.log")
cronscript = 'python ' + f"{cronpath} " + f"{functions} " + f"{macroname} " + f"{macrotime} " + f"{macroday} " + ">> "  + f"{cronlog} " + "2>&1"
usr = getpass.getuser()

def cleanup():
    if os.path.exists('/tmp/schedule.log'):
        os.remove('/tmp/schedule.log')
    if os.path.exists('/tmp/bckschedule.log'):
        os.remove('/tmp/bckschedule.log')

def run_macro(macroname):
    macro_file = os.path.join(macros_dir, f"{macroname}.hpy")
    if os.path.isfile(macro_file):
        print(f"Running macro '{macroname}'...")
        subprocess.run(["bash", macro_file])
    else:
        print(f"Macro '{macroname}' not found")


def createjob():
    errorcron = False
    spacemacrotime = macrotime.replace(":"," ")
    hourminutes = spacemacrotime.split()
    hours = hourminutes[0]
    minutes = hourminutes[1]


    if(macroday == "Every"):
        cronjob = (f"{minutes} " + f"{hours} " + "* * *")
    elif(macroday == "Monday"):
        cronjob = (f"{minutes} " + f"{hours} " + "* * 1")
    elif(macroday == "Tuesday"):
        cronjob = (f"{minutes} " + f"{hours} " + "* * 2")
    elif(macroday == "Wednesday"):
        cronjob = (f"{minutes} " + f"{hours} " + "* * 3")
    elif(macroday == "Thursday"):
        cronjob = (f"{minutes} " + f"{hours} " + "* * 4")
    elif(macroday == "Friday"):
        cronjob = (f"{minutes} " + f"{hours} " + "* * 5")
    elif(macroday == "Saturday"):
        cronjob = (f"{minutes} " + f"{hours} " + "* * 6")
    elif(macroday == "Sunday"):
        cronjob = (f"{minutes} " + f"{hours} " + "* * 0")

    with CronTab(user=usr) as cron:
        for job in cron:
            if re.search("/etc/hppymacros/scheduler.py", str(job)):
                print("Couldn't write cron schedule because a cron scheduler already exists. Delete it first.")
                errorcron = True
                return

        if errorcron != True:
            with open(cronlog, "w") as cronl:
                cronl.write("The output of your command is: " + "\n" )
                cronl.close()

            job = cron.new(command=cronscript)
            job.setall(cronjob)
            cron.write()
            print("Wrote a persistent cron schedule to user: " + usr)

def schedule_macro(macroname, macrotime, macroday=None):
    macro_executed = False  # Flag to track if macro has been executed
 
    if args == "-pr":
        if os.geteuid() != 0:
            print('To run persistent schedules, you need root privileges. Run "sudo" before your command.')
        else:
            createjob()

    if args != "-pr":
        print("Enter 'cancel' to stop the script")
    elif functions == "-sc":
        print("Entering 'cancel' will stop the main script, but the cron schedule will still be there. Delete it with hppy -kcs.")

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        current_day = datetime.datetime.now().strftime("%A")

        if current_time == macrotime and (current_day == macroday or macroday == 'Every') and not macro_executed:
            run_macro(macroname)
            macro_executed = True  # Set the flag to indicate macro has been executed

        if current_time == macrotime and (current_day == macroday or macroday == 'Every') and not macro_executed:
                run_macro(macroname)
                macro_executed = True  # Set the flag to indicate macro has been executed

            # Prompt the user for input
        if functions == "-sc":
            user_input = input()
            if user_input.lower() == "cancel":
                print("Script canceled.")
                cleanup()
                return  # Exit the function and return to the command line 

                # Reset the flag at the start of a new day
        if current_time == "00:00":
            macro_executed = False

        # Sleep for 5 seconds before checking the time again
        time.sleep(1)

if functions != "-kcs":
    if re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', macrotime):
        file = open('/tmp/schedule.log', 'w')
        pymacroname = repr(macroname)
        pymacrotime = macrotime
        pymacroday = macroday
        if macroday is None:
            pymacroday = ''

        file.write(pymacroname + "\n" + pymacrotime + "\n" + pymacroday)

        file.close()

        if macroday not in valid_days:
                print("Error: Invalid day. Please enter a valid day of the week. The first letter of the day needs to be uppercase. Example: Tuesday or Every, for every day.")
                cleanup()
                sys.exit(1)

        schedule_macro(macroname, macrotime, macroday)
        print(cronscript)
        print(cronpath)
    else:
        print("Select a valid time format. Example: 23:39")
        cleanup()

if functions == "-kcs":
    with CronTab(user=usr) as cron:
        for job in cron:
            if re.search("/etc/hppymacros/scheduler.py", str(job)):
                cron.remove(job)
                cron.write()
                os.remove(cronlog)
                print("Succesfully removed cron schedule.")
            else:
                print("Could not find a cron job for the scheduler.")

atexit.register(cleanup)
