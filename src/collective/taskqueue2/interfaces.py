# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.autoform import directives

class ICollectiveTaskqueue2Layer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
    

    
class IAsyncContext(Interface):
    """ marker interface
    context implementing it will show information about async process ongoing
    """