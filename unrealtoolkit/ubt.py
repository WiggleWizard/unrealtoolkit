import subprocess
import glob
import os
import json
import _winreg


class UProject():
	path          = None
	file_name     = None
	info          = None
	installed_dir = None

	def __init__(self, path):
		self.path, self.name = os.path.split(path)
		self.file_name, _    = self.name.split('.')

		with open(path) as f:
			self.info = json.load(f)

		registry_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\EpicGames\\Unreal Engine\\" + self.info['EngineAssociation'], 0, _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
		value, _ = _winreg.QueryValueEx(registry_key, "InstalledDirectory")
		_winreg.CloseKey(registry_key)

		self.installed_dir = value + "/Engine/Binaries/DotNET/UnrealBuildTool.exe"

	def get_ubt_path(self):
		return self.installed_dir

	def generate_project(self):
		ubt_path = self.get_ubt_path()
		project_path = os.path.join(self.path, self.file_name + ".uproject")

		process = subprocess.Popen([ubt_path, '-projectfiles', '-project=' + project_path, '-game', '-rocket', '-progress'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		for c in iter(process.stdout.readline, b''):
			print(c.rstrip())

		for c in iter(process.stderr.readline, b''):
			print(c.rstrip())

		process.stderr.close()
		process.stdout.close()

		process.wait()

	def save_info(self):
		project_full_path = os.path.join(self.path, self.file_name + ".uproject")
		with open(project_full_path, "w") as uproject_file:
			uproject_file.write(json.dumps(self.info, indent=4, sort_keys=True))

def get_uproject_file(search_path=None):
	cwd = os.getcwd()

	potential_project_files = [
		"*.uproject",
		"../../../*.uproject" # Could be when in a plugin path
	]

	if not search_path:
		search_path = cwd

	# Look for a uproject file
	for project_file_path in potential_project_files:
		project_file = glob.glob(os.path.join(search_path, project_file_path))
		if project_file:
			return project_file[0]

	return None

def get_uproject(search_path=None):
	uproject_file_path = get_uproject_file(search_path)
	if uproject_file_path == None:
		return None

	return UProject(uproject_file_path)