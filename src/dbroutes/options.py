DEFAULT_NAMES = ('routing_key', 'sequence', 'cluster')


class ShardInfo(object):
    def __init__(self, options):
        self.options = options
        self.model = None
        self.name = None

    def __repr__(self):
        return u'<%s: model=%s, options=%s>' % (
            self.__class__.__name__, self.model, self.options)

    def contribute_to_class(self, cls, name):
        self.name = name
        self.model = cls
        setattr(cls, name, self)

        opts = self.options

        if opts:
            for k in (k for k in DEFAULT_NAMES if hasattr(opts, k)):
                setattr(self, k, getattr(opts, k))

        if not hasattr(self, 'sequence'):
            self.sequence = cls._meta.db_table
