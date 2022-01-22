import argparse
import os

from utils import get_project_root_dir

MyHelpFormatter = argparse.RawTextHelpFormatter

main_script = os.path.join(get_project_root_dir(), "staking_manager.py")
venv_env = os.path.join(get_project_root_dir(), "venv/bin/python3")
