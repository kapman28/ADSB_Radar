# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 19:21:59 2014

@author: Kregg
"""

import VirtualAircraft as va
import time
import socket
import numpy as np

# this value defines the odds that we see each traffic object
# Make it smaller to make transmissions more likely to get through
missedCommsProb = 0.1
ownShipReportStr = 'OwnShip: '
trafficReportStr = 'Traffic: '

# traffic should be a list of virtualAircraft
def produceTrafficString( traffic ):
    s = '' 
    
    if len(traffic) > 0:
        s = trafficReportStr
        for plane in traffic :
            if np.random.uniform() > missedCommsProb :            
                s += aircraftString( plane )
    
    return s
    
def produceOwnshipString( ownShip ):
    s = ''
    
    s = ownShipReportStr + aircraftString(ownShip)

    return s    
    
    
def aircraftString( plane ):
    s = ''
    s += 'BasicReport:'
    s += '\t' + 'Time: 123ms'
    s += '\t' + 'Payload: 0'
    s += '\t' + 'AddrType 0'
    s += '\t' + 'Addr: ' + str(plane.address)
    s += '\t' + 'Lat: ' + str(plane.latitude)
    s += '\t' + 'Long: ' + str(plane.longitude)
    s += '\t' + 'Alt: ' + str(plane.altitude)
    s += '\t' + '(Air)'
    s += '\t' + 'Vel(kts): ' + str(plane.speed)
    s += '\t' + 'Hdg: ' + str(plane.heading)
    s += '\n\r'
    
    return s


# grab a port and wait for connection
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
s.bind( ('', 3790) )
s.listen(1)

print "Listening for connections...\n\r"

# when we get it, accept/attach
(clientSocket, addr) = s.accept()

#print 'Connection from ' + str(clientSocket.getsockname()) + ' : ' + addr
print 'Connection \n\r'

clientSocket.setblocking(0)

tStep = 1.0
trafficManager = va.aircraftManager()
trafficManager.generateAircraft()
indx = 0

try:
    while (True):
        # Normally we'd parse Ground Station data here; Instead, simulate our own
        trafficManager.propogateAircraft(tStep)
        strOwn = ''
        strOther = ''
        strOwn = produceOwnshipString( trafficManager.aircraft[0])    
        strOther = produceTrafficString( trafficManager.aircraft[1:])
    #    try:
        if len(strOwn) > 0 :
            clientSocket.send(strOwn)
        if len(strOther) > 0 :
            clientSocket.send(strOther)
        print indx
        indx += 1
    #    except socket.error:
     #       print ''
            # print "no data"
        
        time.sleep(tStep)
except:
    pass

clientSocket.close()

s.close()

print 'Connections Closed'
