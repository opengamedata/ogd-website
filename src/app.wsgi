import os
import site
import sys
from pathlib import Path

# Ensure this path is writable by the user the WSGI daemon runs as
os.environ['OGD_FLASK_APP_LOG_FILE'] = '/var/log/flask-apps/ogd-website.log'

HOME_FOLDER = "placeholder home"


# Specifying the path used in the hosting environment, there might be a better way to do this
if not HOME_FOLDER in sys.path:
    sys.path.append(HOME_FOLDER)

from config.AppConfig import AppConfig
if not AppConfig.APP_CONFIG['LOCAL']:
    py_version = ".".join([str(sys.version_info.major), str(sys.version_info.minor)])
    packages_dir = Path(HOME_FOLDER) / "lib" / f"python{py_version}" / "site-packages"

    site.addsitedir(str(packages_dir))
    sys.path.insert(0, sys.path.pop()) # Move venv sitedir to front of sys.path

    # os.chdir(HOME_FOLDER)
    # activation_file = Path(HOME_FOLDER) / ".venv" / "bin" / "activate_this.py"
    # with open(activation_file, encoding="UTF-8") as activate:
    #     exec(activate.read(), {"__file__":activation_file}) # necessary HACK pylint: disable=exec-used

from app import application
