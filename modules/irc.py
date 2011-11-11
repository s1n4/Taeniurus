#!/usr/bin/python
#Filename: irc.py
#Author: s1n4
#Project: Taeniurus
#IRC Module

import ConfigParser, re, socket, time

class IRC :
	P = 'PRIVMSG'
	N = 'NOTICE'
	K = 'KICK'
	J = 'JOIN'
	I = 'INVITE'

	def __init__(self) :
		conf = ConfigParser.ConfigParser()
		conf.read('taeniurus.cfg')
		
		self.socket   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.mynick   = conf.get('info', 'nick')
		self.uname    = conf.get('info', 'uname')
		self.rname    = conf.get('info', 'realname')
		self.password = conf.get('info', 'password')
		self.server   = conf.get('info', 'server')
		self.port     = conf.getint('info', 'port')
		self.channel  = conf.get('info', 'channel')


	def chmode(self, mode) :
		#this works such as /mode but for channel not user
		socket.send('MODE %s %s\r\n' % (self.channel, mode))


	def join(self, socket=None, channel=None) :
		#this works such as /join in irc clients
		self.socket.send('JOIN %s\r\n' % channel)

	def kick(self, nick, reason=None) :
		#this works such as /kick in irc clients
		#kick(user, 'reason')
		if not reason : reason = nick
		self.socket.send('KICK %s %s :%s\r\n' % (self.channel, nick, reason))


	def knock(self, socket=None) :
		#this works such as /knock in irc clients
		self.socket.send('knock %s\r\n' % self.channel)


	def names(self) :
		self.socket.send('NAMES %s\r\n' % self.channel)
		data = self.socket.recv(1024)

		if data :
			ranks = ['+', '%', '@', '&', '~']
			data = data.replace(':', '').split()

			if len(data) >= 6 :
				for i in range(0, 5) :
					data.pop(0)

			nicks = data; del data
			nicklist = []

			for nick in nicks :
				if nick[0] in ranks :
					nicklist.append(nick[1:])

				else :
					nicklist.append(nick)

			return nicklist #this line returns a list of users which the bot is on.


	def nickname(self, data) :
		#this function retuens nick of who on the channel is speaking.
		if not data : 
			exit()
		data = data.replace(':', '').split()
		return data[0][:data[0].find('!')]


	def notice(self, msg, to=None) :
		#this works such as /notice in irc clients.
		if to == None :
			to = self.channel
		self.socket.send('NOTICE %s :%s\r\n' % (to, msg))


	def op(self, nick) :
		#this gives op mode to the user on the channel.
		self.socker.send('MODE %s +o %s\r\n' % (self.channel, nick))


	def part(self, channel, msg) :
		#this works such as /part in irc clients.
		self.socket.send('PART %s :%s\r\n' % (channel, msg))


	def pong(self, data) :
		#this is a game between the bot and network for staying up on irc network.
		self.socket.send('PONG %s\r\n' % data)


	def pm(self, msg, to=None) :
		#this works such as /msg in irc clients.
		if to == None :
			to = self.channel
		self.socket.send('PRIVMSG %s :%s\r\n' % (to, msg))


	def process(self, data) :
		#this is for processing datas on the main code's bot.
		if not data :
			exit()

		P = self.P
		N = self.N
		K = self.K
		J = self.J
		I = self.I

		From    = None
		arg     = None
		user    = None
		nick    = self.nickname(data)
		Wjoined = None
		window  = None
		args    = data.split()

		if args[0] == 'PING' :
			self.pong(args[1])

		elif args[1] == P or args[1] == J :
			if args[1] == J : 
				Wjoined = True
				self.channel = args[2] if args[2][0] == '#' else args[2][1:]

			user = args[0]
			vhost = user[user.find('@'):]
			del user; user = nick + vhost

			if args[1] == P :
				arg = re.search('(?<=PRIVMSG ).*', data).group()
				if arg[0] == '#' :
					self.channel = arg[:arg.find(' ')]
					window = arg[:arg.find(' ')]
				else :
					window = 'taeniurus'

				arg = arg[arg.find(' :')+2:]

		elif args[1] == N :
			try :
				RNotice = re.search('(?<=NOTICE ' + self.mynick + ' :).*', data).group()
			except :
				pass
			
		elif args[1] == K and args[3] == self.mynick :
			self.join(self.socket, args[2]) #args[2] is name of the channel bot is on, (in this line)

		elif args[1] == I and args[2] == self.mynick :
			self.join(self.socket, args[3])

		del data
		return arg, nick, user, Wjoined, window
		#this returns arg (it's everything that a user send on the channel), nick (nick of a user which is speaking on the channel)
		#user (nick@hostname of a user which is speaking on the channel), Wjoined (Who Joined, if this variable be True, this means 
		#a user has joined on the channel), window (name of channel or its bot a user is talking to)


	def quit(self, qmsg=None) :
		#this workds such as /quit in irc clients
		if not qmsg :
			qmsg = 'Leaving'
		self.socket.send('QUIT :%s\r\n' % qmsg)


	def umode(self, channel, mode, nick) :
		#this sets a mode for a nick on the channel
		#such as /mode but for user not channel
		#umode('#darkprocess', '+v', nick) for example
		self.socket.send('MODE %s %s %s\r\n' % (channel, mode, nick))


	def voice(self, nick) :
		#this gives voice mode such as /voice in irc clients
		self.socket.send('MODE %s +v %s\r\n' % (self.channel, nick))


	def whois(self, nick) :
		#this returns a list variable of nick you've whoised
		self.socket.send('WHOIS %s\r\n' % nick)
		data = self.socket.recv(1024)
		whoislst = []

		if len(data.split()) >= 4 :
			datax = ' '.join(data.split()[4:])
			datay = datax[1:] if datax[0] == ':' else datax
			whoislst = [datay]

		while 'end of /whois list' not in data.lower() :
			data = self.socket.recv(1024)

			for i in data.split('\n') :
				if len(i.split()) >= 4 :
					datax = ' '.join(i.split()[4:])
					datay = datax[1:] if datax[0] == ':' else datax
					whoislst.append(datay)

		if whoislst : return whoislst


	def connect(self, socket=None, server=None, channel=None) :
		#this is for connecting the bot to the server you putted the address into main config file
		#and join channel you want
		self.socket.connect((self.server, self.port))
		self.socket.send('NICK %s\r\n' % self.mynick)
		self.socket.send('USER %s %s %s :%s\r\n' % (self.uname, self.uname, self.server, self.rname))

		while True :
			data = self.socket.recv(1024)
			if data and data.split()[0] == 'PING' :
				self.socket.send('PONG %s\r\n' % data.split()[1])

			if 'Nickname is already in use' in data :
				#when nick of your bot is already in use, this changes nick of the bot to the current nick + -num
				for c in xrange(1, 1000) :
					newnick = self.mynick + '-' + str(c)
					self.socket.send('NICK %s\r\n' % newnick)
					data = self.socket.recv(1024)
					if 'Nickname is already in use' not in data :
						self.mynick = newnick
						break

			if 'End of' in data :
				#It will be identified for NickServ if you putted the nickserv password into config file
				if self.password :
					time.sleep(1)
					self.pm('IDENTIFY %s' % self.password, 'NickServ')
					self.socket.recv(1024)
					time.sleep(1)

				self.join(self.socket, self.channel)
				break

		return self.socket

