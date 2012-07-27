# Taeniurus

An irc bot that you can configure it or anything else you'd like to use (writing your own commands etc).

Taeniurus is also a snake ([Orthriophis taeniurus](http://en.wikipedia.org/wiki/Orthriophis_taeniurus)).

The name is chosen because I really like snakes.


## Requirement

python 2.6 or 2.7


## Use

```bash
$ ./taeniurus.py
```

## License

It's licensed under the GPLv3.

See [LICENSE](Taeniurus/tree/master/LICENSE) file for more information.


## Guide

### Stuff you should do before anything

Before running it you should change something in the _taeniurus.cfg_ file, otherwise it will connect to the default server and join the default channel which are irc.freenode.net and #xprous


### Note

After running it you should identify yourself for the bot with the `!oper` command: `!oper user password`,
from the irc channel you've joined or via private message.

The default user and password are `admin`.

When you're identified, you can change the user and the password with the `!cguser` and the `!passwd` commands:
`!cguser newuser`, `!passwd newpassword`

Taeniurus checks commands from irc and executes their codes that are stored in _cmds.cfg_ file.

> It works with the ConfigParser module that is used to parsing configuration files like _.cfg, .ini_

Please note that there is an access level per command/user, they are `oper` and `*`, if a command access's level is `oper` only an user who is identified for the bot as an oper can use the command, and `*` is used for all users.



### Existing commands

There are several commands as the default with the following description.

`!quote`, As it's recognizable, it works like `/quote` in irc clients, It sends a raw data to the network without doing anything else.

`!addcmd`; It lets you to write your own command that will be added into the _cmds.cfg_ file.

`!delcmd`; It allows you to delete the command you want to.

`!addtask`; You can add a task for the bot irc.

`!deltask`; It allows you to delete a task that is stored in the _tasks.cfg_ file.

`!cguser`; To change the username that is stored in the _taeniurus.cfg_ file.

`!passwd`; To change the password that is stored in the _taeniurus.cfg_ file.

`!show_cmds`; It lists all existing commands.

`!show_tasks`; It lists all existing tasks.

`!pid`; It will show you its pid.

`!killop`; To kill a bot operator who is identified for the bot (`!killop nickname`).

`!reload_confs`; It allows you to reload all configuration files.

`!bash`; It performs a shell command from the irc, it will show you output of the command as well.

`!help`; It lists the contents of the _commands_ file.

`!opers`; It allows you to see nick of those who are identified for the bot as operator.



### How to add a command

There is a command to add your own command, but you must know some of variables that are existed.

```python
arg, nick, user, Wjoined, window = irc.parse(data)
```

`arg`, A string variable to storing logs and something else.

```ini
[log]
code = if arg : log = file(logspath+window+'.log', 'a'); log.write(time.strftime('%H:%M')+' <'+nick+'> '+arg+'\n'); log.close()
```

`args`, A list variable to recognize commands and their arguments, for instance:
`!bash echo "hello"`. args[0] would be the command `!bash`, args[1] would be `echo` and args[2] would be `"hello"` as well, in this instance.

> Also, an important thing for writing a command is the variable _args_.

`nick`, The nick of that who is talking on the channel or to the bot.

`user`, It contains: `nick@hostname` of that who is talking.

`Wjoined`, A boolean variable (True or False), It will be True for when a user has joined the channel.


#### Now you will be able to add a command.

`!addcmd [!cmd name] [access level (oper/anything else)] [python code]`

**e.g.** `!addcmd !voice oper irc.voice(args[1])`

**usage:** `!voice nickname`

It will set a vioce (+) mode for nickname on the channel.



### How to add a task

There is a command to add a task.

Take a loot at the followig instance to figure it out.

```ini
[tw]
code = if Wjoined and nick != irc.mynick : irc.notice('Hey %s, Welcome to %s!' % (nick, irc.channel), nick)
```

I want to edit the task _tw_ from the irc:

```
!deltask tw
!addtask tw if Wjoined and nick != irc.mynick : irc.notice('Hey %s, Welcome to %s!' % (nick, irc.channel), nick); irc.voice(nick)
```


#### I hope it's useful!
