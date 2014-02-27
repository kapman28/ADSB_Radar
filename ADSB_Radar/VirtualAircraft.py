# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 16:04:09 2014

@author: Kregg
"""

import numpy as np

class virtualAircraft :
    """ Virtual Aircraft Propogator"""
    speed = 0.0               # in knots
    altitude = 0.0            # in feet
    heading = 0.0             # in degrees
    currClimbRate = 0.0       # in feet per minute
    currTurnRate = 0.0        # in degrees per second
    defaultClimbRate = 500.0  # in feet per minute
    defaultTurnRate = 3.0     # in degrees per second
    turnSecondsLeft = 0     # # of seconds left to maintain turn
    climbSecondsLeft = 0    # # of seconds left to maintain climb
    defaultTurnTime = 10    # # of seconds to turn for each time we indicate a turn
    defaultClimbTime = 20   # # of seconds to climb for each time a turn is indicated
    latitude = 0.0            # our current latitude in degrees, N = +, S = -
    longitude = 0.0           # our current longitude in degrees, E = +, W = -
    address = 0             # unique address to be incremented each time an aircraft is created
    # aircraftAddress is a static class variable to give unique IDs to each instance
    aircraftAddress = 1000000
    
    def __init__(self, v0 = 100, alt0 = 3000, heading0 = 360, lat0 = 38.0, long0 = -118.25):
        self.speed = v0
        self.altitude = alt0
        self.heading = heading0
        self.latitude = lat0
        self.longitude = long0
        self.address = self.__class__.aircraftAddress
        self.__class__.aircraftAddress += 1
        
        return
        
    # start or continue a turn for defaultTurnTime more seconds
    def setTurn(self, turnToTheRight = True):
        self.turnSecondsLeft = self.defaultTurnTime
        self.currTurnRate = self.defaultTurnRate
        if ~turnToTheRight:
            self.currTurnRate = -self.currTurnRate
            
    # start or continue a climb/descent for defaultClimbTime more seconds
    def setClimb(self, isClimbing = True):
        self.climbSecondsLeft = self.defaultClimbTime
        self.currClimbRate = self.defaultClimbRate
        if ~isClimbing :
            self.currClimbRate = -self.currClimbRate
    
    # march the aircraft through time by this number of seconds    
    def propogateState(self, deltaT = 1.0):
        if self.turnSecondsLeft > 0.0 :
            self.heading = (self.heading + np.min([deltaT, self.turnSecondsLeft]) * self.currTurnRate) % 360.0
            self.turnSecondsLeft -= deltaT
        
        if self.climbSecondsLeft > 0.0 :
            self.altitude += self.currClimbRate / 60.0 * np.min([deltaT, self.climbSecondsLeft])
            self.climbSecondsLeft -= deltaT
        
        degreesPerKnotPerSecond = 1.688 / (60.0 * 6076.0)    # one knot if 1.688 feet per second, one minute latitude is 6076.0 feet
        self.latitude += np.cos(np.deg2rad(self.heading)) * degreesPerKnotPerSecond * self.speed * deltaT
        self.longitude += np.sin(np.deg2rad(self.heading)) * degreesPerKnotPerSecond * np.cos(self.latitude) * self.speed * deltaT
        
        return
        
class aircraftManager :
    """ Virtual Aircraft Manager"""        
    aircraft = []
    # begin left turns and descents for random values below these values
    leftTurnThresh = 0.01
    descentThresh = 0.01
    # begin right turns and climbs for random values above these values
    rightTurnThresh = 0.99
    climbThresh = 0.99
    
    def __init__(self):
        aircraft = []
        return
        
    def generateAircraft(self, n = 5, centerLat = 38.0, centerLong = -119.3, radiusNM = 2.0, 
                         minAlt = 1000.0, maxAlt = 5000.0, minSpeed = 40.0, maxSpeed = 250.0) :
        for indx in range(n) :
            latitude = centerLat + np.random.uniform(-radiusNM/60.0, radiusNM/60.0)
            longitudeRadius = -radiusNM/60.0/np.cos(latitude)
            longitude = centerLong + np.random.uniform(-longitudeRadius, longitudeRadius)
            newPlane = virtualAircraft( v0 = np.round(np.random.uniform(minSpeed, maxSpeed)),
                                       alt0 = 100.0 * np.round(np.random.uniform( minAlt/100.0, maxAlt/100.0)),
                                        heading0 = np.round(np.random.uniform(0.0,360.0)), lat0 = latitude, long0 = longitude)
            self.aircraft.append( newPlane )
        
        return
    
    # propogate all the aircraft forward in time for deltaT seconds, initiating random climbs & turns    
    def propogateAircraft(self, deltaT = 1.0):
        for aircraft in self.aircraft :
            turnRandNum = np.random.uniform()
            if turnRandNum > self.rightTurnThresh :
                aircraft.setTurn(True)
            elif turnRandNum < self.leftTurnThresh :
                aircraft.setTurn(False)
            
            climbRandNum = np.random.uniform()
            if climbRandNum > self.climbThresh :
                aircraft.setClimb(True)
            elif climbRandNum < self.descentThresh :
                aircraft.setClimb(False)
            
            aircraft.propogateState(deltaT)
        
        return
