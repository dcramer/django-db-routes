from django.db.models.base import ModelBase, Model

from .manager import PartitionManager
from .options import ShardInfo, DEFAULT_NAMES


class PartitionBase(ModelBase):
    def __new__(cls, name, bases, attrs):
        # if 'Meta' not in attrs:
        #     attrs['Meta'] = type('Meta', (object,), {})
        # else:
        #     attrs['Meta'].abstract = True
        # attrs['Meta'].managed = True

        if 'objects' not in attrs:
            attrs['objects'] = PartitionManager()

        attr_shardopts = attrs.pop('Shards', None)

        new_cls = super(PartitionBase, cls).__new__(cls, name, bases, attrs)

        if not attr_shardopts:
            shardopts = getattr(new_cls, 'Shards', None)
        else:
            shardopts = attr_shardopts
        base_shardopts = getattr(new_cls, '_shards', None)

        new_cls.add_to_class('_shards', ShardInfo(shardopts))

        if base_shardopts:
            for k in DEFAULT_NAMES:
                if not hasattr(new_cls._shards, k):
                    setattr(new_cls._shards, k, getattr(base_shardopts, k, None))

        return new_cls


class PartitionModel(Model):
    __metaclass__ = PartitionBase

    class Meta:
        abstract = True
