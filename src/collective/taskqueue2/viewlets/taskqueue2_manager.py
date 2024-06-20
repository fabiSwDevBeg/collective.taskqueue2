from collective.taskqueue2.huey_config import huey_taskqueue
from plone import api
from csi.asyncmanager.interfaces import IAsyncContext
import time



def find_async_folders():
    catalog = api.portal.get_tool(name='portal_catalog')
    folders = catalog(portal_type='Folder')
    for brain in folders:
        folder = brain.getObject()
        if IAsyncContext.providedBy(folder):
            return folder
    return None


def update_progress(context, progress):
    print(f'Task {context}: Progress {progress}%')
    api.content.rename(obj=find_async_folders(), new_id="ProvaFolder"+str(progress))
    
    
    
@huey_taskqueue.task()
def do_work(num_operations):
    context = args.get("context")
    num_operations = args.get("num_operations")
    for i in range(1, num_operations + 1):
        # Simula un'operazione che richiede tempo
        time.sleep(1)
        progress = (i / num_operations) * 100
        update_progress(context, progress)

    return 'Task completed!'
