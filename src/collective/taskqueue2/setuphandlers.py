# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from collective.taskqueue2.interfaces import IAsyncContext
from plone import api
from plone.app.contenttypes.interfaces import IFolder
from zope.interface import alsoProvides
from zope.interface import implementer
from collective.taskqueue2.huey_config import tasks_folder_id




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
    portal = api.portal.get()
    if tasks_folder_id in context:
        raise ValueError(f"A folder with the ID '{folder_id}' already exists.")

    folder = api.content.create(
        type='Folder',
        id=tasks_folder_id,
        container=portal, 
    )

    # Apply the IAsyncContext interface to the folder
    alsoProvides(folder, IAsyncContext)
    alsoProvides(folder, IFolder)

    # Reindex the object to make sure the new interface is indexed
    folder.reindexObject(idxs=['object_provides'])

    return folder      

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
        