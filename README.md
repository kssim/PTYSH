## PTYSH
PTYSH is an abbreviation of 'Python Teletype Shell'.
It was made with reference to the 'zebra vtysh'.
Vtysh is an integrated shell for Quagga routing software.

Ptysh is not the only route shell, the shell is customizable, so you can normally use.
It made it possible to add commands to the module for availability.



## Usage
### Start shell
When you run the 'ptysh_main.py', the shell begins.
You can use the commands summarized below.
During PTYSH to use commands such as ctrl-c and ctrl-z does not work.


### Add custom module
To add a module, you will create a file with reference to the sample code in the "modules" directory.
You can create additional logic inherit the class ptysh_module.


## Command
### disable mode
1. enable
	* Enter the control shell
	* It required password. (default password is ptysh)
2. exit
	* exit the shell.
3. list
	* show command list.
4. st
	* start-shell (default shell is bash)
	* It is hidden command.
	* It required password and it is same to enable password.


### enable mod
1. diable
	* exit the enable mode
2. exit
	* exit the shell.
3. list
	* show command list.
4. configure terminal
	* It is control menu for other modules.

### configure terminal mode
1. exit
	* exit the shell.
2. list
	* show command list.


## Idea or Issue
If you have an idea or issue, feel free to open an issue or make pull request.