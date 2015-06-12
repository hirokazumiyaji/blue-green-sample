# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from datetime import datetime
import time

from fabric.api import cd, sudo, run as fabrun, env, settings, abort, hide

env.use_ssh_config = True
env.ssh_config_path = "ssh.config"

CONTAINER_PORT = {
    "blue": "4567",
    "green": "4568",
}

RUN_FORMAT = "docker run -d -p {}:4567 -e SERVER_COLOR={} --name {} -t server"


def production():
    env.hosts = ["default"]


def build():
    with cd("/src"):
        sudo("docker build -t server:latest .")


def deploy():
    prepare()
    run()
    switch()
    stop()


def prepare():
    result = sudo("ls /etc/nginx/switch/blue", warn_only=True)
    if result.succeeded:
        env.current = "blue"
        env.next = "green"
    else:
        env.current = "green"
        env.next = "blue"

    result = sudo("docker ps | grep server | awk '{print $1}'")
    if result.succeeded:
        env.current_container_id = result.stdout


def _curl(port):
    endpoint = "http://localhost:{}".format(port)

    with hide('running', 'stdout', 'stderr', 'warnings'):
        return fabrun(
            "curl -LI {} -o /dev/null -w '%{{http_code}}\n' -s".format(
                endpoint))

def run():
    server_name = "{}_{}".format(
        env.next, datetime.now().strftime("%Y%m%d%H%M%S"))
    run_result = sudo(RUN_FORMAT.format(
        CONTAINER_PORT[env.next], env.next, server_name
    ))

    with settings(warn_only=True, quiet=True):
        for i in range(5):
            result = _curl(CONTAINER_PORT[env.next])
            if result.stdout == "200":
                break
            time.sleep(.5)

    if result.stdout != "200":
        stop(run_result.stdout)
        abort("request failed.")


def switch():
    sudo("mkdir -p /etc/nginx/switch")
    sudo("touch /etc/nginx/switch/{}".format(env.next))
    sudo("rm -f /etc/nginx/switch/{}".format(env.current))


def stop(container_id=None):
    if container_id is None:
        container_id = env.current_container_id

    if container_id:
        sudo("docker stop {}".format(container_id))


def ps(run_only="true"):
    if run_only in ["true", "True"]:
        sudo("docker ps")
    else:
        sudo("docker ps -a")


def images():
    sudo("docker images")


def cleancontainer():
    sudo("docker rm `docker ps -a -q`", warn_only=True)


def removeimage():
    sudo("docker rmi $(docker images | awk '/^<none>/ { print $3 }')", warn_only=True)
