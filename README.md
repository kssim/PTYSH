## PTYSH
PTYSH is an abbreviation of 'Python Teletype Shell'.<br>
It was made with reference to the 'zebra vtysh'.
Vtysh is an integrated shell for Quagga routing software.<br>
Ptysh is not the only route shell, the shell is customizable, so you can general purpose.<br>


## Notice
You can install PTYSH through the pip.<br>
However, you must manually install some libraries.<br>
I'll update the library list soon.<br>


## Usage
### Start shell
When you run the 'ptysh_main.py', the shell begins.<br>
You can use the commands summarized below.<br>
You can't use the command (suchs as Ctrl-Z or Ctrl-C) to use during PTYSH.<br>


### Add custom module
To add a module, you will create a file with reference to the sample code in the "modules" directory.<br>
You can create additional logic inherit the class 'ptysh_module'.<br>


## Command
### In 'disable mode'
1. enable
	* Enter the control shell
	* It is required password. (default password is ptysh)
2. exit
	* exit the shell.
3. list
	* show command list.
4. st
	* start-shell (default shell is bash)
	* It is hidden command.
	* It is required password and it is same to enable password.


### In 'enable mode'
1. diable
	* exit the enable mode
2. exit
	* exit the shell.
3. list
	* show command list.
4. configure terminal
	* It is control menu for other modules.


### In 'configure terminal mode'
1. exit
	* exit the shell.
2. list
	* show command list.
3. [Modules list]
	* show modules name list


## Plan
1. Fix the pip install configuration problem(libraries).
2. Improved stability in various environments.
3. Create wiki page and fix the readme file.



## Idea or Issue
If you have an idea or issue, feel free to open an issue or make pull request.
