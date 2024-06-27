# -*- coding: utf-8 -*-
from collective.taskqueue2 import _
from collective.taskqueue2.interfaces import IAsyncContext
from collective.taskqueue2.huey_events import log_status_types
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getAdapter
from datetime import datetime


TERMINATI = ['FAILURE', 'SUCCESS', 'PENDING']


class AsyncManager(ViewletBase):

    def render(self):
        self.anyFinished = False
        self.anyRunning = False
        self.manager = getAdapter(self.context, IAsyncContext)
        keys = self.manager.getProcessKeys()
        for k in keys:
            progress, statuses = self.manager.getProcessInfo(k)
            if progress and len(progress) > 0:
                self.anyRunning = True
            if statuses and len(statuses) > 0:
                for status in statuses:
                    if status['status_type'] in log_status_types[:2]:
                        self.anyFinished = True
        return self.index()



    
class TaskStatus(BrowserView):

    def getProcesses(self):
        keys = self.manager.getProcessKeys()
        return keys

    def updateInfo(self, inactive=0):

        for k in self.getProcesses():
            progress, status = self.manager.getProcessInfo(k)
            if status:
                progress['status'] = status[0]['status_type']
                progress['context_path'] = status[0]['context_path']
            self.info.append((k, progress))

    def timestamp_to_string(self, timestamp):
        if not isinstance(timestamp, (int, float)):
            return         
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%d %B %Y, %H:%M:%S")
    
    def __call__(self):
        self.manager = getAdapter(self.context, IAsyncContext)
        self.info = []
        self.updateInfo()
        self.msg = _(str(self.info))
        return self.index()
    
    
        


class TasksProcessed(BrowserView):

    def getProcesses(self):
        keys = self.manager.getProcessKeys()
        return keys

    def updateInfo(self, inactive=0):

        for k in self.getProcesses():
            progress, status = self.manager.getProcessInfo(k)
            if status:
                progress['status'] = status[0]['status_type']
                progress['context_path'] = status[0]['context_path']
            self.info.append((k, progress))

    def timestamp_to_string(self, timestamp):
        if not isinstance(timestamp, (int, float)):
            return         
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%d %B %Y, %H:%M:%S")

    def __call__(self):
        self.manager = getAdapter(self.context, IAsyncContext)
        self.info = []
        self.updateInfo()
        self.msg = _(str(self.info))
        return self.index()

    
    
        

