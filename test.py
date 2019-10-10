#!/usr/bin/env python2

import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('PiCQDisplay1', 4210)

rx1 = open('/mnt/RAMDisk/rx1.txt','r')
lh1 = open('/mnt/RAMDisk/lastHeard1.txt','r')

rx1details = rx1.read().rstrip()
rx1details = rx1details+';'

lh1details = lh1.read().rstrip()
lh1details = lh1details+';'

gesamt = rx1details+lh1details;

try:
    # Send data
    #print('sending {!r}'.format(gesamt))
    sent = sock.sendto(gesamt, server_address)

finally:
    #print('closing socket')
    rx1.close()
    lh1.close()
    sock.close()
