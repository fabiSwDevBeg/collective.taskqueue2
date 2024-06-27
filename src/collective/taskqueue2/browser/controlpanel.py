# -*- coding: utf-8 -*-
from collective.taskqueue2 import _
from collective.taskqueue2.interfaces import ILogsSchema
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from datetime import date
from z3c.form import button
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform import directives
from plone.autoform import directives as form
from plone.z3cform import layout
from z3c.form.interfaces import IDisplayForm
from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IList


class ILogsList(IList):
    pass


@implementer(ILogsList)
class LogsList(schema.List):
    pass


class ITaskQueue2ControlPanel(Interface):
    days_to_keep = schema.Int(
        title=_(u'Giorni di Logs da mantenere'),
        description=_("Giornalmente i log più vecchi di questo numero di giorni"
                      " vengono eliminati."),
        min=1,
        max=64,
        default=10,
        required=True, 
    )
    logs = schema.List(
        title=_(u'Elenco dei Logs'),
        description=_("Elenco dei log per task asincroni o crontab,"
                      " generati dal primo avvio dell'istanza"),
        value_type=DictRow(title=u'LOG', schema=ILogsSchema),
        default=[],
        #readonly=True, 
    )
    directives.widget(
        'logs',
        DataGridFieldFactory,
        allow_insert=False,
        allow_delete=False,
        allow_reorder=False,
        auto_append=False,
    )        
    
    

class TaskQueue2ControlPanelForm(RegistryEditForm):
    schema = ITaskQueue2ControlPanel
    schema_prefix = "taskqueue2"
    label = u'TaskQueue2 Logs'
    
    def handleSave(self, action):
        return "Ciao"

#TaskQueue2ControlPanelView = layout.wrap_form(
    #TaskQueue2ControlPanelForm, ControlPanelFormWrapper)

class TaskQueue2ControlPanel(ControlPanelFormWrapper):
    form = TaskQueue2ControlPanelForm