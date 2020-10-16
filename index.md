# True Documentation
Welcome to the official True BOT documentation. This page has been created by Sal Code, Owner & Developer of True BOT.

## Commands

* `t!help`: The help command shows a window with all the fundamentals instructions that the user can follow to use True in the best way.<br />_The following command create a direct channel to message with the user. All the messages sent with this mode can be only red by the author of the message_.

* `t!cmd`: The cmd command shows the list od all the commands which can be used by a user; This command contains only the users commands, not the Staff's commands.<br />_The following command create a direct channel to message with the user. All the messages sent with this mode can be only red by the author of the message_.

* `t!helpstaff`: The following command shows a list of all the staff's dedicates commands and to use them on the server.<br />_The following command create a direct channel to message with the user. All the messages sent with this mode can be only red by the author of the message_.

* `t!ticket`: The following commands create a custom ticket for the user where he can get support from the Staff. It will be created a private support channel with the syntax **❗ticket** followed by the user name and tag. With this, True will automatically create a custom role, called **❗ticket** follows by the user name and tag. The channel can be accessed only by the Staff members and the user.<br />**⚠ _We reccomend the user to use only one ticket per time. Creating more than 1 ticket could probably be a warn_**

* `t!usereport`: If a user make a profanity, doesn't follow the server rules or simply does something wrong, you can report that user to the Staff by using the following command.

* `t!bugreport`: If you find a bug on the server, it's always good to report it to the Staff. Use this command to warn bugs.

* `t!verify`: If you join in a server where the verification system's on, to verify yourself in the guild, go the **#✅verify** channel and type the following command.

* `t!how_to`: If you want to know how to change True's settings in your server, use this command to see the commands to change the management of your guild.<br />_This command has more than one page. To switch from a page to another, use the emojies provided by True reacting to the message._

* `t!ban`: Use this command to ban a user from the server. This command can be used only by staff members. _Syntax: t!ban @username reason_.

* `t!kick`: Use this command to kick a user from the server. This command can be used only by staff members. _Syntax: t!kick @username reason_.

* `t!sudo`: Use this command to warn a user for his/her wrong behavior. This command can be used only by staff members. _Syntax: t!sudo @username reason_.

* `t!mute`: Use this command to mute a user on the server. This command can be used only by staff members. _Syntax: t!mute @username time reason_.

* `t!unmute`: Use this command to un mute a user on the server. This command can be used only by staff members. _Syntax: t!unmute @username_.

## How to contribute - Applying changes
If you want to apply changes to the actual version of True, you can make this by cloning the source code into your local machine.

#### Cloning the repository into the local machine
```bash
    cd workspace
    git clone https://github.com/Salazar34/True.git
```

#### Change the documentation
Before appy changes to the documentation, you need to install an extra module
```bash
    pip3 install mkdocs
```
After you've correctly installed the module, you can start working on the page.
```bash
    cd workspace
    cd docs
    cd docs
```
When you're here, you can open the file called **index.md** and you can make your changes to the documentation page of the server. To see the live changes to the documentation:
```bash
    mkdocs serve
```
Copy & Paste the local host adress in your browser.<br />After yoiu've finished your work, delete the **site** folder & then re-create the folder with the new changes; To do this, use the following commands
```bash
    rm -r site
    mkdocs build
```

## Bug report
> If you find any bug using True, If you want to contribute to the project, you can report that bug by using the [Google Forms](https://forms.gle/sH97ZjbR7opgU9ic6) or you can join our [Discord server](https://discord.gg/bXTMz9T). We will remember your contribute for our mission.<br />If you have some ideas or suggestions, join our [Discord server](https://discord.gg/bXTMz9T) to express your opinion. Thank You!