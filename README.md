![Taeniurus](http://ubuntuone.com/3rPdv4GGW9r6ObIaiz2fVK)

**Developer: s1n4 (s1n4@live.com)**

**Ideas by: arda7an, sdk, hamid rostami**

**License: GPLv3**

***

&nbsp; &nbsp; &nbsp;Hello, This is a project with the name Taeniurus.

An irc bot that you can configure it or anything else you'd like to use (writing your own commands etc).

Also I should say the main goal of this project is only learning, learning python or how to wrting an irc bot.

All codes are written by s1n4 (Sina Samavati) and license under The GNU General Public License.

Tell me your suggestions and ideas about the Taeniurus with sending email to s1n4@live.com or join us on the freenode #xprous

Thanks!


_Taeniurus Copyright (C) 2011 s1n4_


***

### Welcome to the "Taeniurus" Project Wiki.
### Project Taeniurus Information:
&nbsp;&nbsp;&nbsp;&nbsp;Taeniurus is an IRC bot written in the python programming language.

Taeniurus is also a snake ([Orthriophis taeniurus](http://en.wikipedia.org/wiki/Orthriophis_taeniurus)).

The name was chosen because I really like snakes!

The project is licensed under the GNU General Public License Version 3 (http://www.gnu.org/licenses/gpl-3.0.html).

I would recommend you to read the license completely and then use
the bot so there would be no problem for neither of us.

**_The main idea on creating this Project is only Learning and nothing else_**.

> **As stated in the license, I DO NOT guarantee that this will work. Use at your own risk.
I DO NOT take any blames on harms to your computer etc.**


## Stuff you should do before everything:
Before running it you should change something in the taeniurus.cfg file, otherwise it will connect to the default server and joins the default channel.

![taeniurus.cfg](http://ubuntuone.com/3ejammcytt9Y7iWbQTHhVD)

Default server and channel are the freenode irc network and #xprous irc channel.

### Note:
After running it you should identify yourself for the bot with the `!oper` command: 
`!oper user password`, from the irc channel you've join or via private message.

Default user and password are `admin`. When you're identified, you can change the user and the password with the `!cguser` and the `!passwd` commands:
`!cguser newuser`, `!passwd newpassword`

Taeniurus gives commands from irc and finds the code of them in the cmds.cfg file then does them with the 'exec' statement.

Please note that there is an access level per command/user, them are `oper` and `*`, if a command access's level is `oper` only an user which is identified for the bot as an oper can do the command, and `*` is for all users.

(Writing this wiki will be completed when we have more free time!)