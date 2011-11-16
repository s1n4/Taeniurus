![Taeniurus](http://ubuntuone.com/3rPdv4GGW9r6ObIaiz2fVK)

**Developer: s1n4 (s1n4@live.com)**

**Ideas by: arda7an, sdk, hamid rostami**

**License: GPLv3**

***

&nbsp;&nbsp;&nbsp;&nbsp;Hello, This is a project with the name Taeniurus.

An irc bot that you can configure it or anything else you'd like to use (writing your own commands etc).

Also I should say the main goal of this project is only learning, learning python or how to wrting an irc bot.

All codes are written by s1n4 (Sina Samavati) and license under The GNU General Public License.

Tell me your suggestions and ideas about the Taeniurus with sending email to s1n4@live.com or join us on the freenode #xprous

Thanks!


_Taeniurus Copyright (C) 2011 s1n4_

***

### Project Taeniurus Information:
&nbsp;&nbsp;&nbsp;&nbsp;Taeniurus is an IRC bot written in the python programming language.

Taeniurus is also a snake ([Orthriophis taeniurus](http://en.wikipedia.org/wiki/Orthriophis_taeniurus)).

The name was chosen because I really like snakes!

The project is licensed under the GNU General Public License Version 3 (http://www.gnu.org/licenses/gpl-3.0.html).

**_The main idea on creating this Project is only Learning and nothing else_**.

> **As stated in the license, I DO NOT guarantee that this will work. Use at your own risk.
I DO NOT take any blames on harms to your computer etc.**


***

### Stuff you should do before everything:
Before running it you should change something in the taeniurus.cfg file, otherwise it will connect to the default server and join the default channel which are irc.freenode.net and #xprous

![taeniurus.cfg](http://ubuntuone.com/3ejammcytt9Y7iWbQTHhVD)

### Note:
After running it you should identify yourself for the bot with the `!oper` command: `!oper user password`, from the irc channel you've joined or via private message.

The default user and password are `admin`.
When you're identified, you can change the user and the password with the `!cguser` and the `!passwd` commands: `!cguser newuser`, `!passwd newpassword`

Taeniurus gives that who is using commands from irc and finds the code of command in the cmds.cfg file then, will run the code with 'exec' statement.

> It works with the ConfigParser module which is used to parsing configuration files like `.cfg, .ini`.

Please note that there is an access level per command/user, there are `oper` and `*`, if a command access's level is `oper` only an user who is identified for the bot as an oper can use the command, and `*` would be for all users.


***

### TODO
There are several commands and I'll explain them.

`!quote`, As it's recognizable, it works like `/quote` in irc clients which sends a raw data to the network without doing anything else.

`!addcmd`, It lets you to write your own commands which will be added into the `cmds.cfg` file.

`!delcmd`, You will be able to delete the command you want to.

`!addproc`, You can add your own process for when irc is running.

`!delproc`, You can delete the process which is stored in the `process.cfg` file.

`!cguser`, To change the username which is stored in the `taeniurus.cfg` file.

`!passwd`, To change the password which is stored in the `taeniurus.cfg` file, password will encrypt with the md5 hash algorithm.

`!show_cmds`, To see all commands.

`!show_procs`, To see all processes.

`!pid`, It will show you its pid.

`!killop`, To kill a bot operator who is identified for the bot (`!killop nickname`).

`!reload_confs`, To reload all configuration files.

`!bash`, To do a shell command from the irc, It will show you output of the command as well.

***
