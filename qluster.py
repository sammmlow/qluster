# -*- coding: utf-8 -*-

###############################################################################
###############################################################################
##                                                                           ##
##      ___  _    _   _ ____ _____ ____ ____                                 ##
##     / _ \| |  | | | |  __|_   _| ___| __ \                                ##
##    ( |_| ) |__| |_| |__  | | | | __|  -/ /                                ##
##     \_  /|____|_____|____| |_| |____|_|\_\                                ##
##       \/                                       v 0.0                      ##
##                                                                           ##
##    FILE DESCRIPTION:                                                      ##
##                                                                           ##
##    This file contains the GUI class which based on Python tkinter.        ##
##    The class will be called in the QLUSTER main python file.              ##
##                                                                           ##
##    Written by Samuel Y. W. Low.                                           ##
##    First created 16-May-2020 15:56 AM (+8 GMT)                            ##
##    Last modified 20-May-2020 18:00 PM (+8 GMT)                            ##
##                                                                           ##
###############################################################################
###############################################################################

# Import our GUI libraries.
import tkinter

# Import local libraries.
from source import rungui

# Initialise the GUI.
root = tkinter.Tk()
root_gui = rungui.RunGUI( root )
root.mainloop()