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
##    This file contains all the anomaly conversion scripts, from the mean   ##
##    anomaly to the true anomaly and vice versa.                            ##
##                                                                           ##
##    Written by Samuel Y. W. Low.                                           ##
##    First created 20-May-2021 10:17 PM (+8 GMT)                            ##
##    Last modified 20-May-2021 10:17 PM (+8 GMT)                            ##
##                                                                           ##
###############################################################################
###############################################################################

import numpy as np
from source import kepler

# Mean anomaly to eccentric anomaly conversion.
def M2E(M,e):
    
    '''
    Convert mean anomaly (rad) into eccentric anomaly (rad).
    
    Inputs: Mean anomaly and eccentricity
    - M -> Mean anomaly (rad)
    - e -> Eccentricity (dimensionless)
    
    Returns: Eccentric anomaly (rad)
    '''
    
    return kepler.solve(M,e)

# Mean anomaly to true anomaly conversion.
def M2V(M,e):
    
    '''
    Convert mean anomaly (rad) into true anomaly (rad)
    
    Inputs: Mean anomaly and eccentricity
    - M -> Mean Anomaly (rad)
    - e -> Eccentricity (dimensionless)
    
    Returns: True anomaly (rad)
    '''
    
    # First, let us solve for the eccentric anomaly.
    eccAnom = kepler.solve(M,e)
    
    # With the eccentric anomaly, we can solve for position and velocity
    # in the local orbital frame, using the polar equation for an ellipse.
    pos_X = np.cos(eccAnom) - e
    pos_Y = np.sqrt( 1 - e**2 ) * np.sin(eccAnom)
    
    # Finally, let us not forget to compute the true anomaly.
    nu = np.arctan2( pos_Y, pos_X ) 
    
    # Position vector 1x3 (km), velocity vetor 1x3 (km/s), true anomaly (rad)
    return nu

# True anomaly to eccentric anomaly conversion.
def V2E(nu,e):
    
    '''
    Convert true anomaly (rad) into eccentric anomaly (rad)
    
    Inputs: True anomaly, eccentricity
    - nu -> True Anomaly (rad)
    - e  -> Eccentricity (dimensionless)
    
    Returns: Eccentric anomaly (rad)
    '''
    
    E = 2 * np.arctan( np.sqrt( ( 1 - e ) / ( 1 + e ) ) * np.tan( nu / 2 ) )
    return E

# Eccentric anomaly to mean anomaly conversion.
def E2M(E,e):
    
    '''
    Convert eccentric anomaly (rad) into mean anomaly (rad)
    Note this uses the original Keplers equation M = E - e \sin{E}
    
    Inputs: True anomaly, eccentricity
    - E -> Eccentric Anomaly (rad)
    - e -> Eccentricity (dimensionless)
    
    Returns: Mean anomaly (rad)
    '''
    
    M = E - e * np.sin(E)
    return M

# True anomaly to mean anomaly conversion.
def V2M(nu,e):
    
    '''
    Convert true anomaly (rad) into mean anomaly (rad)
    Note this uses the V2E and E2M function as an intermediary
    
    Inputs: True anomaly, eccentricity
    - E -> Eccentric Anomaly (rad)
    - e -> Eccentricity (dimensionless)
    
    Returns: Mean anomaly (rad)
    '''
    
    return E2M( V2E(nu,e), e )
