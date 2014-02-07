from __future__ import absolute_import

from dbroutes.models import PartitionModel
from django.db import models


class DummyModel(PartitionModel):
    group_id = models.IntegerField()

    class Meta:
        db_table = 'dummy'

    class Shards:
        cluster = 'cluster'
        routing_key = 'group_id'
