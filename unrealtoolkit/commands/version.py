import os
import sys
import json

import unrealtoolkit.env


from unrealtoolkit.commands.base import BaseCommand
class Command(BaseCommand):
	def get_description(self):
		return "Prints the current version of unrealtoolkit installed"

	def run(self, args):
		version = open(unrealtoolkit.env.get_project_root_dir() + "/version", 'r').read()
		print("unrealtoolkit v" + version)
