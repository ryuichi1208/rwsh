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
import pwd
import grp
import typing
import multiprocessing
import time
import json
import pickle

from datetime import datetime
from subprocess import call, run, PIPE
from colorama import Fore, Back, Style
from threading import Timer


class Speaker:
    def __init__(self, root: str):
        self.root = root
        self.name = root.name
        self.utterances = None
        self.utterance_cycler = None


"""
colormap = np.array([
    [76, 255, 0],
    [0, 127, 70],
    [255, 0, 0],
    [255, 217, 38],
    [0, 135, 255],
    [165, 0, 165],
    [255, 167, 255],
    [0, 255, 255],
    [255, 96, 38],
    [142, 76, 0],
    [33, 0, 127],
    [0, 0, 0],
    [183, 183, 183],
], dtype=np.float) / 255
"""


class Color:
    """
    Define color when displaying to prompt
    """

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    END = "\033[0m"
    BOLD = "\038[1m"
    UNDERLINE = "\033[4m"
    INVISIBLE = "\033[08m"
    REVERCE = "\033[07m"


class Logger:
    """
    Class that holds format and log level for log output
    Return an instance of the log to the source
    """

    def __init__(self, name=__name__):
        self.logger = getLogger(name)
        self.logger.setLevel(DEBUG)
        formatter = Formatter(
            "[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s"
        )

        handler = StreamHandler()
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        handler = handlers.RotatingFileHandler(
            filename="your_log_path.log", maxBytes=1048576, backupCount=3
        )
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


class Utterance:
    def __init__(self, frames_fpath, wave_fpath):
        self.frames_fpath = frames_fpath
        self.wave_fpath = wave_fpath

    def get_frames(self):
        return np.load(self.frames_fpath)

    def random_partial(self, n_frames):
        frames = self.get_frames()
        if frames.shape[0] == n_frames:
            start = 0
        else:
            start = np.random.randint(0, frames.shape[0] - n_frames)
        end = start + n_frames
        return frames[start:end], (start, end)


def handler(num, frame):
    print(Color.GREEN, "\nlogout...")
    sys.exit()

    
def action(methods=list(['get']), detail=False):
    methods = [method.lower() for method in methods]

    def decorator(func):
        func.bind_to_methods = methods
        func.detail = detail
        return func
    return decorator


def debug_info(num, frame):
    proc_info = """
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
    """.format(
        datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        uptime.boottime(),
        pf.system(),
        pf.processor(),
        str(64 if sys.maxsize > 2 ** 32 else 32) + " bit",
        os.getpid(),
        os.getppid(),
        os.environ.get("USER"),
        str(sys.version_info.major) + "." + str(sys.version_info.minor),
    )

    print(Color.BLUE, "\n", textwrap.dedent(proc_info).strip())
    print(Color.END)
    return


def get_stat_dir_info(dirname: str) -> str:
    os_stat = os.stat(dirname)
    return {
        "PID": os.getpid(),
        "DIR_NAME": dirname,
        "ST_MODE": os_stat.st_mode,
        "ST_INO": os_stat.st_ino,
        "ST_DEV": os_stat.st_dev,
        "ST_NLINK": os_stat.st_nlink,
        "ST_UID": f"{os_stat.st_uid}/{pwd.getpwuid(os_stat.st_uid)[0]}",
        "ST_GID": f"{os_stat.st_gid}/{grp.getgrgid(os_stat.st_gid)[0]}",
        "ST_ATIME": os_stat.st_atime,
        "ST_MTIME": os_stat.st_mtime,
        "ST_CTIME": os_stat.st_ctime,
    }


def multi_proc_lookup_dir(cores: typing.Union[int, None] = 0, find_path: str = "."):

    if not os.path.exists(find_path):
        return "No such file or directory"

    n_cores = cores if cores else multiprocessing.cpu_count()
    proc_pool = multiprocessing.Pool(n_cores)

    dir_list = [
        f
        for f in os.listdir(path=find_path)
        if os.path.isdir(os.path.join(find_path, f))
    ]
    res = proc_pool.map(get_stat_dir_info, dir_list)
    print(json.dumps(res))


def stat_dir(dirpath):
    try:
        st = os.stat(dirpath)
    except FileNotFoundError:
        print("No such file or directory")
        return 1
    return 0


def do_exec_ls_z():
    cmd = "ls"
    directory = os.listdir(".")
    for file in directory:
        if os.path.isdir(file):
            print(Color.RED + file + Color.END)
            continue
        print(file)

def _is_whitespace(char):
  if char == " " or char == "\t" or char == "\n" or char == "\r":
    return True
  cat = unicodedata.category(char)
  if cat == "Zs":
    return True
  return False


def _is_control(char):
  if char == "\t" or char == "\n" or char == "\r":
    return False
  cat = unicodedata.category(char)
  if cat in ("Cc", "Cf"):
    return True
  return False


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
            print(f"command not found: {cmd[0]}")
        except PermissionError:
            print(f"permission denied: {cmd[0]}")
    return res


def get_random_string(length, allowed_chars="", salt=""):
    if not using_sysrandom:
        random.seed(
            hashlib.sha256(
                ("%s%s%s" % (
                    random.getstate(),
                    time.time(),
                    salt)).encode('utf-8')
            ).digest())
    return ''.join(random.choice(allowed_chars) for i in range(length))


def generate_prompt():
    """
    Generate a prompt to display
    """
    hostname = os.uname()[1]
    username = getpass.getuser()

    return f"{hostname}@{username} "


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
    dir_list = os.listdir(path=".")
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
        try:
            cmd = input(f"{prompt}{state} ").split()
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


if __name__ == "__main__":
    # Initialization of tab completion
    init_completion()

    # Initialize the signal to be handled
    signal_set()

    # Transfer execution to interactive processing
    main()

"""
def normalize_volume(wav, target_dBFS, increase_only=False, decrease_only=False):
    if increase_only and decrease_only:
        raise ValueError("Both increase only and decrease only are set")
    dBFS_change = target_dBFS - 10 * np.log10(np.mean(wav ** 2))
    if (dBFS_change < 0 and increase_only) or (dBFS_change > 0 and decrease_only):
        return wav
    return wav * (10 ** (dBFS_change / 20))
"""


def move_all_files(src_dir_path, dst_dir_path):
    paths = get_file_paths(src_dir_path)
    for p in paths:
        p = Path(p)
        p.rename(Path(dst_dir_path) / p.name)


def delete_all_files(dir_path):
    paths = get_file_paths(dir_path)
    for p in paths:
        p = Path(p)
        p.unlink()


class ls_colors_mu_class(Chunk):
    COLOR_TYPE_GRAY = 0
    COLOR_TYPE_RGB = 2
    COLOR_TYPE_PLTE = 3
    COLOR_TYPE_GRAYA = 4
    COLOR_TYPE_RGBA = 6
    color_types = {
        COLOR_TYPE_GRAY: ("Grayscale", (1, 2, 4, 8, 16)),
        COLOR_TYPE_RGB: ("RGB", (8, 16)),
        COLOR_TYPE_PLTE: ("Palette", (1, 2, 4, 8)),
        COLOR_TYPE_GRAYA: ("Greyscale+Alpha", (8, 16)),
        COLOR_TYPE_RGBA: ("RGBA", (8, 16)),
    }
