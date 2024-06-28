from collective.taskqueue2.huey_config import huey_taskqueue
from persistent.dict import PersistentDict
from collective.taskqueue2.interfaces import IAsyncContext
from huey.constants import EmptyData
from plone import api
from zope.component.hooks import setSite
from zope.component.hooks import getSite
from Acquisition import ImplicitAcquisitionWrapper
#from zope.interface import providedBy

from Testing.makerequest import makerequest
from zope.annotation import IAnnotations

from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
from OFS.Application import Application
#from OFS.CopySupport
#from plone.api.content    
import datetime
import functools
import json
import transaction
import Zope2
import traceback


log_status_types = ['FAILURE', 'SUCCESS', 'PENDING']
from logging import getLogger

logger = getLogger(__name__)
REG_KEY = 'taskqueue2.logs'

def check_interface(obj):
    return IAsyncContext.providedBy(obj)

# Stolen from collective.celery
def getApp(*args, **kwargs):
    if Zope2.bobo_application is None:
        orig_argv = sys.argv
        sys.argv = ['']
        res = Zope2.app(*args, **kwargs)
        sys.argv = orig_argv
        return res
    # should set bobo_application
    # man, freaking zope2 is weird
    return Zope2.bobo_application(*args, **kwargs)


def progress_manager(func, context=None):
    """
    @progress_decorator delega il compito di richiamare
    set_status, set_progress e set_end_progress
    alla funzione decorata

    @progress_decorator(context)gestisce autonomamente gli stati iniziali e delega
    solo il set_progress
    alla funzione decorata
    
    La funzione decorata può essere richiamata:
    - Da bin/instance inserendo un entry_point in setup.py nel formato:
      [zopectl.command]
      nome_task = path.to.class:function_name
    
      per poi essere richiamata da un crontab nel buildout.cfg come:
      [buildout]
      parts += 
          routine_name
      
      [routine_name]
      recipe = z3c.recipe.usercrontab
      times = * * * * *
      command = ${buildout:directory}/bin/instance nome_task site_name
      comment = 
      
      
      In questo caso la funzione viene chiamata con
      function_name(<Application at >, ['-c', 'routine_name', 'site_name'])
      
    - Da codice .py:
      from path.to.class import function_name
      
      function_name('site_name')
      
    """
    @huey_taskqueue.task(immediate=False)  
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        task_name = func.__name__
        try:
            t = transaction.manager
            t.begin()
            
            app = makerequest(getApp())
            if not isinstance(args[0], Application):
                plone_site = app.restrictedTraverse("/"+args[0], None)
            else:
                nome_app = args[1][2] if len(args) > 1 and len(args[1]) > 2 else None
                plone_site = app[nome_app] if app and nome_app else None
    
            #server_name = 'localhost'
            #protocol = 'https'
            #request = app.REQUEST
            #request.other['SERVER_URL'] = '{}://{}'.format(protocol, server_name)
            #request.setServerURL(protocol, server_name)
            #request.other['VirtualRootPhysicalPath'] = plone_site.getPhysicalPath()

            progress_manager = Progress(plone_site, task_name)
            
            if not progress_manager.userid:
                api.env.adopt_user(username="admin")
                user = app.acl_users.getUserById('admin')
                newSecurityManager(None, user)
                
            if context:
                progress_manager.set_status(context,
                                            "Task Iniziato!",
                                            log_status_types[2]
                                            )
            func(progress_manager, *args, **kwargs)
            if context:
                progress_manager.set_end_progress(context)
                progress_manager.set_status(context,
                                            "Task Terminato!",
                                            log_status_types[0]
                                            )
            t.commit()
            return 
        except Exception as e:
            t.abort()
            tb = traceback.format_exc()
            if context:
                progress_manager.set_end_progress(context)
                progress_manager.set_status(context,
                                            f"Task Terminato! {e}",
                                            log_status_types[1]
                                            )                       
            logger.error(f"Errore nella creazione del contesto per {task_name}: {str(e)} \n {tb}")
            return
        finally:
            noSecurityManager()
            setSite(None)
        
    return wrapper

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
        unique_task_names = list(set(task['task_id'] for task in data))
        return unique_task_names
    except:
        return []  

