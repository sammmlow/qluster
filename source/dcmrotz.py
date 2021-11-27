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
##    Direction Cosine Matrix for Z-Axis Rotation                            ##
##                                                                           ##
##    Written by Samuel Y. W. Low.                                           ##
##    First created 20-May-2021 12:50 PM (+8 GMT)                            ##
##    Last modified 20-May-2021 12:50 PM (+8 GMT)                            ##
##                                                                           ##
###############################################################################
###############################################################################

import numpy as np

def dcmZ(t):
    '''Generate the direction cosine matrix for an Z-axis rotation of angle t.
    
    Parameters
    ----------
    t : float
        Angle theta (t) is the scalar angle (in radians).

    Returns
    -------
    dcm : numpy.ndarray
        Numpy 3x3 direction cosine matrix.
    
    '''
    
    dcm = np.array([[    np.cos(t), np.sin(t), 0.0 ],
                    [ -1*np.sin(t), np.cos(t), 0.0 ],
                    [    0.0,       0.0,       1.0 ]])
    
    return dcm