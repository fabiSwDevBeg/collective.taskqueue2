# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory
import transaction
import Zope2
from Testing.makerequest import makerequest
from zope.component.hooks import setSite
from zope.interface import implementer
from plone import api
from collective.taskqueue2.setuphandlers import periodici_folder_id
from collective.taskqueue2.huey_config import run_buildout_periodic_tasks, huey_taskqueue
from zope.component import getGlobalSiteManager
from collective.taskqueue2.interfaces import ICollectiveTaskqueue2Layer
from zope.processlifetime import IProcessStarting


KEY = "collective.taskqueue2"

_ = MessageFactory(KEY)

def generateContext():
     
    def inner(func):
        def wrapper(*args, **kwargs):
            #path = "/".join(api.portal.get().getPhysicalPath())
        #username = api.user.get_current().getId()
            path = "/Plone"
            username = "admin"
            t = transaction.manager
            t.begin()
            app = Zope2.app()
        
            site = app.restrictedTraverse(path, None)
            if site is None:
                raise ValueError(f"No site {path}")
            setSite(site)
            site = makerequest(site)
        
            result = None
            with api.env.adopt_user(username=username):
                try:
                    try:
                        context = site.restrictedTraverse(path)
                        if context is None:
                            raise ValueError(f"Unknown context {path}")
                        context = makerequest(context)
                        result = func(context)
        
                        t.commit()
                    except:
                        t.abort()
                        raise
                finally:
                    setSite(None)
                    app._p_jar.close()
            return result
        return wrapper  
    return inner


_menuItemsRegistered = set()

@implementer(IProcessStarting)
def beforeSiteTraverse(event):
    portal = api.portal.get()
    folder = portal[periodici_folder_id]
    huey_tasks = run_buildout_periodic_tasks(huey_taskqueue, folder)
        