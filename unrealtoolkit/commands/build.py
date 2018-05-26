import os
import sys
import json
import string

import unrealtoolkit.ubt


from unrealtoolkit.commands.base import BaseCommand
class Command(BaseCommand):
	def get_help(self):
		return (
			"Usage:\n"
			"    unrealtoolkit build <command> <param...>\n\n"
			"Available build commands:\n"
			"    generate:    Generates pre / post build commands\n"
			"                 This will modify your .uproject file!")

	def get_description(self):
		return "Provides commands to hook into parts of the build process of your Unreal Engine 4 project"

	def run(self, args):
		if args[0] == "generate":
			print("Generating post build step into your Unreal Engine project")

			uproject    = unrealtoolkit.ubt.get_uproject()
			script_path = os.path.dirname(os.path.realpath(__file__))

			# Write build script
			build_tpl_path = os.path.join(script_path, "resources", "build", "skeleton.utk.py")
			build_tpl      = open(build_tpl_path, 'r').read()
			build_skeleton = string.replace(build_tpl, "<%project_name%>", uproject.file_name)
			with open(os.path.normpath(os.path.join(uproject.path, uproject.file_name + ".utk.py")), 'w') as f:
				f.write(build_skeleton)
				f.close()

			# Write the game version header
			gameversion_h_path = os.path.join(script_path, "resources", "build", "GameVersion.h")
			gameversion_h      = open(gameversion_h_path, 'r').read()
			with open(os.path.normpath(os.path.join(uproject.path, "Source", uproject.file_name, "GameVersion.h")), 'w') as f:
				f.write(gameversion_h)
				f.close()

			# Modify the uproject
			uproject.info['PostBuildSteps'] = {
				"Win64": ["unrealtoolkit build post $(ProjectDir) \"variables={\\\"TargetConfiguration\\\": \\\"$(TargetConfiguration)\\\"}\""]
			}
			uproject.save_info()

			return

		if len(sys.argv) < 4:
			print("Needs more args")
			exit()

		build_state = sys.argv[2]
		project_dir = sys.argv[3]

		variables = json.loads(sys.argv[4][10:])

		# Project file path
		project_file_path = unrealtoolkit.ubt.get_uproject_file(project_dir)
		filename_w_ext    = os.path.basename(project_file_path)
		project_name, _   = os.path.splitext(filename_w_ext)

		# Look in the project directory for a build script
		import imp
		project_script = imp.load_source(project_name, project_dir + "/" + project_name + ".utk.py")
		project_script_instance = getattr(project_script, "Project")(project_dir)

		if build_state == "post":
			project_script_instance.post_build(variables)
