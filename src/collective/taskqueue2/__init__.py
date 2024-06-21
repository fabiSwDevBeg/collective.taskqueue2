# -*- coding: utf-8 -*-
"""Init and utils."""
from collective.taskqueue2.huey_config import huey_taskqueue
from collective.taskqueue2.setuphandlers import periodici_folder_id
from plone import api
from Testing.makerequest import makerequest
from zope.component import getGlobalSiteManager
from zope.component.hooks import setSite
from zope.i18nmessageid import MessageFactory

import transaction
import Zope2


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

        