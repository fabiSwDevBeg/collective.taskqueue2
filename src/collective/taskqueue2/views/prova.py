# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from ..huey_events import Progress
from ..huey_events import get_all_processes
from csi.asyncmanager.tasks import do_work2
import json
from plone import api


class ITaskProva(Interface):
    """ Marker Interface for ITaskstatus"""


@implementer(ITaskProva)
class Taskprova(BrowserView):
    def __call__(self):
        obj = do_work2('Plone')
        return "EWWEE"
    
    
    
    
