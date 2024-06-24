from ..huey_config import huey_taskqueue
from ..huey_events import Progress
from Products.Five import BrowserView

import json


class TaskQueue(BrowserView):
    def stats(self):
        """Return taskqueue stats"""
        r = dict(
            pending=len(huey_taskqueue.pending()),
            scheduled=len(huey_taskqueue.scheduled()),
        )
        progress_manager = Progress("Plone", "Prova")
        progress_manager.set_progress(self.context, 80)
        return json.dumps(r)
