from collective.taskqueue2.huey_logger import LOG
from huey import FileHuey
from huey import MemoryHuey
from huey import RedisHuey
from huey import SqliteHuey

import furl
import os
import sys
import importlib


default_huey_url = "sqlite:///tmp/huey_queue.sqlite"


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
    
def run_buildout_tasks(huey_taskqueue):
    config_path = os.path.join(str(os.getcwd()).replace("/bin", ""), 'parts/taskqueue2')
    sys.path.append(config_path)
    import taskqueue2config
    sys.path.remove(config_path)
    #huey_taskqueue.revoke_all()
    if hasattr(taskqueue2config, 'task_schedule'):
        for task_name, task_dict in taskqueue2config.task_schedule.items():
            task_path = task_dict.get('task')
            task_schedule = task_dict.get('schedule')
            if task_path:
                module_path, function_name = task_path.rsplit('.', 1)
                try:
                    module = importlib.import_module(module_path)
                    task_function = getattr(module, function_name)
                    #Succedeva perchè importando il modulo che conteneva 
                    #la funzione già decorata con .task partiva il task
                    #huey_taskqueue._registry.unregister(huey_taskqueue._registry._registry[task_path])
                    huey_taskqueue.periodic_task(task_schedule)(task_function)
                    print(f"Eseguito {task_path}")
                except (ModuleNotFoundError, AttributeError) as e:
                    print(f"Errore nell'importare o eseguire {task_path}: {e}")            

huey_taskqueue = get_huey_taskqueue()
huey_tasks = run_buildout_tasks(huey_taskqueue)

LOG.info(f"Using taskqueue {huey_taskqueue}, {huey_taskqueue.__dict__}")
