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

###############################################################################
###############################################################################

def M2E(M,e):
    '''Mean anomaly to eccentric anomaly conversion via Keplers Equation (rad).
    
    Parameters
    ----------
    M : float
        Mean Anomaly (rad)
    e : float
        Eccentricity (unit-less)
    
    Returns
    -------
    E2 : float
        Eccentric anomaly (rad)
    
    '''
    
    E1 = M         # Initialise eccentric anomaly
    ei = e         # Initialise the float eccentricity
    residual = 1.0 # Initialise convergence residual
    
    while residual >= 0.000001:
        
        fn = E1 - (ei*np.sin(E1)) - M
        fd = 1 - (ei*np.cos(E1))
        E2 = E1 - (fn/fd)
        residual = abs(E2-E1) # Compute residual
        E1 = E2 # Update the eccentric anomaly
        
    return E2

###############################################################################
###############################################################################

def M2V(M,e):
    '''Mean anomaly to true anomaly conversion via Keplers Equation (rad).
    
    Parameters
    ----------
    M : float
        Mean Anomaly (rad)
    e : float
        Eccentricity (unit-less)
    
    Returns
    -------
    nu : float
        True anomaly (rad)
    
    '''
    
    # First, let us solve for the eccentric anomaly.
    eccAnom = M2E(M,e)
    
    # With the eccentric anomaly, we can solve for position and velocity
    # in the perifocal (PQW) frame, using the polar equation for an ellipse.
    pos_X = np.cos(eccAnom) - e
    pos_Y = np.sqrt( 1 - e**2 ) * np.sin(eccAnom)
    
    # Finally, let us compute the true anomaly.
    nu = np.arctan2( pos_Y, pos_X ) 
    
    return nu

###############################################################################
###############################################################################

def V2E(nu,e):
    '''True anomaly to eccentric anomaly conversion (rad).
    
    Parameters
    ----------
    nu : float
        True anomaly (rad)
    e : float
        Eccentricity (unit-less)
    
    Returns
    -------
    E : float
        Eccentric anomaly (rad)
    
    '''
    
    E = 2 * np.arctan( np.sqrt( ( 1 - e ) / ( 1 + e ) ) * np.tan( nu / 2 ) )
    return E

###############################################################################
###############################################################################

def E2M(E,e):
    '''Eccentric anomaly to mean anomaly conversion (rad). Note that this uses
    the original Keplers equation M = E - e*sin(E).
    
    Parameters
    ----------
    E : float
        Eccentric anomaly (rad)
    e : float
        Eccentricity (unit-less)
    
    Returns
    -------
    M : float
        Mean Anomaly (rad)
    
    '''
    
    M = E - e * np.sin(E)
    return M

###############################################################################
###############################################################################

def V2M(nu,e):
    '''True anomaly to mean anomaly conversion (rad).
    
    Parameters
    ----------
    nu : float
        True anomaly (rad)
    e : float
        Eccentricity (unit-less)
    
    Returns
    -------
    M : float
        Mean Anomaly (rad)
    
    '''
    
    return E2M( V2E(nu,e), e )
