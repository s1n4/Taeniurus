![Taeniurus](http://ubuntuone.com/3rPdv4GGW9r6ObIaiz2fVK)

**Developer: s1n4 (s1n4@live.com)**

**Ideas by: arda7an, sdk, hamid rostami**

**License: GPLv3**

***

&nbsp;&nbsp;&nbsp;&nbsp;Hello, This is a project with the name of **Taeniurus**.

An irc bot that you can configure it or anything else you'd like to use (writing your own commands etc).

Also I should say the main goal of this project is only learning, learning python or how to wrting an irc bot.

All codes are written by s1n4 (Sina Samavati) and license under The GNU General Public License.

Tell me your suggestions and ideas about the Taeniurus with sending email to s1n4@live.com or join us on the freenode #xprous

Thanks!


_Taeniurus Copyright (C) 2011 s1n4_

***

* [Project Taeniurus Information](#Project Taeniurus Information)
* [Stuff you should do before everything](#Stuff you should do before everything)
* [TODO](#TODO)
* [How to write a command](#How to write a command)
* [How to write a process for the bot](#How to write a process for the bot)

***

### <a name="Project Taeniurus Information">Project Taeniurus Information</a>
&nbsp;&nbsp;&nbsp;&nbsp;Taeniurus is an IRC bot written in the python programming language.

Taeniurus is also a snake ([Orthriophis taeniurus](http://en.wikipedia.org/wiki/Orthriophis_taeniurus)).

The name was chosen because I really like snakes!

**_The main idea on creating this Project is only Learning and nothing else_**.

> **Use at your own risk, I DO NOT take any blames on harms to your computer etc.**


***

### <a name="Stuff you should do before everything">Stuff you should do before everything</a>
&nbsp;&nbsp;&nbsp;&nbsp;Before running it you should change something in the _taeniurus.cfg_ file, otherwise it will connect to the default server and join the default channel which are irc.freenode.net and #xprous

![taeniurus.cfg](http://ubuntuone.com/3ejammcytt9Y7iWbQTHhVD)

### Note:
&nbsp;&nbsp;&nbsp;&nbsp;After running it you should identify yourself for the bot with the `!oper` command: `!oper user password`, from the irc channel you've joined or via private message.

The default user and password are `admin`.
When you're identified, you can change the user and the password with the `!cguser` and the `!passwd` commands: `!cguser newuser`, `!passwd newpassword`

Taeniurus gives that who is using commands from irc and finds the code of command in the _cmds.cfg_ file then, will run the code with _exec_ statement.

> It works with the ConfigParser module which is used to parsing configuration files like _.cfg, .ini_

Please note that there is an access level per command/user, which are `oper` and `*`, if a command access's level is `oper` only an user who is identified for the bot as an oper can use the command, and `*` would be for all users.


***

### <a name="TODO">TODO</a>
&nbsp;&nbsp;&nbsp;&nbsp;There are several commands as the default with the following description.

`!quote`, As it's recognizable, it works like `/quote` in irc clients, It sends a raw data to the network without doing anything else.

`!addcmd`; It lets you to write your own command which will be added into the _cmds.cfg_ file.

`!delcmd`; You will be able to delete the command you want to.

`!addproc`; You can add your own process for when irc is running.

`!delproc`; You can delete the process which is stored in the _process.cfg_ file.

`!cguser`; To change the username which is stored in the _taeniurus.cfg_ file.

`!passwd`; To change the password which is stored in the _taeniurus.cfg_ file, password will be encrypted with the md5 hash algorithm.

`!show_cmds`; To see all commands.

`!show_procs`; To see all processes.

`!pid`; It will show you its pid.

`!killop`; To kill a bot operator who is identified for the bot (`!killop nickname`).

`!reload_confs`; To reload all configuration files.

`!bash`; To do a shell command from the irc, It will show you output of the command as well.

`!help`; To see the contents of the TODO file.

`!opers`; To see nick of those who are identified for the bot as an operator.

***

### <a name="How to write a command">How to write a command</a>
&nbsp;&nbsp;&nbsp;&nbsp;As you've seen the [TODO](#TODO) section, there is a command to add your own command, but you should know some of variables which exist.

```python
arg, nick, user, Wjoined, window = irc.process(data)
```

`arg`, A string variable to storing logs and something else.

```ini
[log]
code = if arg : log = file(logspath+window+'.log', 'a'); log.write(time.strftime('%H:%M')+' <'+nick+'> '+arg+'\n'); log.close()
```

`args`, A list variable to recognize commands and their arguments, for instance: `!bash echo "hello"`. args[0] would be the command `!bash`, args[1] would be `echo` and args[2] would be `"hello"` as well, in this instance.

> Also, an important thing to write a command is the variable args.

`nick`, The nick of that who is talking on the channel or to the bot.

`user`, It contains: `nick@hostname` of that who is talking.

`Wjoined`, A boolean variable (True or False), It will be True for when a user has joined the channel.

&nbsp;

&nbsp;&nbsp;&nbsp;&nbsp;Now you will be able to add a command.

**To do:** `!addcmd [!cmd name] [access level (oper/anything else)] [python code]`

**e.g.** `!addcmd !voice oper irc.voice(args[1])`

**usage:** `!voice nickname`

It will give nickname a mode on the channel which is voice (+).


> Also, you can add anything else as a command.

***

### <a name="How to write a process for the bot">How to write a process for the bot</a>

&nbsp;&nbsp;&nbsp;&nbsp;As I've already explain in the [TODO](#TODO) section, there is a command to add your own process.

To understanding it, I recommend getting a look at the following example.

```ini
[tw]
code = if Wjoined and nick != irc.mynick : irc.notice('Hey %s, Welcome to %s!' % (nick, irc.channel), nick)```

Now I will edit the process _tw_ from the irc:

    !delproc tw
    !addproc tw if Wjoined and nick != irc.mynick : irc.notice('Hey %s, Welcome to %s!' % (nick, irc.channel), nick); irc.voice(nick)

&nbsp;

_**I hope it's useful!**_