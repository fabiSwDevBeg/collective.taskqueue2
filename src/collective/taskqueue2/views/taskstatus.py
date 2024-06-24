# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from ..huey_events import Progress
import json


class ITaskstatus(Interface):
    """ Marker Interface for ITaskstatus"""


@implementer(ITaskstatus)
class Taskstatus(BrowserView):
    def __call__(self):
        taskname = self.request.get('taskname')
        if taskname:
            progress_manager = Progress(None, taskname)
            obj = progress_manager.get_progress(self.context)
        else:
            progress_manager = Progress(None, "")
            obj = progress_manager.get_all_progress(self.context)            
        self.request.response.setHeader('Content-Type', 'application/json')
        #self.request.response.setHeader('Content-Disposition', 'attachment; filename="data.json"')
        return json.dumps(obj)
