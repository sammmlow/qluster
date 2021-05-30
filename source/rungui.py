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

# Import global libraries
import tkinter as tk
import tkinter.font
from PIL import Image, ImageTk
from os.path import dirname, abspath, join
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

# Import the local libraries
from source import deputy
from source import relative


class RunGUI():

    def __init__(self, master):
        
        '''
        Loads the GUI class object, taking a tkinter.Tk() object as input.
        
        Example initialisation:
        >> root = tkinter.Tk()
        >> root_gui = run_gui( root )
        >> root.mainloop()
        '''
        
        # Create the main frame and window.
        master.title('QLUSTER v0.1')
        master.geometry('1600x1200')
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###         Initialisation of text labels and variables           ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        # Initialise header labels
        self.txt_headerC = 'Chief Satellite Orbit'
        self.txt_headerD = 'Formation RIC Geometry'
        self.txt_headerP = 'Formation Plane Angles'
        
        # Initialise text labels for scenario time parameters
        self.txt_td = 'Propagation Duration (s)'
        self.txt_ts = 'Propagation Timestep (s)'
        
        # Initialise text labels for the Chief satellite orbit
        self.txt_aC = 'Chief Orbit Semi-Major Axis (km)'
        self.txt_eC = 'Chief Orbit Eccentricity (0 to 1)'
        self.txt_iC = 'Chief Orbit Inclination (deg)'
        self.txt_wC = 'Chief Orbit Arg. of Perigee (deg)'
        self.txt_RC = 'Chief Orbit Right Ascension (deg)'
        self.txt_MC = 'Chief Orbit Mean Anomaly (deg)'
        
        # Initialise text labels for RIC requirements
        self.txt_fR = 'Formation Radial Amplitude (km)'
        self.txt_fI = 'Formation In-Track Amplitude (km)'
        self.txt_fO = 'Formation In-Track Offset (km)'
        self.txt_fC = 'Formation Cross-Track Amplitude (km)'
        
        # Initialise text labels for formation plane angular parameters
        self.txt_fPhi = 'Argument of Relative Pericenter (deg)'
        self.txt_fTht = 'Argument of Latitude Crossing (deg)'
        
        # Initialise variables for scenario time parameters
        self.var_td = tk.IntVar() # Propagation Duration (s)
        self.var_ts = tk.IntVar() # Propagation Timestep (s)
        
        # Initialise variables for the Chief satellite orbit
        self.var_aC = tk.DoubleVar() # Chief Semi-Major Axis (km)
        self.var_eC = tk.DoubleVar() # Chief Eccentricity (0 to 1)
        self.var_iC = tk.DoubleVar() # Chief Inclination (deg)
        self.var_wC = tk.DoubleVar() # Chief Arg. of Perigee (deg)
        self.var_RC = tk.DoubleVar() # Chief Right Ascension (deg)
        self.var_MC = tk.DoubleVar() # Chief Mean Anomaly (deg)
        
        # Initialise variables for RIC requirements
        self.var_fR = tk.DoubleVar() # Radial Separation (km)
        self.var_fI = tk.DoubleVar() # In-Track Separation (km)
        self.var_fO = tk.DoubleVar() # In-Track Offset (km)
        self.var_fC = tk.DoubleVar() # Cross-Track Separation (km)
        
        # Initialise variables for formation plane angular parameters
        self.var_fPhi = tk.DoubleVar() # Argument of Relative Pericenter (deg)
        self.var_fTht = tk.DoubleVar() # Argument of Latitude Crossing (deg)
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###             Configure the software logo display               ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        # Define the path to the QLUSTER logo file.
        qluster_logo = dirname(dirname(abspath(__file__)))
        qluster_logo = join(qluster_logo, 'gui', 'qluster_logo.png')
        
        # Configure the background image and load the logo.
        image = Image.open( qluster_logo )
        photo = ImageTk.PhotoImage(image)
        self.logo = tk.Label(image=photo)
        self.logo.image = photo
        self.logo.grid(row=0, column=0, padx=20, pady=20, columnspan=4)
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###       Add basic buttons for LOAD, SAVE, CLEAR, LOG, RUN       ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        # Add a button to read default entries from 'config.txt'.
        self.cfgR = tk.Button(master, text='Load Config', command=self.cfg_R)
        self.cfgR.grid(row=0, column=4, padx=20, pady=5)
        self.cfgR.configure(bg="light blue")
        
        # Add a button to save entries into 'config.txt'.
        self.cfgW = tk.Button(master, text='Save Config', command=self.cfg_W)
        self.cfgW.grid(row=0, column=5, padx=20, pady=5)
        self.cfgW.configure(bg="light blue")
        
        # Add a button to clear the relative orbit plots.
        self.clrBtn = tk.Button(master, text='Clear Plots', command=self.clr)
        self.clrBtn.grid(row=0, column=6, padx=20, pady=5)
        self.clrBtn.configure(bg="light blue")
        
        # Add a button to save the relative ephemeris.
        self.logBtn = tk.Button(master, text='Log Data', command=self.log)
        self.logBtn.grid(row=0, column=7, padx=20, pady=5)
        self.logBtn.configure(bg="light blue")
        
        # Add a button to run QLUSTER.
        self.runBtn = tk.Button(master, text='Run Program', command=self.run)
        self.runBtn.grid(row=0, column=8, padx=20, pady=5)
        self.runBtn.configure(bg="light blue")
        
        
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###     Create input text boxes for propagation time and step     ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        # Input the Propagation Duration (s).
        self.label_td = tk.Label(master, text=self.txt_td )
        self.label_td.grid(row=1, column=0, padx=40, pady=2, sticky='w')
        self.entry_td = tk.Entry(master, width=10, textvariable=self.var_td)
        self.entry_td.grid(row=1, column=1, padx=5, pady=2, sticky='w')
        self.errtx_td = tk.Label(master, text='', fg='red' )
        self.errtx_td.grid(row=1, column=3, padx=5, pady=2, sticky='w')
        
        # Input the Propagation Time Step (s).
        self.label_ts = tk.Label(master, text=self.txt_ts )
        self.label_ts.grid(row=2, column=0, padx=40, pady=2, sticky='w')
        self.entry_ts = tk.Entry(master, width=10, textvariable=self.var_ts)
        self.entry_ts.grid(row=2, column=1, padx=5, pady=2, sticky='w')
        self.errtx_ts = tk.Label(master, text='', fg='red' )
        self.errtx_ts.grid(row=2, column=3, padx=5, pady=2, sticky='w')
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###  Create input text boxes for chief satellite orbit elements   ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        # Title for the Chief Orbital Parameters
        self.label_headerC = tk.Label(master, text=self.txt_headerC,
                                      font=('Helvetica',9,'bold'))
        self.label_headerC.grid(row=3, column=0, padx=40, pady=10, sticky='w')
        
        # Input the Chief Semi-Major Axis (km).
        self.label_aC = tk.Label(master, text=self.txt_aC )
        self.label_aC.grid(row=4, column=0, padx=40, pady=2, sticky='w')
        self.entry_aC = tk.Entry(master, width=10, textvariable=self.var_aC)
        self.entry_aC.grid(row=4, column=1, padx=5, pady=2, sticky='w')
        self.errtx_aC = tk.Label(master, text='', fg='red' )
        self.errtx_aC.grid(row=4, column=3, padx=5, pady=2, sticky='w')
        
        # Input the Chief Eccentricity (0 to 1)
        self.label_eC = tk.Label(master, text=self.txt_eC )
        self.label_eC.grid(row=5, column=0, padx=40, pady=2, sticky='w')
        self.entry_eC = tk.Entry(master, width=10, textvariable=self.var_eC)
        self.entry_eC.grid(row=5, column=1, padx=5, pady=2, sticky='w')
        self.errtx_eC = tk.Label(master, text='', fg='red' )
        self.errtx_eC.grid(row=5, column=3, padx=5, pady=2, sticky='w')
        
        # Input the Chief Inclination (deg)
        self.label_iC = tk.Label(master, text=self.txt_iC )
        self.label_iC.grid(row=6, column=0, padx=40, pady=2, sticky='w')
        self.entry_iC = tk.Entry(master, width=10, textvariable=self.var_iC)
        self.entry_iC.grid(row=6, column=1, padx=5, pady=2, sticky='w')
        self.errtx_iC = tk.Label(master, text='', fg='red' )
        self.errtx_iC.grid(row=6, column=3, padx=5, pady=2, sticky='w')
        
        # Input the Chief Arg. of Perigee (deg)
        self.label_wC = tk.Label(master, text=self.txt_wC )
        self.label_wC.grid(row=7, column=0, padx=40, pady=2, sticky='w')
        self.entry_wC = tk.Entry(master, width=10, textvariable=self.var_wC)
        self.entry_wC.grid(row=7, column=1, padx=5, pady=2, sticky='w')
        self.errtx_wC = tk.Label(master, text='', fg='red' )
        self.errtx_wC.grid(row=7, column=3, padx=5, pady=2, sticky='w')
        
        # Input the Chief Right Ascension (deg)
        self.label_RC = tk.Label(master, text=self.txt_RC )
        self.label_RC.grid(row=8, column=0, padx=40, pady=2, sticky='w')
        self.entry_RC = tk.Entry(master, width=10, textvariable=self.var_RC)
        self.entry_RC.grid(row=8, column=1, padx=5, pady=2, sticky='w')
        self.errtx_RC = tk.Label(master, text='', fg='red' )
        self.errtx_RC.grid(row=8, column=3, padx=5, pady=2, sticky='w')
        
        # Input the Chief Mean Anomaly (deg)
        self.label_MC = tk.Label(master, text=self.txt_MC )
        self.label_MC.grid(row=9, column=0, padx=40, pady=2, sticky='w')
        self.entry_MC = tk.Entry(master, width=10, textvariable=self.var_MC)
        self.entry_MC.grid(row=9, column=1, padx=5, pady=2, sticky='w')
        self.errtx_MC = tk.Label(master, text='', fg='red' )
        self.errtx_MC.grid(row=9, column=3, padx=5, pady=2, sticky='w')
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###    Create input text boxes for formation RIC requirements     ###
        ###    Note that I = 2R geometry must be enforced before RUN!     ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        # Title for the Deputy RIC Formation Geometry Requirements
        self.label_headerD = tk.Label(master, text=self.txt_headerD,
                                      font=('Helvetica',9,'bold'))
        self.label_headerD.grid(row=10, column=0, padx=40, pady=10, sticky='w')
        
        #####################################################################
        #####################################################################
        
        # Input the Formation Radial Separation (km).
        self.label_fR = tk.Label(master, text=self.txt_fR )
        self.label_fR.grid(row=11, column=0, padx=40, pady=2, sticky='w')
        self.entry_fR = tk.Entry(master, width=10, textvariable=self.var_fR)
        self.entry_fR.grid(row=11, column=1, padx=5, pady=2, sticky='w')
        self.scale_fR = tk.Scale(master, from_=0, to=1000, length=100,
                                 orient=tk.HORIZONTAL, showvalue=0,
                                 variable=self.var_fR)
        self.scale_fR.grid(row=11, column=2, padx=5, pady=2, sticky='w')
        self.errtx_fR = tk.Label(master, text='', fg='red' )
        self.errtx_fR.grid(row=11, column=3, padx=5, pady=2, sticky='w')
        
        #####################################################################
        #####################################################################
        
        # Input the Formation In-Track Separation (km).
        self.label_fI = tk.Label(master, text=self.txt_fI )
        self.label_fI.grid(row=12, column=0, padx=40, pady=2, sticky='w')
        self.entry_fI = tk.Entry(master, width=10, textvariable=self.var_fI)
        self.entry_fI.grid(row=12, column=1, padx=5, pady=2, sticky='w')
        self.scale_fI = tk.Scale(master, from_=0, to=2000, length=100,
                                 orient=tk.HORIZONTAL, showvalue=0,
                                 variable=self.var_fI)
        self.scale_fI.grid(row=12, column=2, padx=5, pady=2, sticky='w')
        self.errtx_fI = tk.Label(master, text='', fg='red' )
        self.errtx_fI.grid(row=12, column=3, padx=5, pady=2, sticky='w')
        
        # Input the Formation In-Track Offset (km).
        self.label_fO = tk.Label(master, text=self.txt_fO )
        self.label_fO.grid(row=13, column=0, padx=40, pady=2, sticky='w')
        self.entry_fO = tk.Entry(master, width=10, textvariable=self.var_fO)
        self.entry_fO.grid(row=13, column=1, padx=5, pady=2, sticky='w')
        self.scale_fO = tk.Scale(master, from_=-1000, to=1000, length=100,
                                 orient=tk.HORIZONTAL, showvalue=0,
                                 variable=self.var_fO)
        self.scale_fO.grid(row=13, column=2, padx=5, pady=2, sticky='w')
        self.errtx_fO = tk.Label(master, text='', fg='red' )
        self.errtx_fO.grid(row=13, column=3, padx=5, pady=2, sticky='w')
        
        #####################################################################
        #####################################################################
        
        # Input the Formation Cross-Track Separation (km).
        self.label_fC = tk.Label(master, text=self.txt_fC )
        self.label_fC.grid(row=14, column=0, padx=40, pady=2, sticky='w')
        self.entry_fC = tk.Entry(master, width=10, textvariable=self.var_fC)
        self.entry_fC.grid(row=14, column=1, padx=5, pady=2, sticky='w')
        
        self.scale_fC = tk.Scale(master, from_=0, to=2000, length=100,
                                 orient=tk.HORIZONTAL, showvalue=0,
                                 variable=self.var_fC)
        self.scale_fC.grid(row=14, column=2, padx=5, pady=2, sticky='w')
        self.errtx_fC = tk.Label(master, text='', fg='red' )
        self.errtx_fC.grid(row=14, column=3, padx=5, pady=2, sticky='w')
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###        Define a call-back function that reinforces            ###
        ###        the I = 2R formation geometry relationship.            ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        # Bind variable _fR so that the I = 2R relationship holds.
        
        def callback_R(self):
            try:
                _fR = self.var_fR.get()
                self.var_fI.set( _fR * 2.0 )
            except:
                pass
            finally:
                return None
        
        self.var_fR.trace("w", lambda name, index, mode,
                          var=self: callback_R(self))
        
        #####################################################################
        #####################################################################
        
        # Bind variable _fI so that the I = 2R relationship holds.
        
        def callback_I(self):
            try:
                _fI = self.var_fI.get()
                self.var_fR.set( _fI * 0.5 )
            except:
                pass
            finally:
                return None
        
        self.var_fI.trace("w", lambda name, index, mode,
                          var=self: callback_I(self))
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###  Create input text boxes for chief satellite orbit elements   ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        # Title for the Deputy Formation Plane Angle Parameters
        self.label_headerP = tk.Label(master, text=self.txt_headerP,
                                      font=('Helvetica',9,'bold'))
        self.label_headerP.grid(row=15, column=0, padx=40, pady=10, sticky='w')
        
        # Input the Formation Argument of Relative Pericenter (deg).
        self.label_fPhi = tk.Label(master, text=self.txt_fPhi )
        self.label_fPhi.grid(row=16, column=0, padx=40, pady=2, sticky='w')
        self.entry_fPhi = tk.Entry(master,width=10,textvariable=self.var_fPhi)
        self.entry_fPhi.grid(row=16, column=1, padx=5, pady=2, sticky='w')
        self.scale_fPhi = tk.Scale(master, from_=-180, to=180, length=100,
                                   orient=tk.HORIZONTAL, showvalue=0,
                                   variable=self.var_fPhi)
        self.scale_fPhi.grid(row=16, column=2, padx=5, pady=2, sticky='w')
        self.errtx_fPhi = tk.Label(master, text='', fg='red' )
        self.errtx_fPhi.grid(row=16, column=3, padx=5, pady=2, sticky='w')
        
        #####################################################################
        #####################################################################
        
        # Input the Formation Argument of Latitude Crossing (deg).
        self.label_fTht = tk.Label(master, text=self.txt_fTht )
        self.label_fTht.grid(row=17, column=0, padx=40, pady=2, sticky='w')
        self.entry_fTht = tk.Entry(master,width=10,textvariable=self.var_fTht)
        self.entry_fTht.grid(row=17, column=1, padx=5, pady=2, sticky='w')
        self.scale_fTht = tk.Scale(master, from_=-180, to=180, length=100,
                                   orient=tk.HORIZONTAL, showvalue=0,
                                   variable=self.var_fTht)
        self.scale_fTht.grid(row=17, column=2, padx=5, pady=2, sticky='w')
        self.errtx_fTht = tk.Label(master, text='', fg='red' )
        self.errtx_fTht.grid(row=17, column=3, padx=5, pady=2, sticky='w')
        
        #####################################################################
        #####################################################################
        
        # Add a foot note to inform the user about the I=2R geometry relation.
        footer = 'Note: In-track = 2x Radial Separation by HCW Equations'
        self.footnote = tk.Label(master, text=footer, fg = '#888888',
                                 font=('Helvetica',8,'italic'))
        self.footnote.grid(row=18, column=0, padx=40, pady=40,
                           columnspan=3, sticky='w')
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###              Configure the plot area in the GUI               ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        # Now, we add a sub-frame in the tkinter GUI so that we can embed the
        # the interactive matplotlib 3D plot of the relative orbit.
        self.toolbarFrame = tk.Frame(master)
        self.toolbarFrame.grid(row=1, column=4, padx=20, pady=10,
                               columnspan=5, rowspan=20)
        
        # Create the 3D axes matplotlib figure object, using the pack() method
        # of tkinter within the toolbarFrame object.
        self.orbFig = Figure(figsize=(7,6), dpi=100,
                             linewidth=8, edgecolor="#DDDDDD")
        self.orbFig.set_tight_layout(True)
        self.orbPlot = FigureCanvasTkAgg(self.orbFig, self.toolbarFrame)
        self.orbPlot.get_tk_widget().pack(expand=True)
        
        # Note, the plotting should happen after the figure object is called.
        self.orbAxis = self.orbFig.add_subplot(projection='3d')
        self.orbAxis.set_xlabel('Hill Frame Cross-Track Axis (km)')
        self.orbAxis.set_ylabel('Hill Frame In-Track Axis (km)')
        self.orbAxis.set_zlabel('Hill Frame Radial Axis (km)')
        
        # At this point, you can insert plots if you want. For example,
        # self.orbAxis.scatter([1,2,3],[1,2,3],[1,2,3])
        
        self.orbPlot.draw()
        
        # Add the matplotlib navigation toolbar.
        self.toolbar = NavigationToolbar2Tk(self.orbPlot, self.toolbarFrame)
        self.toolbar.update()
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###    Finally, define string containers for error and warning    ###
        ###    messages to inform the user if input conditions violate    ###
        ###               formatting or physical principles.              ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        self.error_msgprint = '' # Error message to print
    
    #########################################################################
    #########################################################################
    ###                                                                   ###
    ###          Method to load default values from config.txt            ###
    ###                                                                   ###
    #########################################################################
    #########################################################################
    
    def cfg_R(self):
        
        '''
        Method to read the config.txt file:
        -----------------------------------
        1) First, this method checks that all inputs in config.txt are correct
        2) Second, it copies the input parameters into the GUI's variables
        '''
        
        cwd = dirname(dirname(abspath(__file__))) # Current working directory
        iwd = join(cwd, 'config', 'config.txt') # Inputs files
        inputfile = open(iwd,'r') # Open the config.txt file
        inps = {} # Create a dictionary to store all the input 
        integers = ['duration', 'timestep']
        floats = ['orb_a',  'orb_e',  'orb_i',  'orb_w',  'orb_R',  'orb_M',
                  'form_R', 'form_I', 'form_O', 'form_C',
                  'form_phi', 'form_tht']
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###   Parsing through the config.txt file to extract parameters   ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        # Now we parse through the config.txt file.
        for line in inputfile:
            
            # Check for input entry with an 'I', then split and format.
            if line[0] == 'I':
                line_inp = line[3:].split()
                
                # Now, let's try to parse parameters meant to be integers.
                if line_inp[0] in integers:
                    
                    try:
                        inps[ line_inp[0] ] = int(line_inp[1])
                    except ValueError:
                        errmsg = 'Error, expected an integer when reading '
                        errmsg = errmsg + line_inp[0] + ' in config.txt! \n'
                        print(errmsg)
                        self.error_msgprint += errmsg
                        inps[ line_inp[0] ] = 0
                
                # then we parse parameters meant to be floats.
                elif line_inp[0] in floats:
                    
                    try:
                        inps[ line_inp[0] ] = float(line_inp[1])
                    except ValueError:
                        errmsg = 'Error, expected a float when reading '
                        errmsg = errmsg + line_inp[0] + ' in config.txt! \n'
                        print(errmsg)
                        self.error_msgprint += errmsg
                        inps[ line_inp[0] ] = 0.0
                        
                # For all other parameters, just log them down as they are.
                else:
                    inps[ line_inp[0] ] = line_inp[1]
        
        # Close the file when done
        inputfile.close()
        
        #####################################################################
        #####################################################################
        ###                                                               ###
        ###   Parsing through the config.txt file to extract parameters   ###
        ###                                                               ###
        #####################################################################
        #####################################################################
        
        # 0. Check for timing parameters in scenario
        
        self.var_td.set(inps['duration'])
        if inps['duration'] <= 0:
            errmsg = 'Scenario duration cannot be zero or negative! \n'
            self.errtx_td.configure(text='Error!')
        elif inps['duration'] > 31536000:
            errmsg = 'Scenario duration cannot be longer than a year! \n'
            self.errtx_td.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_td.configure(text='')
        self.error_msgprint += errmsg
        
        self.var_ts.set(inps['timestep'])
        if inps['timestep'] <= 0:
            errmsg = 'Scenario step size cannot be zero or negative! \n'
            self.errtx_ts.configure(text='Error!')
        elif inps['timestep'] > inps['duration']:
            errmsg = 'Scenario step cannot be larger than the duration! \n'
            self.errtx_ts.configure(text='Error!')
        elif inps['timestep'] > 31536000:
            errmsg = 'Scenario step size cannot be longer than a year! \n'
            self.errtx_ts.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_ts.configure(text='')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 1. Check for chief satellite semi-major axis
        
        self.var_aC.set(inps['orb_a'])
        if inps['orb_a'] < 6378.14:
            errmsg = 'Semi-major axis below Earth surface! \n'
            self.errtx_aC.configure(text='Error!')
        elif inps['orb_a'] > 385000.0:
            errmsg = 'Semi-major axis beyond Earth orbit! \n'
            self.errtx_aC.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_aC.configure(text='')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 2. Check for chief satellite eccentricity
        
        self.var_eC.set(inps['orb_e'])
        if inps['orb_e'] < 0:
            errmsg = 'Eccentricity cannot be < 0! \n'
            self.errtx_eC.configure(text='Error!')
        elif inps['orb_e'] >= 1.0:
            errmsg = 'Eccentricity cannot be >= 1! \n'
            self.errtx_eC.configure(text='Error!')
        elif ( ( 1 - inps['orb_e'] ) * inps['orb_a'] ) < 6378.14:
            errmsg = 'Perigee altitude below Earth surface! \n'
            self.errtx_eC.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_eC.configure(text='')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 3. Check for chief satellite inclination angle
        
        self.var_iC.set(inps['orb_i'])
        if inps['orb_i'] < -180.0 or inps['orb_i'] > 180.0:
            errmsg = 'Inclination angle must be between +/- 180! \n'
            self.errtx_iC.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_iC.configure(text='')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 4. Check for chief satellite argument of perigee.
        
        self.var_wC.set(inps['orb_w'])
        if inps['orb_w'] < -180.0 or inps['orb_w'] > 180.0:
            errmsg = 'Argument of Perigee must be between +/- 180! \n'
            self.errtx_wC.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_wC.configure(text='')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 5. Check for chief satellite right ascensions of ascending node.
        
        self.var_RC.set(inps['orb_R'])
        if inps['orb_R'] < -180.0 or inps['orb_R'] > 180.0:
            errmsg = 'Right ascension must be between +/- 180! \n'
            self.errtx_RC.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_RC.configure(text='')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 6. Check for chief satellite mean anomaly.
        
        self.var_MC.set(inps['orb_M'])
        if inps['orb_M'] < -180.0 or inps['orb_M'] > 180.0:
            errmsg = 'Mean anomaly must be between +/- 180! \n'
            self.errtx_MC.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_MC.configure(text='')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 7. Check for deputy radial separation (km).
        
        self.var_fR.set(inps['form_R'])
        if inps['form_R'] < 0:
            errmsg = 'Radial separation cannot be negative! \n'
            self.errtx_fR.configure(text='Error!')
        elif inps['form_R'] > 1000.0:
            errmsg = 'Radial separation cannot exceed 1000 km! \n'
            self.errtx_fR.configure(text='Error!')
        else:
            if inps['form_R'] * 2 == inps['form_I']:
                errmsg = ''
                self.errtx_fR.configure(text='')
            else:
                errmsg = 'Radial separation must be half of in-track! \n'
                self.errtx_fR.configure(text='Warning!')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 8. Check for deputy in-track separation (km).
        
        self.var_fI.set(inps['form_I'])
        if inps['form_I'] < 0:
            errmsg = 'In-track separation cannot be negative! \n'
            self.errtx_fI.configure(text='Error!')
        elif inps['form_I'] > 2000.0:
            errmsg = 'In-track separation cannot exceed 2000 km! \n'
            self.errtx_fI.configure(text='Error!')
        else:
            if inps['form_R'] * 2 == inps['form_I']:
                errmsg = ''
                self.errtx_fI.configure(text='')
            else:
                errmsg = 'In-track separation must be twice of radial! \n'
                self.errtx_fI.configure(text='Warning!')
        self.error_msgprint += errmsg
        
        self.var_fO.set(inps['form_O'])
        if inps['form_O'] < -1000.0:
            errmsg = 'In-track offset cannot be < -1000 km! \n'
            self.errtx_fO.configure(text='Error!')
        elif inps['form_O'] > 1000.0:
            errmsg = 'In-track offset cannot be > 1000 km! \n'
            self.errtx_fO.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_fO.configure(text='')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 9. Check for deputy cross-track separation (km).
        
        self.var_fC.set(inps['form_C'])
        if inps['form_C'] < 0:
            errmsg = 'Cross-track separation cannot be negative! \n'
            self.errtx_fC.configure(text='Error!')
        elif inps['form_C'] > 2000.0:
            errmsg = 'Cross-track separation cannot exceed 2000 km! \n'
            self.errtx_fC.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_fC.configure(text='')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 10. Check for Argument of Relative Pericenter (deg)
        
        self.var_fPhi.set(inps['form_phi'])
        if inps['form_phi'] < -180.0 or inps['form_phi'] > 180.0:
            errmsg = 'Relative Pericenter must be between +/- 180! \n'
            self.errtx_fPhi.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_fPhi.configure(text='')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 11. Check for Argument of Latitude Crossing (deg)
        
        self.var_fTht.set(inps['form_tht'])
        if inps['form_tht'] < -180.0 or inps['form_tht'] > 180.0:
            errmsg = 'Latitude Crossing must be between +/- 180! \n'
            self.errtx_fTht.configure(text='Error!')
        else:
            errmsg = ''
            self.errtx_fTht.configure(text='')
        self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # Finally, display an error textbox if there are any error messages.
        
        if len(self.error_msgprint) > 0:
            tk.messagebox.showerror("Error with Configuration File!",
                                    self.error_msgprint)
            self.error_msgprint = '' # Reset error message
        
        return None
    
    #########################################################################
    #########################################################################
    ###                                                                   ###
    ###     Method for writing the entries into the config.txt file.      ###
    ###                                                                   ###
    #########################################################################
    #########################################################################
    
    def cfg_W(self):
        
        '''
        Method to write the config.txt file:
        -----------------------------------
        1) First, this method checks that all inputs in the GUI are correct
        2) Second, it copies the GUI parameters into the config.txt file
        '''
        
        # Reset the GUI error message variable.
        self.error_msgprint = ''
        
        # Get the directory paths.
        cwd = dirname(dirname(abspath(__file__))) # Current working directory
        iwd = join(cwd, 'config', 'config.txt') # Inputs files
        input_r = open(iwd,'r') # Open the config.txt file
        record = [] # Array to record the strings
        
        # Variables to be recorded based on tkinter entries.
        var_arr = [self.var_td, self.var_ts,
                   self.var_aC, self.var_eC, self.var_iC,
                   self.var_wC, self.var_RC, self.var_MC,
                   self.var_fR, self.var_fI, self.var_fO, self.var_fC,
                   self.var_fPhi, self.var_fTht]
        
        # Key values (to be referred).
        key_arr = ['duration','timestep',
                   'orb_a', 'orb_e', 'orb_i', 'orb_w', 'orb_R', 'orb_M', 
                   'form_R', 'form_I', 'form_O', 'form_C',
                   'form_phi', 'form_tht']
        
        #####################################################################
        #####################################################################
        
        # 0. Check for timing parameters in scenario
        
        try:
            _td = self.var_td.get() # Exception raised if entry is erroneous
            if _td <= 0:
                errmsg = 'Scenario duration cannot be zero or negative! \n'
                self.errtx_td.configure(text='Error!')
            elif _td > 31536000:
                errmsg = 'Scenario duration cannot be longer than a year! \n'
                self.errtx_td.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_td.configure(text='')
        except:
            _td = 86400
            self.var_td.set(86400) # Reset to default 86400s (1 day)
            errmsg = 'Error! Expected an integer for scenario duration (s)! \n'
        finally:
            self.error_msgprint += errmsg
            
        try:
            _ts = self.var_ts.get() # Exception raised if entry is erroneous
            if _ts <= 0:
                errmsg = 'Scenario step size cannot be zero or negative! \n'
                self.errtx_ts.configure(text='Error!')
            elif _ts > _td:
                errmsg = 'Scenario step cannot be larger than the duration! \n'
                self.errtx_ts.configure(text='Error!')
            elif _ts > 31536000:
                errmsg = 'Scenario step size cannot be longer than a year! \n'
                self.errtx_ts.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_ts.configure(text='')
        except:
            _ts = 1
            self.var_ts.set(1) # Reset to default 86400s (1 day)
            errmsg = 'Error! Expected an integer for scenario step size (s)! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 1. Check for chief satellite semi-major axis
        try:
            _aC = self.var_aC.get() # Exception raised if entry is erroneous
            if _aC < 6378.14:
                errmsg = 'Semi-major axis below Earth surface! \n'
                self.errtx_aC.configure(text='Error!')
            elif _aC > 385000.0:
                errmsg = 'Semi-major axis beyond Earth orbit! \n'
                self.errtx_aC.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_aC.configure(text='')
        except:
            _aC = 0.0
            self.var_aC.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for Semi-Major Axis (km)! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 2. Check for chief satellite eccentricity
        try:
            _eC = self.var_eC.get() # Exception raised if entry is erroneous
            if _eC < 0:
                errmsg = 'Eccentricity cannot be < 0! \n'
                self.errtx_eC.configure(text='Error!')
            elif _eC >= 1.0:
                errmsg = 'Eccentricity cannot be >= 1! \n'
                self.errtx_eC.configure(text='Error!')
            elif ( ( 1 - _eC ) * _aC ) < 6378.14:
                errmsg = 'Perigee altitude below Earth surface! \n'
                self.errtx_eC.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_eC.configure(text='')
        except:
            self.var_eC.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for the eccentricity! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 3. Check for chief satellite inclination angle
        try:
            _iC = self.var_iC.get() # Exception raised if entry is erroneous
            if _iC < -180.0 or _iC > 180.0:
                errmsg = 'Inclination angle must be between +/- 180! \n'
                self.errtx_iC.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_iC.configure(text='')
        except:
            self.var_iC.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for the inclination! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 4. Check for chief satellite argument of perigee.
        try:
            _wC = self.var_wC.get() # Exception raised if entry is erroneous
            if _wC < -180.0 or _wC > 180.0:
                errmsg = 'Argument of Perigee must be between +/- 180! \n'
                self.errtx_wC.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_wC.configure(text='')
        except:
            self.var_wC.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for the argument of perigee! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 5. Check for chief satellite right ascensions of ascending node.
        try:
            _RC = self.var_RC.get() # Exception raised if entry is erroneous
            if _RC < -180.0 or _RC > 180.0:
                errmsg = 'Right ascension must be between +/- 180! \n'
                self.errtx_RC.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_RC.configure(text='')
        except:
            self.var_RC.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for the right ascension! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 6. Check for chief satellite mean anomaly.
        try:
            _MC = self.var_MC.get() # Exception raised if entry is erroneous
            if _MC < -180.0 or _MC > 180.0:
                errmsg = 'Mean anomaly must be between +/- 180! \n'
                self.errtx_MC.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_MC.configure(text='')
        except:
            self.var_MC.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for the mean anomaly! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 7. Check for deputy radial / in-track separation (km).
        try:
            _fR = self.var_fR.get() # Exception raised if entry is erroneous
            _fI = self.var_fI.get() # Exception raised if entry is erroneous
            if _fR < 0.0:
                errmsg = 'Radial separation cannot be negative! \n'
                self.errtx_fR.configure(text='Error!')
            elif _fR > 1000.0:
                errmsg = 'Radial separation cannot exceed 1000 km! \n'
                self.errtx_fR.configure(text='Error!')
            else:
                if _fR * 2 == _fI:
                    errmsg = ''
                    self.errtx_fR.configure(text='')
                else:
                    errmsg = 'Radial separation must be half of in-track! \n'
                    errmsg += 'Radial separation reset to half of in-track! \n'
                    self.errtx_fR.configure(text='Warning!')
                    self.var_fR.set( 0.5 * _fI )
                    self.errtx_fR.configure(text='')
        except:
            self.var_fR.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for the radial separation! \n'
            errmsg += 'Error! Expected a float for the in-track separation! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 8. Check for deputy in-track separation only (km).
        try:
            _fI = self.var_fI.get() # Exception raised if entry is erroneous
            if _fI < 0.0:
                errmsg = 'In-track separation cannot be negative! \n'
                self.errtx_fI.configure(text='Error!')
            elif _fI > 2000.0:
                errmsg = 'In-track separation cannot exceed 2000 km! \n'
                self.errtx_fI.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_fI.configure(text='')
        except:
            self.var_fI.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for the in-track separation! \n'
        finally:
            self.error_msgprint += errmsg
            
        try:
            _fO = self.var_fO.get() # Exception raised if entry is erroneous
            if _fO < -1000.0:
                errmsg = 'In-track offset cannot be < -1000 km! \n'
                self.errtx_fO.configure(text='Error!')
            elif _fO > 1000.0:
                errmsg = 'In-track offset cannot be > 1000 km! \n'
                self.errtx_fO.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_fO.configure(text='')
        except:
            self.var_fO.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for the in-track offset! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 9. Check for deputy cross-track separation (km).
        try:
            _fC = self.var_fC.get() # Exception raised if entry is erroneous
            if _fC < 0.0:
                errmsg = 'Cross-track separation cannot be negative! \n'
                self.errtx_fC.configure(text='Error!')
            elif _fC > 2000.0:
                errmsg = 'Cross-track separation cannot exceed 2000 km! \n'
                self.errtx_fC.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_fC.configure(text='')
        except:
            self.var_fC.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for cross-track separation! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 10. Check for Argument of Relative Pericenter (deg)
        try:
            _fPhi = self.var_fPhi.get() # Exception raised if entry is erroneous
            if _fPhi < -180.0 or _fPhi > 180.0:
                errmsg = 'Relative pericenter must be between +/- 180! \n'
                self.errtx_fPhi.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_fPhi.configure(text='')
        except:
            self.var_fPhi.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for the relative pericenter! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # 11. Check for Argument of Latitude Crossing (deg)
        try:
            _fTht = self.var_fTht.get() # Exception raised if entry is erroneous
            if _fTht < -180.0 or _fTht > 180.0:
                errmsg = 'Latitude crossing must be between +/- 180! \n'
                self.errtx_fTht.configure(text='Error!')
            else:
                errmsg = ''
                self.errtx_fTht.configure(text='')
        except:
            self.var_fTht.set(0.0) # Reset to default 0.0
            errmsg = 'Error! Expected a float for the latitude crossing! \n'
        finally:
            self.error_msgprint += errmsg
        
        #####################################################################
        #####################################################################
        
        # Finally, display an error textbox if there are any error messages.
        if len(self.error_msgprint) > 0:
            tk.messagebox.showerror("Error with Configuration File!",
                                    self.error_msgprint)
            self.error_msgprint = '' # Reset error message
            return None
        
        # Else, if all the inputs are good, begin over-writing config.txt.
        else:
            
            # Now we parse through the config.txt file.
            for line in input_r:
                
                if line[0] == 'I':
                    words = line.split() # Split string into list of words.
                    key   = words[1] # Get the key from config.txt
                    value = words[2] # Get the value from config.txt
                    
                    # Get the updated value based on the index from key list.
                    value_new = str(var_arr[ key_arr.index(key) ].get())
                    line_new  = line.replace(value, value_new)
                
                else:
                    line_new = line
                
                # Now, record the entries.
                record.append(line_new)
            
            # Close the file when done
            input_r.close()
            
            # Now, we open and overwrite the config.txt file.
            input_w = open(iwd,'w') # Open the config.txt file
            
            for text in record:
                input_w.write(text)
            
            input_w.close()
            return None
    
    #########################################################################
    #########################################################################
    ###                                                                   ###
    ###     Save all config inputs, and runs the main QLUSTER program.    ###
    ###                                                                   ###
    #########################################################################
    #########################################################################
    
    def run(self):
        
        '''
        Saves all current config inputs, and runs the main QLUSTER program.
        '''
        
        try:
            
            # Save the current inputs first.
            self.cfg_W()
            
            # Fetch the scenario time parameters.
            td = self.var_td.get()
            ts = self.var_ts.get()
            
            # Fetch the chief satellite orbit elements.
            aC = self.var_aC.get()
            eC = self.var_eC.get()
            iC = self.var_iC.get()
            wC = self.var_wC.get()
            RC = self.var_RC.get()
            MC = self.var_MC.get()
            
            # Fetch the formation geometry requirements.
            fR = self.var_fR.get()
            fI = self.var_fI.get()
            fO = self.var_fO.get()
            fC = self.var_fC.get()
            
            # Fetch the formation plane angle parameters.
            fPhi = self.var_fPhi.get()
            fTht = self.var_fTht.get()
            
            # Solve for the deputy satellite orbit elements.
            aD, eD, iD, wD, RD, MD = deputy.deputy(td, ts,
                                                   aC, eC, iC,
                                                   wC, RC, MC,
                                                   fR, fI, fO, fC,
                                                   fPhi, fTht)
            
            print('Deputy: ', aD, eD, iD, wD, RD, MD)
            print('Chief: ', aC, eC, iC, wC, RC, MC, '\n')
            
            # Perform the relative orbit propagation.
            rpx, rpy, rpz, rvx, rvy, rvz = relative.propagate(td, ts,
                                                              aC, eC, iC,
                                                              wC, RC, MC,
                                                              aD, eD, iD,
                                                              wD, RD, MD)
            
            # Plot the results in the GUI.           
            self.orbAxis.plot( rpz, # Cross-Track
                               rpy, # In-Track
                               rpx, # Radial Axis
                               label='Relative Orbit in Hill-Frame')
            
            # Update the plots
            self.orbPlot.draw()
            
            # Get the current axes limits on relative orbit plots.
            axOrbR_axes_limits = [abs(self.orbAxis.get_xlim()[0]),
                                  abs(self.orbAxis.get_xlim()[1]),
                                  abs(self.orbAxis.get_ylim()[0]),
                                  abs(self.orbAxis.get_ylim()[1]),
                                  abs(self.orbAxis.get_zlim()[0]),
                                  abs(self.orbAxis.get_zlim()[1])]
            
            # Using axOrbR_axes_limits above, we can find the minimum and
            # maximum axes limits and the span of values.
            axOrbR_axes_max  = max(axOrbR_axes_limits)
            axOrbR_axes_span = axOrbR_axes_max * 2

            # Scale all axes equally for relative orbit plots
            self.orbAxis.set_xlim( -1 * axOrbR_axes_max, axOrbR_axes_max )
            self.orbAxis.set_ylim( -1 * axOrbR_axes_max, axOrbR_axes_max )
            self.orbAxis.set_zlim( -1 * axOrbR_axes_max, axOrbR_axes_max )
            
            # It is important that the XYZ axes in the VVLH (relative 
            # orbit) frame is scaled the same, else it is difficult to 
            # interpret the relative separations on different scales.
            
            # Plot the chief satellite as a tri-axial quiver in VVLH frame.
            axOrbR0 = axOrbR_axes_span * 0.1
            self.orbAxis.quiver( 0,0,0,1,0,0, length = axOrbR0,
                                color = 'r', arrow_length_ratio=0.3 )
            self.orbAxis.quiver( 0,0,0,0,1,0, length = axOrbR0,
                                color = 'r', arrow_length_ratio=0.3 )
            self.orbAxis.quiver( 0,0,0,0,0,1, length = axOrbR0,
                                color = 'r', arrow_length_ratio=0.3 )
            
            # Update the plots
            self.orbPlot.draw()
            
        except Exception as excpt:
            print('Error in running!')
            print(excpt)
            pass
        
        return None
    
    #########################################################################
    #########################################################################
    ###                                                                   ###
    ###     Logs the ephemeris into a CSV file after running QLUSTER.     ###
    ###                                                                   ###
    #########################################################################
    #########################################################################
    
    def log(self):
        
        '''
        Logs the ephemeris into a CSV file after running the QLUSTER program.
        '''
        
        return None
    
    #########################################################################
    #########################################################################
    ###                                                                   ###
    ###    Clears all existing relative orbit plots in the QLUSTER GUI.   ###
    ###                                                                   ###
    #########################################################################
    #########################################################################
    
    def clr(self):
        
        '''
        Clears all existing relative orbit plots in the QLUSTER GUI.
        '''
        
        self.orbAxis.clear()
        self.orbPlot.draw()
        
        return None
