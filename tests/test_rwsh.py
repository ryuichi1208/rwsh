import os
import sys
import pytest
sys.path.append('.')
from rwsh import *

class RoIAlign(Module):

    def __init__(self, out_size, spatial_scale, sample_num=0):
        super(RoIAlign, self).__init__()

        self.out_size = out_size
        self.spatial_scale = float(spatial_scale)
        self.sample_num = int(sample_num)

    def forward(self, features, rois):
        return RoIAlignFunction.apply(features, rois, self.out_size,
                                      self.spatial_scale, self.sample_num)

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
