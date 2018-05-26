import os
from ctypes import windll
import _winreg

def update_sys_environment():
	HWND_BROADCAST = 0xffff
	WM_SETTINGCHANGE = 0x001A
	SMTO_ABORTIFHUNG = 0x0002
	lparam = "Environment"
	return True if windll.user32.SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, unicode(lparam), SMTO_ABORTIFHUNG, 5000, 0) == 1 else False

def add_to_user_path(new_path):
	registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Environment", 0, _winreg.KEY_READ)
	value, _ = _winreg.QueryValueEx(registry_key, "PATH")
	_winreg.CloseKey(registry_key)

	path_already_exists = False
	paths = value.split(";")
	for path in paths:
		if path == new_path:
			path_already_exists = True
			return True

	if path_already_exists == False:
		paths.append(new_path)
		registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Environment", 0, _winreg.KEY_WRITE)
		_winreg.SetValueEx(registry_key, "PATH", 0, _winreg.REG_SZ, ";".join(paths))
		_winreg.CloseKey(registry_key)
	
	return True

def get_project_root_dir():
	script_path = os.path.dirname(os.path.realpath(__file__))
	return os.path.abspath(os.path.join(script_path, ".."))