#!/usr/bin/env python3
import subprocess
import datetime
import time
import os
import sys

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
        current_time = datetime.datetime.now().strftime("%H:%M")
        current_day = datetime.datetime.now().strftime("%A")
        print("Enter 'cancel' to stop the script")

        if current_time == macrotime and (not macroday or current_day == macroday) and not macro_executed:
            run_macro(macroname)
            macro_executed = True  # Set the flag to indicate macro has been executed


        # Reset the flag at the start of a new day
        if current_time == "00:00":
            macro_executed = False

        # Sleep for 5 seconds before checking the time again
        time.sleep(5)


macroname = sys.argv[2]
macrotime = sys.argv[3]
macroday = sys.argv[4] if len(sys.argv) > 4 else None
open('schedule.log', 'w').close()
file = open('/etc/hppymacros/schedule.log', 'w')
pymacroday = macroday
if macroday == 'None':
   pymacroday = ''

file.write(macroname + "\n" + macrotime + "\n" + pymacroday)

file.close()

if macroday and macroday not in valid_days:
        print("Error: Invalid day. Please enter a valid day of the week. The first letter of the day needs to be uppercase. Example: Tuesday.")
        sys.exit(1)

schedule_macro(macroname, macrotime, macroday)
