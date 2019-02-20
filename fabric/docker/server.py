
from common import *
from docker.image import *
from optparse import OptionParser

parser = OptionParser(usage='%prog --server server --http --proxy')
parser.add_option('--server', dest='server', help='server type')
parser.add_option('--http', dest='http', action='store_true', help='use local yum http source')
parser.add_option('--proxy', dest='proxy', action='store_true', help='use local yum proxy')

(options, args) = parser.parse_args()

class Entry:
    def __init__(self, path, work):
        self.path = path
        self.work = work


redirect = {'http': Entry('service/source', 'fab source.http')}

glob_conf.fake = True
# entry = redirect.get(options.server)
entry = redirect.get('http')
# os.system('cd {path}; {work}'.format(path=os.path.join(glob_conf.path, entry.path), work=entry.work))

from invoke import Context
server = __import__('service.source.server', fromlist=['*'])
# server.file(Context)
server.work()