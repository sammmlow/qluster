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
##    Iterative solver for eccentric anomaly using Kepler's Equation         ##
##                                                                           ##
##    Written by Samuel Y. W. Low.                                           ##
##    First created 20-May-2021 14:57 PM (+8 GMT)                            ##
##    Last modified 20-May-2021 14:57 PM (+8 GMT)                            ##
##                                                                           ##
###############################################################################
###############################################################################

import numpy as np

def solve(M, ecc):
    
    '''
    Input mean anomaly (float rad) and eccentricity (dimensionless).
    Outputs the eccentric anomaly (float rad).
    '''
    
    E1 = M         # Initialise eccentric anomaly
    e = ecc        # Initialise the float eccentricity
    residual = 1.0 # Initialise convergence residual
    
    while residual >= 0.000001:
        
        fn = E1 - (e*np.sin(E1)) - M
        fd = 1 - (e*np.cos(E1))
        E2 = E1 - (fn/fd)
        residual = abs(E2-E1) # Compute residual
        E1 = E2 # Update the eccentric anomaly
        
    return E2