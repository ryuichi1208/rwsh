import os
import sys
import math
import signal
import getpass
import numpy as np
import subprocess
from threading import Timer

status = 0

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


def exec_cd(dirpath):
    if len(dirpath) == 0:
        dirpath.append(os.environ["HOME"])
    if stat_dir(dirpath[0]) == 0:
        try:
            os.chdir(str(dirpath[0]))
        except NotADirectoryError:
            print("Not directory")
    return


def exec_cmd(cmd):
    if cmd[0] == "cd":
        exec_cd(cmd[1:])
    else:
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
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
    state = "( ´∀｀)"
    while True:
        cmd = input(f'{prompt}{state} ').split()
        if len(cmd) == 0:
            continue
        if exec_cmd(cmd).returncode != 0:
            state = "(# ﾟДﾟ)"
            continue
        state = "( ´∀｀)"
        global status
        if status == 0:
            timer = Timer(3, notification, ("target", ))
            timer.start()


def notification(target):
    print(f'notification : そろそろ休憩？')
    global status
    status = 1


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)

    main()
