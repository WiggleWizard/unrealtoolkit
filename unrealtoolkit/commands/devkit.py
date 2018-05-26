import os
import sys
import zipfile
import glob
import zlib

from unrealtoolkit.commands.base import BaseCommand
import unrealtoolkit.ubt


class Command(BaseCommand):
	def get_description(self):
		return "Makes a developer kit version of your game"

	def run(self, args):
		search_terms = [
			{
				"":
				[
					"*.uproject"
				]
			},
			{
				"Binaries/Win64":
				[
					"*.dll",
					"*.target",
					"*.modules",
				]
			},

			"Content",
			"Config"
		]

		plugin_search_terms = [
			{
				"":
				[
					"*.uplugin"
				]
			},
			{
				"Binaries/Win64":
				[
					"*.dll",
					"*.modules"
				]
			}
		]

		if len(sys.argv) < 3:
			print("[-] Destination path required")
			return

		# Make destination if not existing
		dest = sys.argv[2]
		dest_path, _ = os.path.split(dest)
		if not os.path.exists(dest_path):
			os.makedirs(dest_path)

		uproject_file_path, uproject_file_name = os.path.split(unrealtoolkit.ubt.get_uproject_file())

		if uproject_file_path == "":
			print("unrealtoolkit: no .uproject file to generate in working directory")
			return
		print("[+] Found UE4 Project file: " + uproject_file_name)

		zf = zipfile.ZipFile(os.path.abspath(dest) + '.zip', mode='w')

		for search_term in search_terms:
			directory = ""

			if type(search_term) == str:
				directory = search_term
				
				if directory == "":
					print("[+] Packing root")
				else:
					print("[+] Packing " + directory)

				for root, _, filenames in os.walk(directory):
					for filename in filenames:
						full_path = os.path.join(root, filename)
						print(u" \u251C\u2500 " + full_path)
						zf.write(full_path, arcname=full_path, compress_type=zipfile.ZIP_DEFLATED)
			else:
				directory = search_term.keys()[0]
				
				print("[+] Packing " + directory)

				for search_glob in search_term[directory]:
					glob_find = glob.glob(os.path.join(directory, search_glob))
					for file in glob_find:
						print(u" \u251C\u2500 " + file)
						zf.write(file, arcname=file, compress_type=zipfile.ZIP_DEFLATED)

		for plugin_dir in os.listdir("Plugins"):
			for plugin_search_term in plugin_search_terms:
				directory = ""

				if type(plugin_search_term) == str:
					continue
				else:
					directory = plugin_search_term.keys()[0]
					full_path = os.path.join("Plugins", plugin_dir, directory)
					
					print("[+] Packing " + directory)

					for search_glob in plugin_search_term[directory]:
						glob_find = glob.glob(os.path.join(full_path, search_glob))
						for file in glob_find:
							print(u" \u251C\u2500 " + file)

							zf.write(file, arcname=file, compress_type=zipfile.ZIP_DEFLATED)

		zf.close()