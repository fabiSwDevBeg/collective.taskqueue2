# -*- coding: utf-8 -*-
from collective.taskqueue2 import _
from collective.taskqueue2.interfaces import IAsyncContext
from collective.taskqueue2.huey_events import log_status_types
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getAdapter


TERMINATI = ['FAILURE', 'SUCCESS', 'PENDING']


class AsyncManager(ViewletBase):

    def render(self):
        self.anyFinished = False
        self.anyRunning = False
        self.manager = getAdapter(self.context, IAsyncContext)
        keys = self.manager.getProcessKeys()
        for k in keys:
            progress, statuses = self.manager.getProcessInfo(k)
            if len(progress) > 0:
                self.anyRunning = True
            if len(statuses) > 0:
                for status in statuses:
                    if status['status_type'] in log_status_types[:2]:
                        self.anyFinished = True
        return self.index()
