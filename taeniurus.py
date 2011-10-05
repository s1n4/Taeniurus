#!/usr/bin/env python

#This file is part of Taeniurus.

#Taeniurus is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#Taeniurus is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Taeniurus.  If not, see <http://www.gnu.org/licenses/>.

#Taeniurus  Copyright (C) 2011  s1n4

from modules.irc import IRC
from multiprocessing import Process
import ConfigParser, hashlib, os, socket, sys, time


def Daemon() :
	#This is for background process, this will put its process into background
	#and writes the bot pid in a file with the name of 'taeniurus.pid'
	pid = os.fork()
	if pid != 0 :
		botpid = file('taeniurus.pid', 'w')
		botpid.write(str(pid))
		print 'Taeniurus PID: \033[1m\033[92m%d\033[0m' % pid
		botpid.close()
		exit()


def Header(server, port) :
	try :
		readme = open('README')
		for line in xrange(11) :
			sys.stdout.write('\033[1m'+readme.readline()+'\033[0m')
			sys.stdout.flush()
			time.sleep(0.01)
	except :
		pass

	print '\rConnecting to %s:%d ' % (server, port),
	for c in xrange(30) :
		sys.stdout.write('.')
		sys.stdout.flush()
		time.sleep(1)


def SaveConf(conf) :
	with open(conf.file_name, 'w') as configfile :
		conf.write(configfile)


def MainConf() :
	conf = ConfigParser.ConfigParser()
	conf.file_name = 'taeniurus.cfg'
	conf.read('taeniurus.cfg')
	info_items = {'nick' : 'Taeniurus', 'uname' : 'taeniurus', 'realname' : 'http://github.com/s1n4/Taeniurus', 'server' : 'irc.freenode.net', 'port' : '8001', 'channel' : '#darkprocess'}
	oper_items = {'user' : 'admin', 'passwd' : hashlib.md5('admin').hexdigest()}

	if conf.has_section('info') :
		for option in info_items :
			if not conf.has_option('info', option) or not conf.get('info', option) :
				conf.set('info', option, info_items[option])
				SaveConf(conf)

	else :
		conf.add_section('info')
		for option in info_items :
			conf.set('info', option, info_items[option])
		SaveConf(conf)


	if conf.has_section('oper') :
		for option in oper_items :
			if not conf.has_option('oper', option) or not conf.get('oper', option) :
				conf.set('oper', option, oper_items[option])
				SaveConf(conf)

	else :
		conf.add_section('oper')
		for option in oper_items :
			conf.set('oper', option, oper_items[option])
			SaveConf(conf)


def main() :
	MainConf()
	opers = {}
	mainconf, process, cmds = (ConfigParser.RawConfigParser(), ConfigParser.RawConfigParser(), ConfigParser.RawConfigParser())
	mainconf.read('taeniurus.cfg')
	process.read('process.cfg')
	cmds.read('cmds.cfg')
	mainconf.file_name, process.file_name, cmds.file_name = ('taeniurus.cfg', 'process.cfg', 'cmds.cfg')
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	irc = IRC(client)
	bgproc = Process(target=Header, args=(irc.server, irc.port,))
	bgproc.start()
	client = irc.connect()

	if bgproc.is_alive() :
		bgproc.terminate()

	print '\nConnected successfully!'
	print 'Connection: \033[1m\033[92m%s:%d\033[0m' % (irc.server, irc.port)
	print 'Channel: \033[1m\033[92m%s\033[0m' % irc.channel
	Daemon()

	AcDen = 'irc.notice("Access Is Denied!", nick)'
	DoneMsg = 'irc.notice("It\'s Done.", nick)'

	while True :
		try :
			data = client.recv(1024)
			arg, nick, user, Wjoined, window = irc.process(data)
			for section in process.sections() :
				if process.get(section, 'code') :
					try :
						exec process.get(section, 'code')
					except :
						for op in opers :
							irc.notice('A problem in process config file is detected!', op)
							irc.notice('File: %s' % process.file_name, op)
							irc.notice('Section: %s' % section, op)

			if arg :
				args = arg.split()
				if len(args) < 1 :
					continue
				try :
					if args[0] == '!oper' and user not in opers.values() and args[1] and args[2] :
						if args[1] == mainconf.get('oper', 'user') :
							if hashlib.md5(args[2]).hexdigest() == mainconf.get('oper', 'passwd') :
								opers[nick] = user
								irc.notice('You are appended into opers list.', nick)
							else :
								irc.notice('User or password incorrect!', nick)

						else :
							irc.notice('User or password incorrect!', nick)

					if args[0] in cmds.sections() :
						if cmds.get(args[0], 'access') == 'oper' and user not in opers.values() :
							exec AcDen
							continue

						exec cmds.get(args[0], 'code')

				except :
					irc.notice('It\'s either an arguments error or I\'m unable to do it.', nick)

				if args[0] == '!quit' and user in opers.values() :
					irc.quit("Killed!")
					import signal
					pid = os.getpid()
					os.kill(int(pid), signal.SIGKILL)

		except :
			try :
				#this will report us some errors
				from modules.report import bugz
				proc = Process(target=bugz, args=(irc, data))
				proc.start()

			except :
				pass


main()
