#!/usr/bin/python3
""" This Fabric script distributes an archive to yyou we server."""
from datetime import datetime
from fabric.api import *
import os

env.hosts = ["52.72.30.141", "54.87.253.86"]
env.user = "ubuntu"

def do_pack():
    """Return the archive path if archive generates correctly."""

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(archived_f_path))

    if t_gzip_archive.succeeded:
        return archived_f_path
    else:
        return None

def do_deploy(archive_path):
    """This script distributes archives."""

    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file, newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version, newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".fomat(newest_version))

        print("New version deployed!")
        return True
    except:
        print("New version not deployed...")
        return false


def deploy():
    """This script automates everything."""

    ap = do_pack()
    if ap is None:
        return False
    return do_deploy(ap)
