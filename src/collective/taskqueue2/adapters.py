# Basic Adapter
# use your own context
from collective.taskqueue2.huey_progress_manager import Progress
from collective.taskqueue2.huey_progress_manager import get_all_processes
from collective.taskqueue2.interfaces import IAsyncContext
from plone import api
from plone.app.contenttypes.interfaces import IFolder
from zope.component import adapter
from zope.interface import implementer
from plone.indexer.decorator import indexer


@adapter(IFolder)
@implementer(IAsyncContext)
class BasicAsyncAwareContext():
    """Implement your store/get procedure  on the context """

    def __init__(self, context):
        self.context = context
        self.app = api.portal.get()
        self.progress_class = None
        
    def generateProgressClassIfNeeded(self, id_task):
        if self.progress_class is None or self.progress_class.task_name != id_task:
            self.progress_class = Progress(self.app, id_task)    

    def getProcessKeys(self):
        """return list of tasks ids"""
        
        return get_all_processes(self.context)

    def getProcessInfo(self, id_task):
        """ return status of process by id"""
        
        self.generateProgressClassIfNeeded(id_task)
        return (
            self.progress_class.get_progress(self.context),
            self.progress_class.get_status(self.context)
        )

    def setProcess(self, id_task, progress):
        """ store progress on Redis"""
        
        self.generateProgressClassIfNeeded(id_task)
        self.progress_class.set_progress(self.context, progress)

    def deleteProcess(self, id_task, **kwargs):
        """ delete process statuses from Redis"""
        
        self.generateProgressClassIfNeeded(id_task)
        self.progress_class.set_end_progress(self.context)
