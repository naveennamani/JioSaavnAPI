import os
from threading import Thread
from typing import Dict

import requests


class TaskManager(object):
    def __init__(self):
        self.task_id = 1000
        self.tasks = {}  # type: Dict[int,str]
        self.task_threads = {}  # type: Dict[int,Thread]

    def add_task(self, task: str) -> int:
        print("creating task", task, self.task_id)
        thread = Thread(target = download_file, args = [task])
        thread.start()
        self.tasks[self.task_id] = task
        self.task_threads[self.task_id] = thread
        self.task_id += 1
        return self.task_id - 1

    def get_task_status(self, task_id: int) -> bool:
        print("getting task status", task_id)
        if task_id not in self.tasks:
            return False
        return os.path.exists(resolve_file_name(self.tasks[task_id]))

    def del_task(self, task_id: int):
        print("deleting task", task_id)
        if task_id not in self.tasks:
            return
        if self.task_threads[task_id].is_alive():
            try:
                self.task_threads[task_id]._stop()
            except:
                pass
        if os.path.exists(resolve_file_name(self.tasks[task_id])):
            os.remove(resolve_file_name(self.tasks[task_id]))


def download_file(url: str):
    try:
        print("downloading file", url)
        resp = requests.head(url, allow_redirects = True)
        print(resp.text, resp.url)
        resp = requests.get(resp.url, allow_redirects = True)
        # print(resp.text)
        print(resp.url)
        with open(resolve_file_name(url), "wb") as fh:
            fh.write(resp.content)
        print("downloaded", url)
    except Exception:
        from traceback import print_exc
        print_exc()


def resolve_file_name(url: str):
    return url.split('/')[-1]
