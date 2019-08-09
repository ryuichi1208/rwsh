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
import readline

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


class Logger:
    """
    Class that holds format and log level for log output
    Return an instance of the log to the source
    """
    def __init__(self, name=__name__):
        self.logger = getLogger(name)
        self.logger.setLevel(DEBUG)
        formatter = Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")

        handler = StreamHandler()
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        handler = handlers.RotatingFileHandler(filename = 'your_log_path.log',
                                               maxBytes = 1048576,
                                               backupCount = 3)
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


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
        return os.environ["HOME"]
    if stat_dir(dirpath[0]) == 0:
        try:
            os.chdir(str(dirpath[0]))
        except NotADirectoryError:
            print("Not directory")
            return 1
    else:
        return 1
    return 0


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
            if stat_dir(cmd[0]) == 0:
                do_exec_cd([cmd[0]])
                return run("echo", stdout=PIPE)
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


def signal_set():
    """
    Run some of the cleanups that should be performed when
    we run signal from a builtin command context.
    I might want to also call reset parser here.
    """
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGUSR1, debug_info)


def completer(text, state):
    """
    Function called by tab completion.
    In the current implementation,
    only the directory can be completed
    """
    dir_list = os.listdir(path='.')
    options = [x for x in dir_list if x.startswith(text)]
    try:
        return options[state]
    except IndexError:
        return None

def init_completion():
    """
    Set up and initialize functions to be called
    by tab completion interactively
    """
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")


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
    # Initialization of tab completion
    init_completion()

    # Initialize the signal to be handled
    signal_set()

    # Transfer execution to interactive processing
    main()
