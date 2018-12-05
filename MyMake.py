#!/usr/bin/env python

import sys
sys.path.insert(0, './EMake')
from experiment_make import ExperimentMake, pjoin
from shutil import copy2
import os
import stat

class MyMake (ExperimentMake):

    my_targets = range(1, 81)
    makefile = "Makefile-run"
    output_folder = "output"

    def run_setup(self, rundir, pwd, params):

        copy2(pjoin(rundir, "setup.sh"), pwd)


    def gather_result(self):
        return []

    def targets(self):
        self.my_targets = {}

        for batch_size in [2 ** j for j in range(2, 7)]:
            self.my_targets[batch_size] = {}
            for container_per_compute in [2 * j for j in range(1, 4)]:
                self.my_targets[batch_size][container_per_compute] = [2 ** j for j in range(2, 5)]

        return self.my_targets

    def run_command(self, rundir, pwd, params):
        # batch_size = params[0]
        # container_per_compute = params[1]
        # n_thread = params[2]
        s = "./setup.sh {} {} {} {}".format(params[0], params[1], params[2], pwd)
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

