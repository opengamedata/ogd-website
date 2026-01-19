import sys
import os
from pathlib import Path

from config.AppConfig import AppConfig

# Ensure this path is writable by the user the WSGI daemon runs as
os.environ['OGD_FLASK_APP_LOG_FILE'] = '/var/log/flask-apps/ogd-website.log'

HOME_FOLDER = "placeholder home"

if not AppConfig.APP_CONFIG['LOCAL']:
    os.chdir(HOME_FOLDER)
    activation_file = Path(HOME_FOLDER) / ".venv" / "bin" / "activate_this.py"
    with open(activation_file, encoding="UTF-8") as activate:
        exec(activate.read(), {"__file__":activation_file}) # necessary HACK pylint: disable=exec-used


# Specifying the path used in the hosting environment, there might be a better way to do this
if not HOME_FOLDER in sys.path:
    sys.path.append(HOME_FOLDER)

from app import application