class Progress:
    """
    Classe che gestisce il logging dei task asincroni
    Puo essere inizializzata automaticamente tramite i due decoratori
    che forniscono progress_manager alla funzione decorata
    """
    def __init__(self, plone, task_name):
        if isinstance(plone, ImplicitAcquisitionWrapper):
            setSite(plone)
            from plone import api
        self.start_time = datetime.datetime.now()
        self.task_name = task_name
        self.userid = api.user.get_current().getId()
        self.portal = api.portal.get()
        
    

    def elapsed_time(self):
        current_time = datetime.datetime.now()
        elapsed = current_time - self.start_time
        return elapsed.total_seconds()   

    def set_status(self, context, message, status_type):
        """
        
        """
        try:
            if not check_interface(context):
                return
            annotation = IAnnotations(context)
            if self.task_name not in annotation:
                annotation[self.task_name] = []
            #dictionary = api.portal.get_registry_record(REG_KEY)
            new_entry = {
                #'task_id': self.task_name,
                'context_path': "/".join(context.getPhysicalPath()),
                'status_type': status_type,
                'data': datetime.datetime.now(),
                'message': message,
                'time_elapsed': self.elapsed_time(),
                'user': self.userid if self.userid else "SYSTEM",
            }
            #dictionary.append(new_entry)
            annotation[self.task_name].insert(0, new_entry)
            #dictionary.insert(0, new_entry)
            #api.portal.set_registry_record(REG_KEY, dictionary)
        except Exception as e:
            tb = traceback.format_exc()
            logger.error(f"Errore nel set dello stato per {self.task_name} "
                         f"su {'/'.join(context.getPhysicalPath())}: {str(e)} \n {tb} ")
            return
        finally:
            transaction.manager.commit()
            transaction.commit()
        
    def get_status(self, context):
        try:
            if not check_interface(context):
                return
            annotation = IAnnotations(context)
            if self.task_name not in annotation:
                return
            return annotation[self.task_name]
            #dictionary = api.portal.get_registry_record(REG_KEY)
            #if not dictionary:
                #return
            #dictionary_filtered = [entry for entry in dictionary if entry['task_id'] == self.task_name]
            #return dictionary_filtered
        except Exception as e:
            logger.error(f"Errore nel get dello stato per {self.task_name} "
                         f"su {'/'.join(context.getPhysicalPath())}: {str(e)}")            
            return    

    def set_progress(self, context, progress):
        try:
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
                'task_id': self.task_name,
                'progress': progress,
                'timestart': self.start_time.timestamp(),
                'timestamp': datetime.datetime.now().timestamp(),
                'userid': self.userid if self.userid else "SYSTEM",
                'time_elapsed': self.elapsed_time(),
            })
            huey_taskqueue.storage.put_data(
                "/".join(context.getPhysicalPath()),
                str(json.dumps(data))
            )
        except Exception as e:
            logger.error(f"Errore nel set del progresso per {self.task_name} "
                         f"su {'/'.join(context.getPhysicalPath())}: {str(e)}")
            return
        
    def set_end_progress(self, context):
        try:
            if not check_interface(context):
                return
            init_dict = huey_taskqueue.storage.peek_data(
                "/".join(context.getPhysicalPath())
            )
            if init_dict is EmptyData:
                return
            json_string = init_dict.decode('utf-8')
            data = json.loads(json_string)
            data_filtered = [task for task in data if task['task_id'] != self.task_name]      
            huey_taskqueue.storage.put_data(
                "/".join(context.getPhysicalPath()),
                str(json.dumps(data_filtered))
            )
        except Exception as e:
            logger.error(f"Errore nel set finale del progresso per {self.task_name} "
                         f"su {'/'.join(context.getPhysicalPath())}: {str(e)}")
            return            

    def get_progress(self, context):
        try:
            if not check_interface(context):
                return            
            init_dict = huey_taskqueue.storage.peek_data(
                "/".join(context.getPhysicalPath())
            )
            if init_dict is EmptyData:
                return {}
            json_string = init_dict.decode('utf-8')
            data = json.loads(json_string)
            filtered_dict = [task for task in data if task['task_id'] == self.task_name]
            if not filtered_dict:
                return {}
            return max(filtered_dict, key=lambda x: x['timestamp'])
        except Exception as e:
            logger.error(f"Errore nel get del progresso per {self.task_name} "
                         f"su {'/'.join(context.getPhysicalPath())}: {str(e)}")
            return {}      


    #def clear_dict(self, dt):
        #if not isinstance(dt, datetime.datetime):
            #return
        #try:
            #dictionary = [value for value in dictionary if value['data'] >= dt]
            #dictionary.append({
                #'task_id': 'SYSTEM',
                #'status_type': 'INFO',
                #'data': datetime.datetime.now(),
                #'message': 'I Logs precedenti al {} sono stati eliminati.'
                #.format(dt.strftime("%A %d %B %Y, %H:%M:%S")),
            #})       
            #api.portal.set_registry_record(REG_KEY, dictionary)
            #transaction.manager.commit()
        #except:
            #logger.error(f"Errore nel get del progresso per {self.task_name} "
                         #f"su {'/'.join(context.getPhysicalPath())}: {str(e)}")            
            #return
