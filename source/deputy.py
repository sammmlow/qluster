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
##    This file contains the function that resolves for the Keplerian        ##
##    elements of the deputy spacecraft. It takes in formation geometry      ##
##    parameters (radial, in-track, cross-track, or RIC), the argument of    ##
##    latitude crossing (rad), the argument of relative pericenter (rad),    ##
##    the six chief orbit Keplerian elements (in km and rad) as inputs.      ##
##    It outputs the six Keplerian orbit elements of the deputy spacecraft   ##
##    that satisfies the formation geometrical requirements.                 ##
##                                                                           ##
##    KEY REFERENCES:                                                        ##
##                                                                           ##
##   [1] Clohessy, W. H., Wiltshire, R. S. (1960). Terminal guidance         ##
##       system for satellite rendezvous. Journal of the Aerospace           ##
##       Sciences, 27(9), 653-658. doi:10.2514/8.8704                        ##
##                                                                           ##
##   [2] D'Amico, S., &; Montenbruck, O. (2006). Proximity operations of     ##
##       formation-flying spacecraft using an eccentricity/inclination       ##
##       vector separation. Journal of Guidance, Control, and Dynamics,      ##
##       29(3), 554-563. doi:10.2514/1.15114                                 ##
##                                                                           ##
##   [3] D'Amico, S. (2010) Autonomous Formation Flying in Low Earth         ##
##       Orbit. PhD Dissertation, TU Delft.                                  ##
##                                                                           ##
##    Written by Samuel Y. W. Low.                                           ##
##    First created 20-May-2021 18:00 PM (+8 GMT)                            ##
##    Last modified 20-May-2021 20:09 PM (+8 GMT)                            ##
##                                                                           ##
###############################################################################
###############################################################################

import numpy as np
from source import anomaly

def deputy(td, ts, aC, eC, iC, wC, RC, MC, fR, fI, fO, fC, fPhi, fTht):
    '''

    Parameters
    ----------
    td : int
        Propagation Duration (s)
    ts : int
        Propagation Timestep (s)
    aC : float
        Chief Orbit Semi-Major Axis (km)
    eC : float
        Chief Orbit Eccentricity (0 to 1)
    iC : float
        Chief Orbit Inclination (deg)
    wC : float
        Chief Orbit Arg. of Perigee (deg)
    RC : float
        Chief Orbit Right Ascension (deg)
    MC : float
        Chief Orbit Mean Anomaly (deg)
    fR : float
        Formation Radial Amplitude (km)
    fI : float
        Formation In-Track Amplitude (km)
    fO : float
        Formation In-Track Offset (km)
    fC : float
        Formation Cross-Track Amplitude (km)
    fPhi : float
        Argument of Relative Pericenter (rad)
    fTht : float
        Argument of Latitude Crossing (rad)
    
    Returns
    -------
    aD : float
        Deputy Orbit Semi-Major Axis (km)
    eD : float
        Deputy Orbit Eccentricity (0 to 1)
    iD : float
        Deputy Orbit Inclination (rad)
    wD : float
        Deputy Orbit Arg. of Perigee (rad)
    RD : float
        Deputy Orbit Right Ascension (rad)
    MD : float
        Deputy Orbit Mean Anomaly (rad)

    '''
    
    # Convert all angles from degrees to radians.
    iC   = np.deg2rad( iC   )
    wC   = np.deg2rad( wC   )
    RC   = np.deg2rad( RC   )
    MC   = np.deg2rad( MC   )
    fPhi = np.deg2rad( fPhi )
    fTht = np.deg2rad( fTht )
    
    # First, the Hill-Clohessy-Wiltshire equations are predicated on the key
    # assumption that the chief and deputy share the same semi-major axis.
    aD = aC
    
    # Second, from the radial or in-track separation, we can derive the deputy
    # satellite's eccentricity and argument of perigee.
    de      = fR / aC
    de_vect = np.array([ de * np.cos(fPhi), de * np.sin(fPhi) ])
    eC_vect = np.array([ eC * np.cos( wC ), eC * np.sin( wC ) ])
    eD_vect = eC_vect + de_vect
    eD      = np.linalg.norm( eD_vect )
    wD      = np.arctan2( eD_vect[1], eD_vect[0] )
    
    # Third, the relative inclination vector components allow us to derive the
    # deputy inclination and right ascension of the ascending node.
    di      = np.sin( fC / aC )
    di_vect = np.array([ di * np.cos(fTht), di * np.sin(fTht) ])
    iD      = iC + di_vect[0]
    RD      = RC + ( di_vect[1] / np.sin(iC) )
    
    # Fourth, we need to determine the argument of latitudes of the chief
    # (where argument of latitude = true anomaly + argument of perigee)
    nuC = anomaly.M2V( MC, eC )
    
    # Finally, we need to ascertain the mean anomaly of the deputy. For a
    # bounded and centered formation geometry, it is expected that the mean
    # argument of latitude of the chief must be equal to the deputy. However,
    # if the user has specified a non-zero offset in the variable fO, then
    # this offset must be applied to the deputy satellite formation center.
    offset = fO / aD
    nuD = nuC + wC - wD + ( ( RD - RC ) * np.cos(iC) ) + offset
    MD = anomaly.V2M( nuD, eD )
    
    # Finally, re-convert all angular output into degrees.
    iD = np.rad2deg( iD )
    wD = np.rad2deg( wD )
    RD = np.rad2deg( RD )
    MD = np.rad2deg( MD )
    
    return aD, eD, iD, wD, RD, MD
