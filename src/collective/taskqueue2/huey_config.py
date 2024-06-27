from collective.taskqueue2.huey_logger import LOG
from collective.taskqueue2.interfaces import IAsyncContext
from huey import FileHuey
from huey import MemoryHuey
from huey import RedisHuey
from huey import SqliteHuey
from huey.signals import SIGNAL_ERROR 
from huey.signals import SIGNAL_LOCKED 
from huey.signals import SIGNAL_CANCELED 
from huey.signals import SIGNAL_REVOKED 
from huey.signals import SIGNAL_COMPLETE 
from zope.component import getAdapter

import furl
import importlib
import os
import sys


default_huey_url = "sqlite:///tmp/huey_queue.sqlite"

tasks_folder_id = "tasks-folder"
tasks_folder_title = "Cartella Tasks"

def get_huey_taskqueue():
    """Return a Huey taskqueue instance"""

    huey_url = os.environ.get("HUEY_TASKQUEUE_URL", default_huey_url)
    parsed_url = furl.furl(huey_url)
    scheme = parsed_url.scheme

    if scheme == "sqlite":
        return SqliteHuey(filename=str(parsed_url.path))
    elif scheme == "redis":
        # requires redis-py
        return RedisHuey(
            host=parsed_url.host,
            port=parsed_url.port,
            password=parsed_url.password,
            db=int(str(parsed_url.path).lstrip("/")),
        )
    elif scheme == "memory":
        return MemoryHuey()
    elif scheme == "file":
        return FileHuey(path=str(parsed_url.path))
    else:
        raise ValueError(
            f"No proper configuration for $HUEY_TASKQUEUE_URL found ({huey_url}"
        )
    

huey_taskqueue = get_huey_taskqueue()


@huey_taskqueue.signal(SIGNAL_ERROR, SIGNAL_LOCKED, SIGNAL_CANCELED, SIGNAL_REVOKED)
def task_not_executed_handler(signal, task, exc=None):
    # This handler will be called for the 4 signals listed, which
    # correspond to error conditions.
    print('[%s] %s - not executed' % (signal, task.id))

@huey_taskqueue.signal(SIGNAL_COMPLETE)
def task_success(signal, task):
    # This handle will be called for each task that completes successfully.
    pass

LOG.info(f"Using taskqueue {huey_taskqueue}, {huey_taskqueue.__dict__}")
