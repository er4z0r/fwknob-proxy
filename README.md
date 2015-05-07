# fwknob-proxy for convenient usage of portknocking on the client

This project is still in its very early stages (i.e. "works for me") .

fwknob-proxy is a SOCKS-proxy written in python that allows you to 'knockify'
applications on the client so you need not always manually send a knock-request before connecting. This can be very hand for applications such as e-mail clients, IRC-clients or even SSH. Basically anything that supports a SOCKS proxy. Even applications that do not directly support SOCKS can still be 'knockified' using a wrapper such as [proxychains-ng](https://github.com/rofl0r/proxychains-ng).

It is a stripped down bastard of Moxie Marlinspike's great [knockknock project](https://github.com/moxie0/knockknock). So 99% of the code was written by him. I simply took his code and ripped out only the proxy part.

## How to use it
* make sure you have the fwknop client installed and configured your ~/.fwknoprc
* Check KnockingEndpointConnection.py if the path to fwknop suits your environment

Here is a sample ~/.fwknoprc

```
[knockify.me]
ACCESS                      tcp/22
SPA_SERVER                  knockify.me
KEY_BASE64                  ...
HMAC_KEY_BASE64             ...
USE_HMAC                    Y
RESOLVE_IP_HTTPS            Y
```
And here is a sample entry from .ssh/config

```
Host knockify
    HostName    knockify.me
    User        whatever
    PreferredAuthentications publickey
    ProxyCommand /usr/bin/nc -X 5 -x 127.0.0.1:1337 %h %p
```

Now you can start the proxy with

```zsh
$python fwknop-proxy 1337
```

and connect to ssh as usual

```zsh
$ shh knockify
```

In the output of fwknop-proxy you should see something like this:

```
$ python fwknop-proxy.py 1337
Command: ['fwknop', '-A', 'tcp/22', '-n', 'knockify.me', '--wget-cmd', '/usr/local/bin/wget', '--verbose']
```

And you ssh session should be granted. Now be careful **you need to keep the proxy running in the background**. Once you kill the proxy, you kill you connection as ssh is forwarding all its traffic through your proxy.

## Why?
I recently abandoned knockknock in favour of fwknop, because the latter seems to take the idea of Single Packet Authorization to the next level.

It was especially the organizational factors that tipped the scales in favour of fwknob:

* It is integrated with many Linux distributions
* It is actively maintained
* The client exists for several different platforms (mobile included)

While all this was neat and nice, I really missed the convenience of knockknock-proxy which makes connecting to a service protected by SPA so transparent you almost forget that it is involved.



