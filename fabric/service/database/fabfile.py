# coding=utf-8

from common import *
import service.database.mariadb as mariadb
import service.database.postgres as postgres

ns = Collection(config)
ns.add_collection(mariadb, 'mar')
ns.add_collection(postgres, 'pos')




