
from EndpointConnection import EndpointConnection

import subprocess
import time

from struct import *

class KnockingEndpointConnection(EndpointConnection):

    def __init__(self, shuttle, profile, host, port):
        self.host    = host
        self.port    = port
        self.profile = profile

        self.sendKnock(host, port)
        EndpointConnection.__init__(self, shuttle, host, port)

    def reconnect(self):
        self.sendKnock(self.host, self.port)
        EndpointConnection.reconnect(self)

    def sendKnock(self, host, port):

        command = "fwknop -A tcp/%d -n %s --wget-cmd /usr/local/bin/wget --verbose" % (port,self.profile.name)
        command = command.split()
        print "Command: %s" % command
        subprocess.call(command, shell=False, stdout=open("fwknob-proxy.log","w+"), stderr=subprocess.STDOUT)
        time.sleep(0.25)
