#!/usr/bin/env python

import sys
sys.path.insert(0, './EMake')
from experiment_make import ExperimentMake, pjoin
from shutil import copy2
import os
import stat

class MyMake (ExperimentMake):

    my_targets = {}
    makefile = "Makefile-run"
    output_folder = "output"

    def run_setup(self, rundir, pwd, params):
        # Setting up for what's inside folder
        # for example we can copy files into folder
        copy2(pjoin(rundir, "setup.sh"), pwd)
        # Create symlink to some file in the folder to be run
        # TODO


    def gather_result(self):
        # IF we want to gather result, we add list of list of filename + extension
        return [["out", ""]]

    def targets(self):
        # All the targets we're running, separated by
        # Tarkgets in a dictionary, last level must be list, can be dictionary inside dictionary

        self.my_targets = {}

        for i in range(0,10):
            my_targets[i] = [j in range(0, 100)]

        return self.my_targets

    def run_command(self, rundir, pwd, params):
        # batch_size = params[0]
        # container_per_compute = params[1]
        # n_thread = params[2]
        s = "./setup.sh {} {} {} {} {}".format(params[0], params[1], params[2], params[3], pwd )
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

