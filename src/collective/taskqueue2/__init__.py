# -*- coding: utf-8 -*-
"""Init and utils."""
from collective.taskqueue2.huey_config import huey_taskqueue
from plone import api
from Testing.makerequest import makerequest
from zope.component import getGlobalSiteManager
from zope.component.hooks import setSite
from zope.i18nmessageid import MessageFactory

import transaction
import Zope2


KEY = "collective.taskqueue2"

_ = MessageFactory(KEY)
