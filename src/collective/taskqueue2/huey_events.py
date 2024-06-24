from collective.taskqueue2.huey_config import huey_taskqueue
from collective.taskqueue2.interfaces import IAsyncContext
from huey.constants import EmptyData
from plone import api
from zope.component.hooks import setSite
from Acquisition import ImplicitAcquisitionWrapper
#from zope.interface import providedBy

import datetime
import functools
import json
import time
import transaction


log_status_types = ['FAILURE', 'SUCCESS', 'PENDING']

def check_interface(obj):
    return IAsyncContext.providedBy(obj)

def get_all_processes(context):
    try:
        if not check_interface(context):
            return            
        init_dict = huey_taskqueue.storage.peek_data(
            "/".join(context.getPhysicalPath())
        )
        if init_dict is EmptyData:
            return []
        json_string = init_dict.decode('utf-8')
        data = json.loads(json_string)
        unique_task_names = list(set(task['task_name'] for task in data))
        return unique_task_names
    except:
        return []  

class Progress:
    def __init__(self, plone, task_name):
        if isinstance(plone, ImplicitAcquisitionWrapper):
            setSite(plone)
        self.start_time = time.time()
        self.task_name = task_name
        
    def progress_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task_name = func.__name__
            app = args[0]
            try:
                nome_app = args[1][2]
                progress_manager = Progress(app[nome_app], task_name)
                return func(progress_manager, *args, **kwargs)
            except Exception as e:
                print(f"Errore nella creazione del contesto per {task_name}: {str(e)}")
                return
            
        return wrapper    

    def elapsed_time(self):
        current_time = time.time()
        elapsed = current_time - self.start_time
        return elapsed    

    def update_status(self, context, message, status_type):
        try:
            if not check_interface(context):
                return            
            dictionary = api.portal.get_registry_record('taskqueue2.logs')
            new_entry = {
                'task_id': self.task_name,
                'context_path': "/".join(context.getPhysicalPath()),
                'status_type': status_type,
                'data': datetime.datetime.now(),
                'message': message,
                'time_elapsed': self.elapsed_time(),
            }
            dictionary.append(new_entry)
            api.portal.set_registry_record('taskqueue2.logs', dictionary)
            transaction.manager.commit()
        except:
            return
        
    def get_status(self, context):
        try:
            if not check_interface(context):
                return            
            dictionary = api.portal.get_registry_record('taskqueue2.logs')
            dictionary_filtered = [entry for entry in dictionary if entry['task_id'] == self.task_name]
            return dictionary_filtered
        except:
            return    

    def set_progress(self, context, progress):
        if not check_interface(context):
            return
        init_dict = huey_taskqueue.storage.peek_data(
            "/".join(context.getPhysicalPath())
        )
        if init_dict is EmptyData:
            data = []
        else:
            json_string = init_dict.decode('utf-8')
            data = json.loads(json_string)
        data.append({
            'task_name': self.task_name,
            'progress': progress,
            'timestamp': datetime.datetime.now().timestamp(),
            'time_elapsed': self.elapsed_time(),
        })
        #if progress == 100:
            #self.update_status(
                #context,
                #"Task Terminato!",
                #log_status_types[2]
            #)
            #self.set_end_progress(context)
        huey_taskqueue.storage.put_data(
            "/".join(context.getPhysicalPath()),
            str(json.dumps(data))
        )
        
    def set_end_progress(self, context):
        if not check_interface(context):
            return
        init_dict = huey_taskqueue.storage.peek_data(
            "/".join(context.getPhysicalPath())
        )
        if init_dict is EmptyData:
            return
        json_string = init_dict.decode('utf-8')
        data = json.loads(json_string)
        data_filtered = [task for task in data if task['task_name'] != self.task_name]      
        huey_taskqueue.storage.put_data(
            "/".join(context.getPhysicalPath()),
            str(json.dumps(data_filtered))
        )        

    def get_progress(self, context):
        try:
            if not check_interface(context):
                return            
            init_dict = huey_taskqueue.storage.peek_data(
                "/".join(context.getPhysicalPath())
            )
            if init_dict is EmptyData:
                return []
            json_string = init_dict.decode('utf-8')
            data = json.loads(json_string)
            filtered_dict = [task for task in data if task['task_name'] == self.task_name]
            if not filtered_dict:
                return []
            return max(filtered_dict, key=lambda x: x['timestamp'])
        except:
            return []      


    def clear_dict(self, dt):
        if not isinstance(dt, datetime.datetime):
            return
        try:
            self.dictionary = [value for value in self.dictionary if value['data'] >= dt]
            self.dictionary.append({
                'task_id': 'SYSTEM',
                'status_type': 'INFO',
                'data': datetime.datetime.now(),
                'message': 'I Logs precedenti al {} sono stati eliminati.'
                .format(dt.strftime("%A %d %B %Y, %H:%M:%S")),
            })       
            api.portal.set_registry_record('taskqueue2.logs', self.dictionary)
            transaction.manager.commit()
        except:
            return
