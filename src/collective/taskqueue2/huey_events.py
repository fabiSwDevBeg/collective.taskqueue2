from plone import api
from collective.taskqueue2.huey_config import huey_taskqueue
from zope.component.hooks import setSite
from huey.constants import EmptyData
import datetime
import transaction
import time
import json


log_status_types = ['PENDING', 'STARTED', 'TERMINATED']

class Progress:
    def __init__(self, plone):
        setSite(plone)
        self.start_time = time.time()

    def elapsed_time(self):
        current_time = time.time()
        elapsed = current_time - self.start_time
        return elapsed    

    def update_status(self, task_name, message, status_type):
        try:
            self.dictionary = api.portal.get_registry_record('taskqueue2.logs')

            new_entry = {
                'task_id': task_name,
                'status_type': status_type,
                'data': datetime.datetime.now(),
                'message': message,
                'time_elapsed': self.elapsed_time,
            }
            print(self.dictionary)
            self.dictionary.append(new_entry)
            api.portal.set_registry_record('taskqueue2.logs', self.dictionary)
            transaction.manager.commit()
        except:
            return

    def update_progress(self, context, task_name, progress):
        init_dict = huey_taskqueue.storage.peek_data("/".join(context.getPhysicalPath()))
        if isinstance(init_dict, EmptyData):
            init_dict = []
        init_dict.append({
            'task_name': task_name,
            'progress': progress,
            'timestamp': datetime.datetime.now().timestamp(),
            'time_elapsed': self.elapsed_time,
        })
        huey_taskqueue.storage.put_data(context.getPhysicalPath(), json.dumps(init_dict))

    def get_progress(self, context, task_name):
        try:
            init_dict = huey_taskqueue.storage.peek_data("/".join(context.getPhysicalPath()))
            if not init_dict:
                return
            filtered_dict = [task for task in init_dict if task['task_name'] == task_name]
            if not filtered_dict:
                return
            return max(filtered_dict, key=lambda x: x['timestamp'])
        except:
            return


    def clean_dict(self, dt):
        if not isinstance(dt, datetime.datetime):
            return
        try:
            self.dictionary = [value for value in self.dictionary if value['data'] >= dt]
            self.dictionary.append({
                'task_id': 'SYSTEM',
                'status_type': 'INFO',
                'data': datetime.datetime.now(),
                'message': 'I Logs precedenti al {} sono stati eliminati.'.format(dt.strftime("%A %d %B %Y, %H:%M:%S")),
            })       
            api.portal.set_registry_record('taskqueue2.logs', self.dictionary)
            transaction.manager.commit()
        except:
            return
