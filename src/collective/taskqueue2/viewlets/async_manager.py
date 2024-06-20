# -*- coding: utf-8 -*-
from csi.asyncmanager import _
from csi.asyncmanager.interfaces import IAsyncContext
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getAdapter


TERMINATI = ['FAILURE', 'SUCCESS', 'PENDING']

class Celerystatus(BrowserView):

    def getProcesses(self):
        keys = self.manager.getProcessKeys()
        return keys

    def updateInfo(self, inactive=0):

        for k in self.getProcesses():
            info = self.manager.getProcessInfo(k)
            self.info.append((k, info))

    def __call__(self):
        self.manager = getAdapter(self.context, IAsyncContext)
        self.info = []
        self.updateInfo()
        self.msg = _(str(self.info))
        return self.index()



class DeleteList(BrowserView):

    def __call__(self):
        self.manager = getAdapter(self.context, IAsyncContext)
        keysToDel = []
        keys = self.manager.getProcessKeys()
        for k in keys:
            info = self.manager.getProcessInfo(k)
            if (info['status'].status in TERMINATI):
                keysToDel.append(k)
        if(keysToDel):
            self.manager.deleteProcess(keysToDel)
            self.status = _(u"Tasks deleted.")
            IStatusMessage(self.request).addStatusMessage(self.status, type="info")
        return self.request.response.redirect(self.context.absolute_url())


class AsyncManager(ViewletBase):

    def render(self):
        self.anyFinished = False
        self.anyRunning = False
        self.manager = getAdapter(self.context, IAsyncContext)
        keys = self.manager.getProcessKeys()
        for k in keys:
            info = self.manager.getProcessInfo(k)
            if (info['status'].status in TERMINATI):
                self.anyFinished = True
            else:
                self.anyRunning = True
        return self.index()
