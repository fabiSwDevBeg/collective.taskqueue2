# -*- coding: utf-8 -*-
from collective.taskqueue2.interfaces import IAsyncContext
from plone.app.contenttypes.interfaces import IFolder
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from zope.processlifetime import IDatabaseOpenedWithRoot


periodici_folder_id = "task-periodici"
periodici_folder_title = "Task Periodici"

@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "collective.taskqueue2:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["collective.taskqueue2.upgrades"]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
   

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
        