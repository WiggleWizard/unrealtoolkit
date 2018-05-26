import sys
import os
import glob


tool_name        = "unrealtoolkit"
commands_dir     = "commands"
exclude_commands = [
	"base",
	"__init__"
]

# Add the build system libs into the import path
script_path = os.path.dirname(os.path.realpath(__file__))
lib_path    = os.path.normpath(script_path)
sys.path.insert(0, lib_path + "/..")

def get_command_instance(command):
	import imp
	command = imp.load_source('Command', lib_path + "/" + commands_dir + "/" + command + ".py")
	return command.Command()

if len(sys.argv) == 1:
	print(tool_name + ": see '" + tool_name + " --help'")
	exit()

# Intersect --help switch
if sys.argv[1] == "--help":
	if len(sys.argv) == 2:
		print("Available " + tool_name + " commands:")
		commands = []
		longest_cmd_name_len = 0

		# Iterate over the available commands in the commands directory
		for filename in os.listdir(lib_path + "/" + commands_dir):
			if filename.endswith(".py"):
				cmd_name = os.path.splitext(filename)[0]

				if cmd_name not in exclude_commands:
					commands.append(cmd_name)

					if len(cmd_name) > longest_cmd_name_len:
						longest_cmd_name_len = len(cmd_name)
			else:
				continue

		for cmd_name in commands:
			cmd_description = get_command_instance(cmd_name).get_description()
			print("    " + cmd_name + ":    " + (" " * (longest_cmd_name_len - len(cmd_name))) + cmd_description)
	else:
		cwd      = os.getcwd()
		app_name = sys.argv[2]
		app_path = lib_path + "/" + commands_dir + "/" + app_name + ".py"

		if not os.path.isfile(app_path):
			print(tool_name + ": '" + app_name + "' is not a unrealtoolkit command. See '" + tool_name + " --help'.")
			exit()

		import imp
		command          = imp.load_source('Command', app_path)
		command_instance = command.Command()
		print(command_instance.get_help())

	exit()
		
cwd = os.getcwd()
app_name = sys.argv[1]
app_path = lib_path + "/" + commands_dir + "/" + app_name + ".py"

# Check to see if the specific application exists
if not os.path.isfile(app_path):
	print(tool_name + ": '" + app_name + "' is not a unrealtoolkit command. See '" + tool_name + " --help'.")
	exit()

# Run the application
import imp
command          = imp.load_source('Command', app_path)
command_instance = command.Command()
command_instance.run(sys.argv[2:])