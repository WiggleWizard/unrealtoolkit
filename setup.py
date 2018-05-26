import os

import unrealtoolkit.env as env

script_path = os.path.dirname(os.path.realpath(__file__))

# Set unrealtoolkit as part of the user's path
env.add_to_user_path(os.path.join(script_path, "bin"))
env.update_sys_environment()