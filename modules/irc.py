#!/usr/bin/env python

#Project: Taeniurus https://github.com/s1n4/Taeniurus
#IRC module

import ConfigParser
import re
import socket
import time

class IRC:
    table = {
        'P': 'PRIVMSG',
        'N': 'NOTICE',
        'K': 'KICK',
        'J': 'JOIN',
        'I': 'INVITE'}

    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read('taeniurus.cfg')

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mynick = conf.get('info', 'nick')
        self.uname = conf.get('info', 'uname')
        self.rname = conf.get('info', 'realname')
        self.password = conf.get('info', 'password')
        self.server = conf.get('info', 'server')
        self.port = conf.getint('info', 'port')
        self.channel = conf.get('info', 'channel')


    def chmode(self, mode):
        #this works like /mode for a channel.
        socket.send('MODE %s %s\r\n' % (self.channel, mode))


    def join(self, socket=None, channel=None):
        #this works like /join in irc clients
        self.socket.send('JOIN %s\r\n' % channel)

    def kick(self, nick, reason=None):
        #this works like /kick in irc clients
        #e.g. kick(user, 'reason')
        if not reason: reason = nick
        self.socket.send('KICK %s %s :%s\r\n' % (self.channel, nick, reason))


    def knock(self, socket=None):
        #this works like /knock in irc clients
        self.socket.send('knock %s\r\n' % self.channel)


    def names(self):
        self.socket.send('NAMES %s\r\n' % self.channel)
        data = self.socket.recv(1024)

        if data:
            ranks = ['+', '%', '@', '&', '~']
            data = data.replace(':', '').split()

            if len(data) >= 6:
                for i in range(0, 5):
                    data.pop(0)

            nicks = data; del data
            nicklist = []

            for nick in nicks:
                if nick[0] in ranks:
                    nicklist.append(nick[1:])

                else:
                    nicklist.append(nick)

            return nicklist #this line returns a list of users who are on a channel.


    def nickname(self, data):
        #this function retuens nick of that who is talking on the channel/to the bot.
        if not data:
            exit()
        data = data.replace(':', '').split()
        return data[0][:data[0].find('!')]


    def notice(self, msg, to=None):
        #this works like /notice in irc clients.
        if to == None:
            to = self.channel
        self.socket.send('NOTICE %s :%s\r\n' % (to, msg))


    def op(self, nick):
        #this gives op mode to the user on the channel.
        self.socker.send('MODE %s +o %s\r\n' % (self.channel, nick))


    def part(self, channel, msg):
        #this works like /part in irc clients.
        self.socket.send('PART %s :%s\r\n' % (channel, msg))


    def pong(self, data):
        #this is a game between the bot and the irc network to staying up.
        self.socket.send('PONG %s\r\n' % data)


    def pm(self, msg, to=None):
        #this works like /msg in irc clients.
        if to == None:
            to = self.channel
        self.socket.send('PRIVMSG %s :%s\r\n' % (to, msg))


    def parse(self, data):
        #this parses datas.
        if not data:
            exit()

        From = None
        arg = None
        user = None
        nick = self.nickname(data)
        Wjoined = None
        window = None
        args = data.split()

        if args[0] == 'PING':
            self.pong(args[1])

        elif args[1] == self.table['P'] or args[1] == self.table['J']:
            if args[1] == self.table['J']:
                Wjoined = True
                self.channel = args[2] if args[2][0] == '#' else args[2][1:]

            user = args[0]
            vhost = user[user.find('@'):]
            del user; user = nick + vhost

            if args[1] == self.table['P']:
                arg = re.search('(?<=PRIVMSG ).*', data).group()
                if arg[0] == '#':
                    self.channel = arg[:arg.find(' ')]
                    window = arg[:arg.find(' ')]
                else:
                    window = self.nickname(data)

                arg = arg[arg.find(' :')+2:-1]

        elif args[1] == self.table['N']:
            try:
                RNotice = re.search('(?<=NOTICE ' + self.mynick + ' :).*', data).group()
            except:
                pass

        elif args[1] == self.table['K'] and args[3] == self.mynick:
            self.join(self.socket, args[2]) #args[2] would be the name of the channel (in this line)

        elif args[1] == self.table['I'] and args[2] == self.mynick:
            self.join(self.socket, args[3])

        del data
        return arg, nick, user, Wjoined, window
        #this returns arg (it's everything that a user sends on the channel), nick (nick of a user which is speaking on the channel)
        #user (nick@hostname of a user who is speaking on the channel), Wjoined (Who Joined, if this variable is being True, this means
        #a user has joined on the channel), window (name of channel or nick of a user)


    def quit(self, qmsg=None):
        #this works like /quit in irc clients
        if not qmsg:
            qmsg = 'Leaving'
        self.socket.send('QUIT :%s\r\n' % qmsg)


    def umode(self, mode, nick):
        #this sets a mode for a nick on the channel
        #like /mode but for a user not channel
        #e.g. umode('+v', nick)
        self.socket.send('MODE %s %s %s\r\n' % (self.channel, mode, nick))


    def voice(self, nick):
        #this gives voice mode (like /voice in irc clients)
        self.socket.send('MODE %s +v %s\r\n' % (self.channel, nick))


    def whois(self, nick):
        #this returns a list variable of nicks.
        self.socket.send('WHOIS %s\r\n' % nick)
        data = self.socket.recv(1024)
        whoislst = []

        if len(data.split()) >= 4:
            datax = ' '.join(data.split()[4:])
            datay = datax[1:] if datax[0] == ':' else datax
            whoislst = [datay]

        while 'end of /whois list' not in data.lower():
            data = self.socket.recv(1024)

            for i in data.split('\n'):
                if len(i.split()) >= 4:
                    datax = ' '.join(i.split()[4:])
                    datay = datax[1:] if datax[0] == ':' else datax
                    whoislst.append(datay)

        if whoislst: return whoislst


    def connect(self, socket=None, server=None, channel=None):
        #this connects the bot to the server that you putted its address into the main config file.
        #and joins the channel which is placed in the main config file.
        self.socket.connect((self.server, self.port))
        self.socket.send('NICK %s\r\n' % self.mynick)
        self.socket.send('USER %s %s %s :%s\r\n' % (self.uname, self.uname, self.server, self.rname))

        while True:
            data = self.socket.recv(1024)
            if data and data.split()[0] == 'PING':
                self.socket.send('PONG %s\r\n' % data.split()[1])

            if 'Nickname is already in use' in data:
                #this changes nick of the bot to the current nick + -num, for when the nick of the bot is already in use.
                for c in xrange(1, 1000):
                    newnick = self.mynick + '-' + str(c)
                    self.socket.send('NICK %s\r\n' % newnick)
                    data = self.socket.recv(1024)
                    if 'Nickname is already in use' not in data:
                        self.mynick = newnick
                        break

            if 'End of' in data:
                #It will be identified for NickServ if you've putted the nickserv password into the main config file.
                if self.password:
                    time.sleep(1)
                    self.pm('IDENTIFY %s' % self.password, 'NickServ')
                    self.socket.recv(1024)
                    time.sleep(1)

                self.join(self.socket, self.channel)
                break

        return self.socket
