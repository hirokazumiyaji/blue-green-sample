# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from fabric.api import cd, run as fabrun, shell_env


CONTAINER_PORT = {
    "blue": "4567",
    "green": "4568",
}


def production():
    env.user = "vagrant"
    env.hosts = ["192.168.33.10"]


def build():
    with cd("/src"):
        fabrun("sudo docker build -t server:latest .")


def deploy():
    prepare()
    run()
    switch()
    stop()


def prepare():
    result = run("ls /etc/nginx/switch/blue")
    env.current = ""
    env.next = ""


def run():
    fabrun("sudo docker run -d -p {}:4567 -e SERVER_COLOR={} -t server".format(
        CONTAINER_PORT[env.current], env.next,
    ))


def switch():
    fabrun("sudo mkdir -p /etc/nginx/switch")
    fabrun("sudo touch /etc/nginx/switch/{}".format())
    fabrun("sudo rm /etc/nginx/switch/{}".format())


def stop():
    fabrun("sudo docker stop {}".format(env.current_container_id))
