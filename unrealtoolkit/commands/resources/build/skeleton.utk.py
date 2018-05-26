import os
import re
import sys


from unrealtoolkit.project import UTKProject
class Project(UTKProject):
	def post_build(self, build_variables):
		# Increase the shipping build number
		if build_variables['TargetConfiguration'] == "Shipping":
			version_file_path = os.path.join(self.project_path, 'Source/<%project_name%>/GameVersion.h')
			file_data = ""
			with open(version_file_path, 'r') as file :
				file_data = file.read()
			
			regex = r'\#define GAME_BUILD_NUMBER (\d+)'
			match = re.search(regex, file_data, re.MULTILINE)
			current_build = int(match.group(1))
			new_file_data = re.sub(regex, "#define GAME_BUILD_NUMBER " + str(current_build + 1), file_data)
		
			with open(version_file_path, 'w') as file:
				file.write(new_file_data)