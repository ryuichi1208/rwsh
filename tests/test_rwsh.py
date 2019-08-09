import os
import sys
import pytest
sys.path.append('.')
from rwsh import *

def test_init_completion():
   assert init_completion() == None

def test_do_exec_ls_z():
    assert do_exec_ls_z() == None

def test_do_exec_ls_z():
    assert do_exec_ls_z() == None

def test_generate_prompt():
    hostname = os.uname()[1]
    username = getpass.getuser()
    assert generate_prompt() == f'{hostname}@{username} '

@pytest.mark.parametrize("dirpath, res",
                         [("notdir", 1),
                          (".", 0),
                          ("..", 0),
                          ("getstat",1)
                         ])
def test_stat_dir(dirpath, res):
    assert stat_dir(dirpath) == res

@pytest.mark.parametrize("dirpath, res",
                         [(["notdir"], 1),
                          ([], os.environ["HOME"]),
                          (["."], 0),
                          ([".."], 0),
                          (["getstat"],1)
                         ])
def test_do_exec_cd(dirpath, res):
    assert do_exec_cd(dirpath) == res
