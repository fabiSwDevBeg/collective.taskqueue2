# Basic Adapter
# use your own context
from collective.taskqueue2 import KEY
from collective.taskqueue2.interfaces import IAsyncContext
from collective.taskqueue2.viewlets.async_manager import TERMINATI
from persistent.dict import PersistentDict
from plone.app.contenttypes.interfaces import IFolder
from zope.annotation import IAnnotations
from zope.component import adapter
from zope.interface import implementer


def getHueyProcessStatus(task_id):
    from collective.taskqueue2.huey_config import huey_taskqueue
    try:
        result = huey_taskqueue.result(task_id)
        return TERMINATI[1] if result else TERMINATI[2]
    except:
        return TERMINATI[0]
    


@adapter(IFolder)
@implementer(IAsyncContext)
class BasicAsyncAwareContext():
    """Implement your store/get procedure  on the context """

    def __init__(self, context):
        self.context = context

    def getProcessKeys(self):
        """return list of celery id"""
        ann =  IAnnotations(self.context).get(KEY, {})

        return list(ann.keys())

    def getProcessInfo(self, id):
        """ return status of process by id"""
        ann =  IAnnotations(self.context).get(KEY)
        info = ann.get(id, None)
        process = getHueyProcessStatus(id)

        info.update(status=process)

        return info

    def setProcess(self, id, **kwargs):
        """ store celery id on the context annotation"""
        ann =  IAnnotations(self.context)

        if KEY not in ann:
            ann[KEY] = PersistentDict()

        info = ann[KEY]
        info[id] = dict(kwargs)

    def deleteProcess(self, idList, **kwargs):
        """ delete celery id on the context annotation"""
        ann =  IAnnotations(self.context)
        for k in idList:
            del ann[KEY][k]
