# coding: utf-8

import re
import socket
from pprint import PrettyPrinter


class Profiles(object):

    def __init__(self):
        self.profiles_by_ip = {}
        self.profiles_by_host = {}

    def addByIP(self,profile):
        self.profiles_by_ip[profile.ip]=profile

    def addByHost(self,profile):
        self.profiles_by_host[profile.host]=profile

    def add(self,profile):
        self.addByIP(profile)
        self.addByHost(profile)


    def byIP(self,ip):
        return self.profiles_by_ip[ip]

    def byHost(self,host):
        return self.profiles_by_host[host]

    def __str__(self):
        return self.profiles_by_host.values()

class Profile(object):
    def __init__(self,name,host,ip):
        self.name = name
        self.host = host
        self.ip = ip

    def __str__(self):
        return "[%s]\n\tserver=%s\n\tip=%s\n" % (self.name,self.host,self.ip)


def is_stanza(line):
    m = re.match('\[([\w\-\.]+)\]',line)
    if m:
        m.groups(1)
        return True
    else:
        return False

def fromFile(file):
    f = open(file,"r")
    all = f.read()
    f.close()

    config_lines = [ x for x in all.splitlines() if not x.startswith('#') ]
    #first find the lines that contain the stanza headers
    stanza_hdrs = [ (i,config_lines[i]) for i in range(len(config_lines)) if is_stanza(config_lines[i]) ]
    stanzas = []
    p = Profiles()
    #then search between those lines for the SPA_SERVER line
    for i in range(len(stanza_hdrs)):
        start=stanza_hdrs[i][0]+1
        try:
            end=stanza_hdrs[i+1][0]
        except IndexError:
            end=len(config_lines)-1
        server= [ re.sub("\s+",' ',x) for x in config_lines[start:end] if 'SPA_SERVER' in x ]
        if server:
            stanza_name = stanza_hdrs[i][1].strip('[]')
            server_name = server[0].split(' ')[1]
            server_ip = socket.gethostbyname(server_name)
            p.add(Profile(stanza_name,server_name,server_ip))
            stanzas+=[{'name':stanza_name,'server':server_name, 'server-ip':server_ip}]
    return p


if __name__ == '__main__':
    pp = PrettyPrinter()
    profiles = fromFile("/Users/tbender/.fwknoprc")

    pp.pprint(profiles)




