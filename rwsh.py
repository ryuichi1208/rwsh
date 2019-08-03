"""
/*
 *
 * This software may be freely redistributed under the terms of the
 * GNU General Public License.
 *
 * Written by ryuichi1208 (ryucrosskey@gmail.com)
 *
 */
"""


import os
import sys
import math
import signal
import getpass
import numpy as np
import colorama
import textwrap
import uptime
import platform as pf

from datetime import datetime
from subprocess import call, run, PIPE
from colorama import Fore, Back, Style
from threading import Timer

class Color:
    """
    Define color when displaying to prompt
    """
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
    print(Color.GREEN, "\nlogout...")
    sys.exit()


def debug_info(num, frame):
    proc_info = '''
    ===== DEBUG INFO =====
     DATE   : {}
     UPTIME : {}
     OS     : {}
     CPU    : {}
     BIT    : {}
     PID    : {}
     PPID   : {}
     USER   : {}
     Python : {}
     ======================
    '''.format(
                datetime.now().strftime("%Y/%m/%d %H:%M:%S"), \
                uptime.boottime(), \
                pf.system(), \
                pf.processor(), \
                str(64 if sys.maxsize > 2**32 else 32) + " bit", \
                os.getpid(), \
                os.getppid(), \
                os.environ.get("USER"), \
                str(sys.version_info.major) + "."  + str(sys.version_info.minor)
              )

    print(Color.BLUE, "\n", textwrap.dedent(proc_info).strip())
    print(Color.END)
    return

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


def do_exec_vim(filepath):
    """
    Called when running vim.
    Since not implemented, EDITOR assumes neovim
    """
    call(["nvim", filepath])
    return


def do_exec_cmd(cmd):
    """
    Dispatch function for command execution
    Separate function calls for each command you call

    Basically, only Linux commands are accepted
    """
    if cmd[0] == "cd":
        do_exec_cd(cmd[1:])
        return run("echo", stdout=PIPE)
    if cmd[0] in ["vim", "vi"]:
        do_exec_vim(cmd[1] if len(cmd) > 1 else None)
        return run("echo", stdout=PIPE)
    if cmd[0] == "ls" and len(cmd) > 1 and cmd[1] == "-z":
        do_exec_ls_z()
    else:
        try:
            res = run(cmd, stdout=PIPE)
            sys.stdout.buffer.write(res.stdout)
        except FileNotFoundError:
            print(f'command not found: {cmd[0]}')
        except PermissionError:
            print(f'permission denied: {cmd[0]}')
    return res


def generate_prompt():
    """
    Generate a prompt to display
    """
    hostname = os.uname()[1]
    username = getpass.getuser()

    return f'{hostname}@{username} '


def main():
    prompt = generate_prompt()

    # Pictograph when end status is 0
    state = "🤗"

    """
    Receive command input in loop processing
    Send signal SIGINT to exit
    """
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
    signal.signal(signal.SIGUSR1, debug_info)
    main()
