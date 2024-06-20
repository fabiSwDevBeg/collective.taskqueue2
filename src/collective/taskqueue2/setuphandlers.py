# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api
from collective.taskqueue2.huey_config import run_buildout_periodic_tasks, huey_taskqueue
from collective.taskqueue2.interfaces import IAsyncContext
from collective.taskqueue2.huey_logger import LOG
from plone.app.contenttypes.interfaces import IFolder
from zope.interface import alsoProvides

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
    # Create a new page on the root site where you can verify the status of the periodic tasks
    portal = api.portal.get()
    riepilogo_periodici = api.content.create(
        type="Document",
        title=periodici_folder_title,
        id=periodici_folder_id,
        container=portal, 
    )
    
    alsoProvides(riepilogo_periodici, IAsyncContext)
    alsoProvides(riepilogo_periodici, IFolder)
    riepilogo_periodici.reindexObject(idxs=['object_provides'])
    
    run_buildout_periodic_tasks(huey_taskqueue, riepilogo_periodici)

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    portal = api.portal.get()
    try:
        api.content.delete(obj=portal[periodici_folder_id])
    except KeyError:
        LOG.info(f"Errore nell'eliminazione del documento: non trovata")
    for periodic_task in huey_taskqueue._registry._periodic_tasks:
        huey_taskqueue.revoke_all(periodic_task)
        