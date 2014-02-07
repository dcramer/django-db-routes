django-db-routes
================

The gist of the package is that we create a custom connection handler (``django.db.connections``) which
will map virtual shards to real databases. Databases end up being ``<clustername>.shard<number>``.

Partitioned Models
------------------


::

        DATABASE_CLUSTERS = {
            'mycluster': {
                'NAME': 'mycluster',
                'SHARDS': 1024,
                'HOSTS': [
                    {'HOST': '192.168.0.100'},
                    {'HOST': '192.168.0.101'},
                    {'HOST': '192.168.0.102'},
                    {'HOST': '192.168.0.103'},
                ],
            },
        }


Extend the PartitionModel class when creating your models:

::

    from django.db import models
    from dbroutes.models import PartitionModel

    class MyModel(PartitionModel):
        user_id = models.PositiveIntegerField()

        class Shards:
            routing_key = 'user_id'
            cluster = 'mycluster'

Query the nodes passing in your ``key``:

::

    objects = MyModel.objects.filter(user_id=1)
