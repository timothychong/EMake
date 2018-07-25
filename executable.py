#!/usr/bin/env python

import sys

import time
from random import randint

def main():

    a = int(sys.argv[1])
    b = int(sys.argv[2])

    out = -1
    time.sleep (5 + randint(0, 5))

    if (a < 5 and b < 5):
        out = 0
    elif (a < 5):
        out = 1
    elif (b < 5):
        out = 2
    else:
        out = 2


    with open("out", "w") as handle:
        handle.write(str(out))

if __name__ == "__main__":
    main()
