import os
import sys
import math
import signal
import getpass
import numpy as np
import subprocess
import colorama
from colorama import Fore, Back, Style
from threading import Timer

class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'

def handler(num, frame):
    print("\nlogout...")
    sys.exit()


def stat_dir(dirpath):
    try:
        st = os.stat(dirpath)
    except FileNotFoundError:
        print("No such file or directory")
        return 1
    return 0


def do_exec_ls_z():
    cmd = "ls"
    directory = os.listdir('.')
    for file in directory:
        if os.path.isdir(file):
            print(Color.RED + file + Color.END)
            continue
        print(file)


def do_exec_cd(dirpath):
    if len(dirpath) == 0:
        dirpath.append(os.environ["HOME"])
    if stat_dir(dirpath[0]) == 0:
        try:
            os.chdir(str(dirpath[0]))
        except NotADirectoryError:
            print("Not directory")
    return


def do_exec_cmd(cmd):
    if cmd[0] == "cd":
        do_exec_cd(cmd[1:])
    if cmd[0] == "ls" and len(cmd) > 1 and cmd[1] == "-z":
        do_exec_ls_z()
    else:
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE)
            sys.stdout.buffer.write(res.stdout)
        except FileNotFoundError:
            print(f'command not found: {cmd[0]}')
        except PermissionError:
            print(f'permission denied: {cmd[0]}')
    return res


def generate_prompt():
    hostname = os.uname()[1]
    username = getpass.getuser()
    return f'{hostname}@{username} '


def main():
    prompt = generate_prompt()
    state = "🤗"
    while True:
        try :
            cmd = input(f'{prompt}{state} ').split()
            if len(cmd) == 0:
                continue
            if do_exec_cmd(cmd).returncode != 0:
                state = "😡"
                continue
            state = "🤗"
        except EOFError:
            print(Color.GREEN + "logout...")
            sys.exit()
        except UnboundLocalError:
            continue


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    main()
