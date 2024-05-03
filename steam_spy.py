import yaml
from argparse import ArgumentParser
from steam_service import SteamService

with open('config/setting.yaml', 'r') as file:
    setting = yaml.safe_load(file)

parser = ArgumentParser(description=__doc__)

parser.add_argument('-d', '--discount',  dest='d', default=setting['discount'], type=int,   help='[%] Minimum discount of the apps')
parser.add_argument('-l', '--lifespan',  dest='l', default=setting['lifespan'], type=int,   help='[days] Lifespan of the reports')
parser.add_argument('-f', '--filepath',  dest='f', default=setting['filepath'],             help='Filepath of the report database')
parser.add_argument('-s', '--sender',    dest='s', default=setting['sender']['email'],      help='Address for the sender email')
parser.add_argument('-p', '--password',  dest='p', default=setting['sender']['password'],   help='Password for the sender email')
parser.add_argument('-r', '--receivers', dest='r', default=setting['receivers'], nargs='+', help='Recipients email addresses')

args = parser.parse_args()

steam_service = SteamService(args.d, args.l, args.f, args.s, args.p)
steam_service.proces_message(args.r)
