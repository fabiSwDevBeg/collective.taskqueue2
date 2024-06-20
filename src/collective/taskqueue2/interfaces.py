# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import Interface

class ICollectiveTaskqueue2Layer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
    

    
class IAsyncContext(Interface):
    """ marker interface
    context implementing it will show information about async process ongoing
    """

    def getProcessKeys(self):
        """return list of celery id"""

    def getProcess(self, id):
        """ return status of process by id"""

    def setProcess(self, id, **kwargs):
        """ store celery id"""

    def deleteProcess(self, idList, **kwargs):
        """ delete celery id"""
