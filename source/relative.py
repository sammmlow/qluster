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
##    This file contains the relative orbit propagation function. It takes   ##
##    the 06x chief and deputy orbit Keplerian elements (in km and radians)  ##
##    as input, and outputs the Hill-frame position and velocity vectors as  ##
##    two sets of Nx3 NumPy matrices, where N = total number of samples.     ##
##                                                                           ##
##    Written by Samuel Y. W. Low.                                           ##
##    First created 16-May-2020 15:56 AM (+8 GMT)                            ##
##    Last modified 20-May-2020 18:00 PM (+8 GMT)                            ##
##                                                                           ##
###############################################################################
###############################################################################

import numpy as np
from source import posvel

def propagate(td, ts, aC, eC, iC, wC, RC, MC, aD, eD, iD, wD, RD, MD):
    
    '''
    Core method for relative trajectory generation.

    Input Arguments:
    ----------------
    - td = Propagation Duration (s)
    - ts = Propagation Timestep (s)
    - aC = Chief Orbit Semi-Major Axis (km)
    - eC = Chief Orbit Eccentricity (0 to 1)
    - iC = Chief Orbit Inclination (deg)
    - wC = Chief Orbit Arg. of Perigee (deg)
    - RC = Chief Orbit Right Ascension (deg)
    - MC = Chief Orbit Mean Anomaly (deg)
    - aD = Deputy Orbit Semi-Major Axis (km)
    - eD = Deputy Orbit Eccentricity (0 to 1)
    - iD = Deputy Orbit Inclination (deg)
    - wD = Deputy Orbit Arg. of Perigee (deg)
    - RD = Deputy Orbit Right Ascension (deg)
    - MD = Deputy Orbit Mean Anomaly (deg)
    
    Returns 06x NumPy arrays
    ------------------------
    - X-Coordinate Hill-Frame positions
    - Y-Coordinate Hill-Frame positions
    - Z-Coordinate Hill-Frame positions
    - X-Coordinate Hill-Frame velocities
    - Y-Coordinate Hill-Frame velocities
    - Z-Coordinate Hill-Frame velocities
    '''
    #########################################################################
    #########################################################################
    ###                                                                   ###
    ###    First step is to turn all angular arguments from to radians    ###
    ###                                                                   ###
    #########################################################################
    #########################################################################
    
    iC, iD = np.deg2rad(iC), np.deg2rad(iD)
    wC, wD = np.deg2rad(wC), np.deg2rad(wD)
    RC, RD = np.deg2rad(RC), np.deg2rad(RD)
    MC, MD = np.deg2rad(MC), np.deg2rad(MD)
    
    #########################################################################
    #########################################################################
    ###                                                                   ###
    ###   Initialisation of relative state transition matrix parameters   ###
    ###                                                                   ###
    #########################################################################
    #########################################################################
    
    # Compute relative eccentricity and inclination vector components.
    ix =   iD - iC
    iy = ( np.sin(iC) * (RD - RC) )
    ex = ( eD * np.cos(wD) ) - ( eC * np.cos(wC) )
    ey = ( eD * np.sin(wD) ) - ( eC * np.sin(wC) )
    da = ( aD - aC ) / aC
    dR = ( RD - RC ) * np.cos(iC)
    
    # With the above, we can already define the state transition matrix
    # from classical orbit elements to VVLH frame relative state vectors.
    M = [[      da,     0.0, -1*ex, -1*ey    ],
         [      dR, -1.5*da,   0.0,   0.0    ],
         [     0.0,     0.0, -1*iy,    ix    ],
         [     0.0,     0.0, -1*ey,    ex    ],
         [ -1.5*da,     0.0,   0.0,   0.0    ],
         [     0.0,     0.0,    ix,    iy    ]]
    
    #########################################################################
    #########################################################################
    ###                                                                   ###
    ### Initialisation of all other required orbit parameters before loop ###
    ###                                                                   ###
    #########################################################################
    #########################################################################
    
    # Gravitational constant = G * Earth Mass (km**3/s**2)
    mu = 398600.44 
    
    # Get the mean motion of the chief.
    nC = np.sqrt( mu / ( aC**3 ) )
    
    # Get the mean motion of the deputy.
    nD = np.sqrt( mu / ( aD**3 ) )
    
    # Initialise relative position and velocity component arrays.
    rpx, rpy, rpz = [], [], []
    rvx, rvy, rvz = [], [], []
    
    # Initialise pi in terms of astropy units
    pi = np.pi
    
    # For each sample...
    for t in range( 0, td, ts ):
        
        # Update the mean anomaly of the chief (loop over pi).
        MC = ( ( MC + pi + ( nC * ts ) ) % ( 2 * pi ) ) - pi
        
        # Update the mean anomaly of the deputy (loop over pi).
        MD = ( ( MD + pi + ( nD * ts ) ) % ( 2 * pi ) ) - pi
        
        # Compute the chief position, velocity and true anomaly.
        pC, vC, nuC = posvel.posvel( aC, eC, iC, wC, RC, MC )
        
        # Compute the deputy position, velocity and true anomaly.
        pD, vD, nuD = posvel.posvel( aD, eD, iD, wD, RD, MD )
        
        # Get the argument of latitude of the chief.
        uC = nuC + wC
        uC = ( uC + pi ) % ( 2 * pi ) - pi # Loop over pi
        
        # Get the argument of latitude of the deputy.
        uD = nuD + wD
        uD = ( uD + pi ) % ( 2 * pi ) - pi # Loop over pi
        
        # Get the relative argument of latitude.
        du = uD - uC
        du = ( du + pi ) % ( 2 * pi ) - pi # Loop over pi
        
        # Save the chief initial argument of latitude.
        if t == 0:
            uC0 = uC
        
        # Compute the deputy elapsed argument of latitude.
        uD_elapsed = uD - uC0
        uD_elapsed = ( uD_elapsed + pi ) % ( 2 * pi ) - pi
        
        # Compute the velocity magnitude
        vCMag = np.sqrt( vC[0]**2 + vC[1]**2 + vC[2]**2 )
        
        # Initialize the time-dependent input vector
        uVect = np.array([ 1.0, uD_elapsed, np.cos(uC), np.sin(uC) ])
        
        # Update Row 1 Column 0 of the state transition matrix.
        M[1][0] = du + dR
        
        # We may now compute the normalized relative state vectors
        relPos = np.matmul( M[:3], uVect )
        relVel = np.matmul( M[3:], uVect )
        
        # Un-normalize the relative position vectors
        rpx.append( (relPos[0] * aC) )
        rpy.append( (relPos[1] * aC) )
        rpz.append( (relPos[2] * aC) )
        
        # Un-normalize the relative velocity vectors
        rvx.append( (relVel[0] * vCMag) )
        rvy.append( (relVel[1] * vCMag) )
        rvz.append( (relVel[2] * vCMag) )
    
    # Save the entire relativeEphem matrix.
    rpx = np.array( rpx ) * ( 1 )
    rpy = np.array( rpy ) * ( 1 )
    rpz = np.array( rpz ) * (-1 )
    rvx = np.array( rvx ) * ( 1 )
    rvy = np.array( rvy ) * ( 1 )
    rvz = np.array( rvz ) * (-1 )
    
    return rpx, rpy, rpz, rvx, rvy, rvz
