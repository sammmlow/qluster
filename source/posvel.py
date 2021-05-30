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
##    Function to solve for the orbit position, velocity and true anomaly.   ##
##                                                                           ##
##    Written by Samuel Y. W. Low.                                           ##
##    First created 02-May-2021 00:53 AM (+8 GMT)                            ##
##    Last modified 20-May-2021 10:14 AM (+8 GMT)                            ##
##                                                                           ##
###############################################################################
###############################################################################

import numpy as np
from source import kepler
from source import dcmrotx
from source import dcmrotz

def posvel(a, e, i, w, R, M):
    
    '''
    Inputs: Keplerian elements and gravitational constant.
    - a   -> Semi-major axis (km)
    - e   -> Eccentricity (one)
    - i   -> Inclination (rad)
    - w   -> Argument of Perigee (rad)
    - R   -> Right Angle of Asc Node (rad)
    - M   -> Mean Anomaly (rad)

    Output: Inertial position vector, velocity vector, and true anomaly
    - pos -> inertial position (1x3 vector, km)
    - vel -> inertial velocity (1x3 vector, km/s)
    - nu  -> true anomaly (float, rad)
    '''
    
    # Ensure the conversion of the attractor's gravitational constant.
    mu = 398600.44 # G * Earth Mass (km**3/s**2)
    
    # The general flow of the program, is to first solve for the radial
    # position and velocity (in the inertial frame) via Kepler's equation.
    # Thereafter, we obtain the inertial coordinates in the Hill frame,
    # by performing a 3-1-3 Euler Angle rotation using an appropriate DCM.
    
    # First, let us solve for the eccentric anomaly.
    eccAnom = kepler.solve(M,e)
    
    # With the eccentric anomaly, we can solve for position and velocity
    # in the local orbital frame, using the polar equation for an ellipse.
    pos_X = a * ( np.cos(eccAnom) - e)
    pos_Y = a * np.sqrt( 1 - e**2 ) * np.sin(eccAnom)
    pos_norm = np.sqrt( pos_X**2 + pos_Y**2 )
    vel_const = np.sqrt( mu * a ) / pos_norm
    vel_X = vel_const * ( -1 * np.sin(eccAnom) )
    vel_Y = vel_const * ( np.sqrt( 1 - e**2 ) * np.cos(eccAnom) )
    
    # To perform the conversion from local orbit plane to an ECI frame, we
    # need perform the 313 Euler angle rotation in the following sequence:
    # Right Angle of Ascending Node -> Inclination -> Argument of Latitude.
    # Now, let us get us the DCM that converts to the hill-frame.
    DCM_HN = np.matmul( dcmrotz.dcmZ(w),
                        np.matmul( dcmrotx.dcmX(i), 
                                   dcmrotz.dcmZ(R) ) )
    
    # Notice that the hill frame computation does not include a rotation
    # of the true anomaly, and that's because the true anomaly has already
    # been accounted for when computing pos_X and pos_Y using information 
    # from the eccentric anomaly. Including true anomaly in the DCM 
    # rotation would double-count that anomaly rotation.
    
    # The current coordinates are in the local hill frame, and thus 
    # conversion from hill to inertial would be the transpose of HN.
    DCM_NH = np.transpose(DCM_HN)
    
    # For the matrix multiplication below, we will 
    
    # With the hill frame, we can now convert it to the ECI frame.
    pos = np.matmul(DCM_NH, np.array([ pos_X, pos_Y, 0.0 ]))
    vel = np.matmul(DCM_NH, np.array([ vel_X, vel_Y, 0.0 ]))
    
    # Finally, let us not forget to compute the true anomaly.
    nu = np.arctan2( pos_Y, pos_X ) 
    
    # Position vector 1x3 (km), velocity vetor 1x3 (km/s), true anomaly (rad)
    return pos, vel, nu
