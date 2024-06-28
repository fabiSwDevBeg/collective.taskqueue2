# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.interface import Attribute
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.autoform import directives

class ICollectiveTaskqueue2Layer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
    

    
class IAsyncContext(Interface):
    """ marker interface
    context implementing it will show information about async process ongoing
    """

class IProgress(Interface):
    """
    Interfaccia per la classe Progress che gestisce il logging dei task asincroni
    """

    start_time = Attribute("L'oggetto datetime corrispondente "
                           "all'orario di inizio del task")
    task_name = Attribute("Il nome del task")
    userid = Attribute("L'ID dell'utente")
    portal = Attribute("L'istanza del portale")

    def elapsed_time():
        """Ritorna il tempo trascorso dall'istanziazione della classe in secondi"""

    def set_status(context, message, status_type, **extra_metadata):
        """
        Imposta uno stato sulla IAnnotations relativa al context
        sulla chiave self.task_name
            'status_type': status_type,
            'data': datetime di invio,
            'message': message,
            'time_elapsed': tempo di esecuzione in secondi
                dall'istanziazione della classe,
            'user': SYSTEM per gli utenti anonimi oppure l'username,
            'request': oggetto richiesta del context
            'extra_metadata': argomenti passati a extra_metadata,
        """

    def get_status(context):
        """
        Ritorna una lista di dizionari contenente tutto lo storico degli stati
        per self.task_name, ordinato cronologicamente in modo tale
        che l'elemento alla posizione [0] sia il più recente.
        """

    def set_progress(context, progress, **extra_metadata):
        """
        Imposta un progresso sul RedisStorage, come chiave il path del context
        Il progresso non è persistito, al termine dell'esecuzione viene chiamato
        set_end_progress che elimina le chiavi relative al progresso in corso
        N.B. tutti i parametri della funzione eccetto context devono essere Pickle-abili
            'task_id': il task_name con la quale è stata instanziata la classe,
            'progress': progress,
            'timestart': timestamp di istanziazione della classe,
            'timestamp': timestamp di esecuzione,
            'time_elapsed': tempo di esecuzione in secondi dall'istanziazione della classe,
            'userid': SYSTEM per gli utenti anonimi oppure l'username,
            'extra_metadata': argomenti passati a extra_metadata,
        """

    def set_end_progress(context):
        """
        Rimuove il progresso sul RedisStorage, come chiave il path del context
        eliminando i dizionari che hanno task_id == self.task_name
        """

    def get_progress(context):
        """
        Ritorna il dizionario più recente relativo al progresso
        con task_id == self.task_name
        """

    def clear_before_dt(context, dt):
        """
        Rimuove tutti gli stati presenti sui contesti
        che implementano IAsyncContext precedenti al datetime.datetime dt
        passato alla funzione
        """