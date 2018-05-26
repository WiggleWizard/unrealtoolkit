![alt text](logo.png)

A toolkit designed to assist with Unreal Engine game development. Utilities range from generating a devkit of your game to making a class without opening the Editor. See the [Commands](#commands) section for a set of available commands.

The tool can also allow pre / post build hooking to expose each step to a Python script. See the [Build Hooks](#build-hooks) section for more information on that.

----

## Installation
_Note: Unrealtoolkit requires Python 2.7_
- Clone [unrealtoolkit](https://github.com/Zinglish/unrealtoolkit) to any location.
- Run `setup` from any command line tool within the unrealtoolkit directory.
- Restart your command line tool or open a new one and type `unrealtoolkit version` to confirm the tool installed correctly.

During the setup process, the tool will adjust your user `PATH` environment variable to add the absolute path to the `bin` directory so you can use unrealtoolkit from command line in any location.

Currently unrealtoolkit has only been tested on Windows 10.

# Commands
## Usage
See `unrealtoolkit --help` for a list of commands. To get further help on a specific command you can use `unrealtoolkit --help <command>`.

Most, if not all, commands should be run in either your root project (with a *.uproject file in the root) or run within the root of a plugin directory.

Available commands:
- [build](#build-hooks):           Provides commands to hook into parts of the build process of your Unreal Engine 4 project
- devkit:          Makes a developer kit version of your game
- makeclass:       Makes a class for Unreal Engine 4 without having to open the Editor
- regenproject:    Generates Visual Studio project files
- ue4version:      Prints the Unreal Engine 4 version the project uses
- version:         Prints the current version of unrealtoolkit installed

# Build Hooks
It's possible to use unrealtoolkit to allow post / pre build Python scripts in your project. One example you may use this for is to increase a build / version number upon building a shipping version of your game.

To install these hooks you can run `unrealtoolkit build generate`. This will modify your .uproject file to include the necessary lines in your `.uproject` file and will also generate a skeleton build script for you in the root of your project.