# -*- coding: utf-8 -*-
from collective.taskqueue2 import _
from collective.taskqueue2.interfaces import ILogsSchema
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from datetime import date
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform import directives
from plone.autoform import directives as form
from plone.z3cform import layout
from z3c.form.interfaces import IDisplayForm
from zope import schema
from zope.interface import Interface
from zope.interface import implementer
from zope.schema.interfaces import IList


class ILogsList(IList):
    pass


@implementer(ILogsList)
class LogsList(schema.List):
    pass


class ITaskQueue2ControlPanel(Interface):
    directives.widget(logs=DataGridFieldFactory)
    logs = schema.List(
        title=_(u'Elenco dei Logs'),
        description=_("Elenco dei log per task asincroni o crontab,"+\
        " generati dal primo avvio dell'istanza"),
        value_type=DictRow(title=u'LOG', schema=ILogsSchema),
        default=[],
        required=True,
    )
    
    

class TaskQueue2ControlPanelForm(RegistryEditForm):
    schema = ITaskQueue2ControlPanel
    schema_prefix = "taskqueue2"
    label = u'TaskQueue2 Logs'


#TaskQueue2ControlPanelView = layout.wrap_form(
    #TaskQueue2ControlPanelForm, ControlPanelFormWrapper)

class TaskQueue2ControlPanel(ControlPanelFormWrapper):
    form = TaskQueue2ControlPanelForm