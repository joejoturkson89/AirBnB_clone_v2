#!/usr/bin/python3
"""This module for Fabric script that generates a tgz archive."""
import os
from datetime import datetime
from fabric.api import local, runs_once
import tarfile

def do_pack():
    
    try:
        name = "web_static_" + datetime.now().strftime("%Y%m%d%H%M%S")
        local('mkdir -p versions')
        local("tar -cvzf versions/{}.tgz {}".format(
            name, "web_static/"))
        size = os.path.getsize("./version/{}.tgz".format(name))
        print("web_static packed: versions/{}.tgz -> {}Bytes".format(
            name, size))
    except:
        return None
