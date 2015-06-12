# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    @task(1)
    def index(self):
        self.client.get("/")

    @task(1)
    def auth(self):
        self.client.get("/auth")


class WebSiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 900
