import logging

from mongoengine import (
    Document,
    StringField, ListField,
    ReferenceField, NULLIFY)

from utils.exceptions import (ObserverNotRegisteredError,
                              ObserverAlreadyRegisteredError)
from db.observer import Observer, UserObserver


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


class Subject(Document):
    emoji = StringField(required=True, max_length=5)
    name = StringField(required=True, max_length=55, unique=True)
    uri = StringField(required=True, max_length=120, unique=True)
    default_session = StringField(required=True, max_length=55)

    observers = ListField(
        ReferenceField(UserObserver, reverse_delete_rule=NULLIFY), default=[]
    )

    def __str__(self):
        return f"{self.header} {self.uri}"

    @property
    def header(self):
        return f"{self.emoji} {self.name}"

    def subscribe(self, observer):
        if observer in self.observers:
            raise ObserverAlreadyRegisteredError(f"Observer {observer} "
                                                 f"is already registered!")
        self.observers.append(observer)
        self.save()

    def unsubscribe(self, observer):
        if observer not in self.observers:
            raise ObserverNotRegisteredError(f"Observer {observer} "
                                             f"is not registered!")
        self.observers.remove(observer)
        self.save()

    def notify(self, update_message):
        self.reload()
        official_observer = Observer.get_official_observer()
        logger.info(f'Notifying official observer {official_observer} '
                    f'for {self}')
        official_observer.notify(update_message)
        logger.info(f'Notifying observers {self.observers} for {self}')
        for observer in self.observers:
            observer.notify(update_message)
