import string
import os
import glob

import unrealtoolkit.ubt


from unrealtoolkit.commands.base import BaseCommand
class Command(BaseCommand):
	def get_description(self):
		return "Makes a class for Unreal Engine 4 without having to open the Editor"

	def get_help(self):
		return "No help available"

	def run(self, args):
		uproject = unrealtoolkit.ubt.get_uproject()

		script_path    = os.path.dirname(os.path.realpath(__file__))
		template_path  = os.path.join(script_path, "resources", "makeclass")

		acceptable_class_name = "n"
		while acceptable_class_name != "y":
			class_name = raw_input('Full C++ Class Name (with prefix): ')
			if class_name == "":
				continue

			# Check the input
			if class_name[0] != "U" and class_name[0] != "A" and class_name[0] != "S" and class_name[0] != "I" and class_name[0] != "F":
				print("Class name not accepted, must start with U (if object), A (if actor), F (if non object) or S (if Slate)")
				continue

			acceptable_class_name = raw_input(class_name + "? Y/n: ")
			if acceptable_class_name == "":
				acceptable_class_name = "y"

		file_name = class_name[1:]

		# Read the templated files
		hTpl   = open(os.path.join(template_path, 'public.h'), 'r').read()
		cppTpl = open(os.path.join(template_path, 'private.cpp'), 'r').read()

		# Write header file
		header = string.replace(hTpl, "<%className%>", class_name)
		header = string.replace(header, "<%fileName%>", file_name)
		header = string.replace(header, "<%apiNamespace%>", uproject.file_name.upper())
		f = open(os.path.normpath(os.path.join(uproject.path, 'Source', uproject.file_name, file_name + ".h")), 'w')
		f.write(header)
		f.close()

		# Write cpp file
		cpp = string.replace(cppTpl, "<%className%>", class_name)
		cpp = string.replace(cpp, "<%fileName%>", file_name)
		cpp = string.replace(cpp, "<%apiNamespace%>", uproject.file_name.upper())
		f = open(os.path.normpath(os.path.join(uproject.path, 'Source', uproject.file_name, file_name + ".cpp")), 'w')
		f.write(cpp)
		f.close()

		print("Class made, don't forget to regenerate your project if you're done, use \"unrealtoolkit regenproject\" to regen")