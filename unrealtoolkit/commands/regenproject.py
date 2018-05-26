import os
import glob

import unrealtoolkit.ubt


from unrealtoolkit.commands.base import BaseCommand
class Command(BaseCommand):
	def get_description(self):
		return "Generates Visual Studio project files"

	def run(self, args):
		# Look for a uproject file
		uproject = unrealtoolkit.ubt.get_uproject()

		if not uproject:
			print("unrealtoolkit: no .uproject file to generate in working directory")
			return

		uproject.generate_project()

		