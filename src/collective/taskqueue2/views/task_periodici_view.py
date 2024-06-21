# -*- coding: utf-8 -*-

# from collective.taskqueue2 import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from zope.annotation import IAnnotations


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ITaskPeriodiciView(Interface):
    """ Marker Interface for ITaskPeriodiciView"""


@implementer(ITaskPeriodiciView)
class TaskPeriodiciView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('task_periodici_view.pt')

    def __call__(self):
        annotations = IAnnotations(self.context)
        self.annotations_data = {key: value for key, value in annotations.items()}
        return self.index()
