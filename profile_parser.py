# coding: utf-8

import re
import socket
from pprint import PrettyPrinter

def is_stanza(line):
    m = re.match('\[([\w\-\.]+)\]',line)
    if m:
        m.groups(1)
        return True
    else:
        return False
pp = PrettyPrinter()
f = open("/Users/tbender/.fwknoprc","r")
all = f.read()
f.close()

config_lines = [ x for x in all.splitlines() if not x.startswith('#') ]

#first find the lines that contain the stanza headers
stanza_hdrs = [ (i,config_lines[i]) for i in range(len(config_lines)) if is_stanza(config_lines[i]) ]

pp.pprint(stanza_hdrs)

#then search between those lines for the SPA_SERVER line

stanzas = []
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
        stanzas+=[{'name':stanza_name,'server':server_name, 'server-ip':server_ip}]

pp.pprint(stanzas)



