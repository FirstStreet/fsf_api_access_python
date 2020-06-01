from os import environ


def connection_params():
    pg = {
        'PGUSER': 'user',
        'PGHOST': 'host',
        'PGPORT': 'port',
        'PGDATABASE': 'database',
        'PGPASSWORD': 'password',
        'PGPASSFILE': 'passfile',
    }
    return {v: environ[k] for k, v in pg.items() if k in environ}
