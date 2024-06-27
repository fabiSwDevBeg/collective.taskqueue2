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


class ILogsSchema(Interface):
    """ marker interface
    context implementing it will show information about async process ongoing
    """
    
    task_id = schema.TextLine(
        title=u'ID Task',
        description=u'Codice Identificativo del Task',
    )
    directives.mode(task_id='display')
    
    context_path = schema.TextLine(
        title=u'Context Path',
        description=u'Path del Contesto su cui è stata eseguita l\' azione',
    )
    directives.mode(context_path='display')
    
    status_type = schema.TextLine(
        title=u'Tipo di Log',
        description=u'Categoria del Log',
    )
    directives.mode(status_type='display')
    
    data = schema.Datetime(
        title=u'Data Esecuzione',
        description=u"Data e Ora dell'esecuzione dell'azione",
    )
    directives.mode(data='display')
    
    message = schema.Text(
        title=u'Messaggio',
        description=u"Descrizione dell'operazione",
    )
    directives.mode(message='display')
    
    time_elapsed = schema.Float(
        title=u'Tempo Trascorso',
        description=u"Tempo trascorso dall'inizio dell'operazione",
    )
    directives.mode(time_elapsed='display')
    
    user = schema.TextLine(
        title=u'Utente',
        description=u"Nome Utente",
    )
    directives.mode(user='display')
    