# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from collective.taskqueue2.interfaces import IAsyncContext
from plone import api
from plone.app.contenttypes.interfaces import IFolder
from zope.interface import alsoProvides
from zope.interface import implementer
from collective.taskqueue2.huey_config import tasks_folder_id
from logging import getLogger

logger = getLogger(__name__)

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
    try:
        
        portal = api.portal.get()
        if tasks_folder_id in portal:
            folder = portal[tasks_folder_id]
        else:
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
    except Exception as e:
        logger.error(f"Errore durante l'installazione di collective.taskqueue2: {e}")

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
        