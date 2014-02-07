from django.conf import settings


def install(settings=settings):
    from dbroutes.utils import PartitionConnectionHandler
    from django import db

    handler = PartitionConnectionHandler(settings.DATABASES)

    db.connections.__class__ = type(handler)
    db.connections.__dict__ = vars(handler)
