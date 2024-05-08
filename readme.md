# Hppy macros

(You are in the `indev` branch, which means that the source code found in here is not release-ready and it's often not working. This branch is use for the sake of logging and commodity)

Hppy macros is a linux macroing tool for automatizing linux commands.  
You can schedule a macro to run at certain days of the weeks, and at certain hours.  
It is an open source project ran by me (the creator) written in bash and python.  

To install it, first download the latest release from [Releases](https://github.com/mogapog/hppy-macros/releases) and unzip it. Then open a terminal in the "/hppyactualinstall/" directory inside the unzipped file and then type the following commands:  

`chmod +x hppy`  

Next, run:  

`./hppy -i`  

This will set up everything you need. The macros, the python scripts and this readme file will move to the directory "/etc/hppymacros".  

Run `hppy -h` after the installation to see all the commands.  

The hppy file itself will be located at "/usr/local/bin/"  

If you are running distros based on ubuntu (e.g linux mint), you may encounter issues when trying to run the scheduler. We reccomend running `sudo apt install python-is-python3` on your terminal before installing to prevent them.

Right now the hppy project is in a beta phase and a lot of things could and will change. Please report any bugs you find as this will help make the project better.  

The tool works by creating a text file with the commands and running them as bash. You input the commands you want to be stored in a macro, and then you run them all at once.  

You can schedule the macros to run at certain hours of the day, and at certain days of the week if you want to. Currently you can only schedule one macro at a time,  
and the macro will not keep scheduling if you restart the computer.  

There are _other_ (and better) ways to run multiple commands on the background and schedule them. But if you want, you can run this one. It's lightweight,
somewhat easy to use and easy to fork.  

Thanks for reading.  

## Hppy version 0.1.0

