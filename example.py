#!/usr/bin/env python

import os
import sys
import stat
from shutil import copy2

EMAKE_DIR = os.environ.get('EMAKE_DIR')
if EMAKE_DIR is None:
    print "EMAKE_DIR not set"
    exit(-1)
else:
    print "EMake directory: {}".format(EMAKE_DIR)

sys.path.insert(0, EMAKE_DIR + "/EMake")
from experiment_make import ExperimentMake, pjoin, symlnk

class MyMake (ExperimentMake):

    my_targets = {}
    makefile = "Makefile-run"
    output_folder = "output"

    def run_setup(self, rundir, pwd, params):
        # Setting up for what's inside folder
        # Create symlink to some file in the folder to be run
        symlnk(rundir, pwd, "setup.sh")

    def run_dependency(self, rundir, pwd, params):
        # Dependency for target
        #TODO
        return []

    def gather_result(self):
        # IF we want to gather result, we add list of list of filename + extension
        return [["out", ""]]

    def targets(self):
        # All the targets we're running, separated by
        # Tarkgets in a dictionary, last level must be list, can be dictionary inside dictionary
        self.my_targets = {}

        for i in range(0,10):
            self.my_targets[i] = [j for j in range(10, 20)]
        return self.my_targets

    def run_command(self, rundir, pwd, params):
        # batch_size = params[0]
        # container_per_compute = params[1]
        # n_thread = params[2]
        s = "./setup.sh {} {} {}".format(params[0], params[1], pwd)
        return s

    def __init__(self):
        self.my_targets = self.targets()

def main():
    m = MyMake()
    m.validate()
    m.setup_folders()
    m.run_setup_all()
    m.gen_make()

if __name__ == "__main__":
    main()

