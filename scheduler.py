#!/usr/bin/env python3
import subprocess
import datetime
import time
import os
import sys
import re

macros_dir = "/etc/hppymacros"
valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def run_macro(macroname):
    macro_file = os.path.join(macros_dir, f"{macroname}.hpy")
    if os.path.isfile(macro_file):
        print(f"Running macro '{macroname}'...")
        subprocess.Popen(["bash", macro_file])
    else:
        print(f"Macro '{macroname}' not found")

def schedule_macro(macroname, macrotime, macroday=None):
    macro_executed = False  # Flag to track if macro has been executed

    while True:
        print("Enter 'cancel' to stop the script")
        current_time = datetime.datetime.now().strftime("%H:%M")
        current_day = datetime.datetime.now().strftime("%A")

        if current_time == macrotime and (not macroday or current_day == macroday) and not macro_executed:
            run_macro(macroname)
            macro_executed = True  # Set the flag to indicate macro has been executed

        # Prompt the user for input
        if functions == "-sc":
            user_input = input()
            if user_input.lower() == "cancel":
                print("Script canceled.")
                os.remove('/tmp/schedule.log')
                return  # Exit the function and return to the command line 

        # Reset the flag at the start of a new day
        if current_time == "00:00":
            macro_executed = False

        # Sleep for 5 seconds before checking the time again
        time.sleep(5)

functions = sys.argv[1]
macroname = sys.argv[2]
macrotime = sys.argv[3]
macroday = sys.argv[4] if len(sys.argv) > 4 else None

if re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', macrotime):
    open('schedule.log', 'w').close()
    file = open('/tmp/schedule.log', 'w')
    pymacroname = repr(macroname)
    pymacrotime = macrotime
    pymacroday = macroday
    if macroday is None:
        pymacroday = ''

    file.write(pymacroname + "\n" + pymacrotime + "\n" + pymacroday)

    file.close()

    if macroday and macroday not in valid_days:
            print("Error: Invalid day. Please enter a valid day of the week. The first letter of the day needs to be uppercase. Example: Tuesday.")
            sys.exit(1)

    schedule_macro(macroname, macrotime, macroday)
else:
    print("Select a valid time format. Example: 23:39")