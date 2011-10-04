#!/usr/bin/python

import socket

#A small bot for reporting some errors on the freenode #darkprocess

def bugz(irc, data) :
	freenode = ('irc.freenode.net', 'chat.freenode.net')
	channel = '#darkprocess'
	partmsg = 'Bug reporting, It has done'

	if irc.server in freenode :
		irc.join(channel=channel)
		irc.pm('!bugz '+data, channel)
		irc.part(channel, partmsg)

	else :
		from irc import IRC
		irc = IRC(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
		irc.server = freenode[0]
		irc.port = 8001
		irc.channel = channel
		irc.connect()
		irc.pm('!bugz '+data, channel)
		irc.part(channel, partmsg)
		irc.quit(partmsg)

