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

from lib.irc import IRC
from multiprocessing import Process
import ConfigParser
import hashlib
import os
import sys
import time


class Error(Exception):
    #this class will store some exception errors and how them occurred
    def __init__(self, value, path):
        errors = file(path+'errors.log', 'a')
        errors.write(value)
        errors.close()

    def __str__(self):
        return "Oops!, something went wrong, errors are logged in the '%s'errors.log file" % self.path

def bash(command):
    return os.popen(command).read()


def daemon(pidfile):
    #This puts the process to background
    #and writes the pid in a file with the name 'taeniurus.pid' (as default)
    pid = os.fork()
    if pid != 0:
        botpid = file(pidfile, 'w')
        botpid.write(str(pid))
        print 'Taeniurus PID: \033[1m\033[92m%d\033[0m' % pid
        botpid.close()
        exit()


def detect_user():
    if os.getenv('USERNAME') == 'root':
        print 'DO NOT RUN IT AS ROOT!'
        exit(1)


def header(server, port):
    print r'''
___________                        .__
\__    ___/_____     ____    ____  |__| __ __ _______  __ __  ______
  |    |   \__  \  _/ __ \  /    \ |  ||  |  \\_  __ \|  |  \/  ___/
  |    |    / __ \_\  ___/ |   |  \|  ||  |  / |  | \/|  |  /\___ \
  |____|   (____  / \___  >|___|  /|__||____/  |__|   |____//____  >
                \/      \/      \/                               \/  IRC Bot

Developer:    s1n4 (contact@s1n4.com)
Ideas by:     arda7an, sdk, hamid rostami
License:      GPLv3
'''
    print '\rConnecting to %s:%d ' % (server, port),
    while True:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)


def save_conf(conf):
    with file(conf._file, 'w') as configfile:
        conf.write(configfile)


def main_conf():
    conf = ConfigParser.ConfigParser()
    conf._file = 'taeniurus.cfg'
    conf.read('taeniurus.cfg')
    info_items = {'nick': 'Taeniurus', 'uname': 'taeniurus', 'realname': 'http://github.com/s1n4/Taeniurus',
                  'server': 'irc.freenode.net', 'port': '8001', 'channel': '#xprous'}
    oper_items = {'user': 'admin', 'passwd': hashlib.md5('admin').hexdigest()}

    if conf.has_section('info'):
        for option in info_items:
            if not conf.has_option('info', option) or not conf.get('info', option):
                conf.set('info', option, info_items[option])
                save_conf(conf)

    else:
        conf.add_section('info')
        for option in info_items:
            conf.set('info', option, info_items[option])

        save_conf(conf)


    if conf.has_section('oper'):
        for option in oper_items:
            if not conf.has_option('oper', option) or not conf.get('oper', option):
                conf.set('oper', option, oper_items[option])
                save_conf(conf)

    else:
        conf.add_section('oper')
        for option in oper_items:
            conf.set('oper', option, oper_items[option])
            save_conf(conf)


def main():
    main_conf()
    opers = {}
    mainconf, tasks, cmds = (ConfigParser.RawConfigParser(), ConfigParser.RawConfigParser(), ConfigParser.RawConfigParser())
    mainconf._file, tasks._file, cmds._file = ('taeniurus.cfg', 'tasks.cfg', 'cmds.cfg')
    mainconf.read(mainconf._file)
    tasks.read(tasks._file)
    cmds.read(cmds._file)
    pidfile = mainconf.get('info', 'pid file')
    logspath = mainconf.get('info', 'logs path')
    irc = IRC()
    bgproc = Process(target=header, args=(irc.server, irc.port,))
    bgproc.start()
    client = irc.connect()

    if bgproc.is_alive():
        bgproc.terminate()

    print '\nConnected successfully!'
    print 'Connection: \033[1m\033[92m%s:%d\033[0m' % (irc.server, irc.port)
    print 'Channel: \033[1m\033[92m%s\033[0m' % irc.channel
    daemon(pidfile)

    acc_den = 'irc.notice("Access is denied!", nick)'
    done_msg = 'irc.notice("Done.", nick)'

    while True:
        try:
            data = client.recv(1024)
            arg, nick, user, joined, window = irc.parse(data)
            for section in tasks.sections():
                if tasks.get(section, 'code'):
                    try:
                        exec tasks.get(section, 'code')
                    except:
                        for op in opers:
                            irc.notice('A problem in tasks config file!', op)
                            irc.notice('File: %s' % tasks._file, op)
                            irc.notice('Section: %s' % section, op)

            if arg:
                args = arg.split()
                if len(args) < 1:
                    continue

                try:
                    if args[0] == '!oper' and user not in opers.values() and args[1] and args[2]:
                        if args[1] == mainconf.get('oper', 'user'):
                            if hashlib.md5(args[2]).hexdigest() == mainconf.get('oper', 'passwd'):
                                opers[nick] = user
                                irc.notice('You are appended into opers list.', nick)
                            else:
                                irc.notice('User or password incorrect!', nick)

                        else:
                            irc.notice('User or password incorrect!', nick)

                    if args[0] in cmds.sections():
                        if cmds.get(args[0], 'access') == 'oper' and user not in opers.values():
                            exec acc_den
                            continue

                        exec cmds.get(args[0], 'code')

                except:
                    irc.notice('It\'s either an argument error or I\'m unable to do it.', nick)

                if args[0] == '!quit' and user in opers.values():
                    qmsg = ' '.join(args[1:]) if len(args) >= 2 else 'Leaving'
                    irc.quit(qmsg)
                    import signal
                    pid = os.getpid()
                    os.kill(int(pid), signal.SIGKILL)

        except:
            raise Error(data, logspath)

detect_user()
main()

#EOF
