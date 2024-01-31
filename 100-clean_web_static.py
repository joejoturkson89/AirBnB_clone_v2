#!/usr/bin/python3
import os
from fabric.api import *

env.hosts = ['52.72.30.141', '54.87.253.86']

def do_clean(number=0):
    """This script deletes out-of-date archives."""

    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [achives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in range archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
