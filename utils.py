import os
import sys
from subprocess import Popen, PIPE, STDOUT


def get_project_root_dir():
    return os.path.dirname(os.path.abspath(__file__))


def print_debug(print_me):
    print(f"\n**************** {print_me} ****************\n")


def executeCliCommand(venv_env, main_script, func, *args):
    cmd_list = [venv_env, main_script]
    for arg in args:
        cmd_list.append(arg)
    if sys.platform.lower().startswith("win"):
        p = Popen(cmd_list, text=True, shell=True, stdin=PIPE, stdout=PIPE,
                  stderr=STDOUT)
    else:
        p = Popen(cmd_list, text=True, stdin=PIPE, stdout=PIPE,
                  stderr=STDOUT)
    std_in, sdt_out = p.communicate()
    print_debug(f"{func} \n{std_in}")
    return std_in, sdt_out
