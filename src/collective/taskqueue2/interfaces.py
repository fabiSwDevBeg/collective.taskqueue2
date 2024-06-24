# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveTaskqueue2Layer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
    

    
class IAsyncContext(Interface):
    """ marker interface
    context implementing it will show information about async process ongoing
    """


class ILogsSchema(Interface):
    """ marker interface
    context implementing it will show information about async process ongoing
    """
    
    task_id = schema.TextLine(
        title=u'ID Task',
        description=u'Codice Identificativo del Task',
        required=True,
        default="", 
        readonly=True,
    )
    
    context_path = schema.TextLine(
        title=u'Context Path',
        description=u'Path del Contesto su cui è stata eseguita l\' azione',
        required=True,
        default="", 
        readonly=True,
    )    
    
    status_type = schema.TextLine(
        title=u'Tipo di Log',
        description=u'Categoria del Log',
        required=True,
        default="", 
        readonly=True,
    )
    
    data = schema.Datetime(
        title=u'Data Esecuzione',
        description=u"Data e Ora dell'esecuzione dell'azione",
        required=True,
        readonly=True,
    )
    
    message = schema.TextLine(
        title=u'Messaggio',
        description=u"Descrizione dell'operazione",
        required=True,
        default="",
        readonly=True,
    )
    
    time_elapsed = schema.Int(
        title=u'Tempo Trascorso',
        description=u"Tempo trascorso dall'inizio dell'operazione",
        required=True,
        default=0,
        readonly=True,        
    )