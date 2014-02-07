from django.db import connections
from django.db.models.manager import Manager


class PartitionManager(Manager):
    """
    Allows operation of partitions by passing key to get_query_set().
    """
    def get_database_from_key(self, key):
        """
        Given a key, which is defined by the partition and used to route queries, returns the
        database connection alias which the data lives on.
        """
        cluster = connections.get_cluster(self.model._shards.cluster)

        return cluster.db_for_key(key)

    def get_query_set(self, key=None):
        if not key:
            raise ValueError(
                'You must filter on %r before expanding a %s queryset.' % (
                    self.model._shards.routing_key, self.model.__name__)
            )

        db = self.get_database_from_key(key=key)
        return super(PartitionManager, self).get_query_set().using(db)

    def _wrap(func_name):
        def wrapped(self, **kwargs):
            key = kwargs.get(self.model._shards.routing_key)

            return getattr(self.get_query_set(key=key), func_name)(**kwargs)

        wrapped.__name__ = func_name
        return wrapped

    filter = _wrap('filter')
    get = _wrap('get')
    create = _wrap('create')
    get_or_create = _wrap('get_or_create')
