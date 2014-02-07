from django.conf import settings
from django.db.utils import ConnectionHandler, load_backend


class Cluster(object):
    def __init__(self, name, hosts, shards):
        self.name = name
        self.shards = shards
        self.hosts = hosts

    def db_for_key(self, key):
        return '%s.shard%d' % (self.name, key % self.shards)


class PartitionConnectionHandler(ConnectionHandler):
    def __init__(self, databases):
        super(PartitionConnectionHandler, self).__init__(None)
        self.shards = {}
        self.clusters = {}

        for name, options in databases.iteritems():
            if options.get('SHARDS'):
                self.add_cluster(
                    name=name,
                    settings_dict=options,
                )
            else:
                self.databases[name] = options

    def __getitem__(self, alias):
        # TODO(dcramer): ideally we could reuse database connections and just
        # enforce no cross-shard transactions
        # TODO(dcramer): we need to set a limit of the maximum number of open
        # connections
        if hasattr(self._connections, alias):
            return getattr(self._connections, alias)

        settings_dict = self.databases[alias]
        conn = self.load_connection(alias, settings_dict)
        setattr(self._connections, alias, conn)
        return conn

    def add_cluster(self, name, settings_dict):
        assert name not in self.databases

        hosts = settings_dict.pop('HOSTS')
        shards = settings_dict.pop('SHARDS')

        num_hosts = len(hosts)

        phys_hosts = []
        for n, host in enumerate(hosts):
            host_name = '%s.host%d' % (name, n)
            for key, value in settings_dict.iteritems():
                host.setdefault(key, value)
            self.databases[host_name] = host
            phys_hosts.append(host_name)

        for n in xrange(1, shards + 1):
            host_name = phys_hosts[n % num_hosts]
            self.databases['%s.shard%d' % (name, n)] = self.databases[host_name]

        print self.databases

        self.clusters[name] = Cluster(name, phys_hosts, shards)

    def get_cluster(self, name):
        return self.clusters[name]

    def ensure_defaults(self, settings_dict):
        """
        Puts the defaults into the settings dictionary for a given connection
        where no settings is provided.
        """
        settings_dict.setdefault('ENGINE', 'dbroutes.backend')
        settings_dict.setdefault('SCHEMA', 'public')
        settings_dict.setdefault('OPTIONS', {})
        settings_dict.setdefault('TIME_ZONE', 'UTC' if settings.USE_TZ else settings.TIME_ZONE)
        for setting in ['NAME', 'USER', 'PASSWORD', 'HOST', 'PORT']:
            settings_dict.setdefault(setting, '')
        for setting in ['TEST_CHARSET', 'TEST_COLLATION', 'TEST_NAME', 'TEST_MIRROR']:
            settings_dict.setdefault(setting, None)

    def load_connection(self, alias, settings_dict):
        self.ensure_defaults(settings_dict)
        backend = load_backend(settings_dict['ENGINE'])
        conn = backend.DatabaseWrapper(settings_dict, alias)
        return conn
