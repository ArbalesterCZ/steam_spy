from argparse import ArgumentParser
from steam_service import SteamService

parser = ArgumentParser(description=__doc__)

parser.add_argument('-d', '--discount', dest='d', default=50, type=int, help='[%] Minimum discount of the apps')
parser.add_argument('-l', '--lifespan', dest='l', default=14, type=int, help='[days] Lifespan of the reports.')
parser.add_argument('-f', '--filepath', dest='f', default='report_database', help='Filepath of the report database.')

parser.add_argument('-s', '--sender',    dest='s', required=True, help='Address for sender email')
parser.add_argument('-p', '--password',  dest='p', required=True, help='Password for sender email')
parser.add_argument('-r', '--receivers', dest='r', required=True, nargs='+', help='Recipients email addresses.')

args = parser.parse_args()

steam_service = SteamService(args.d, args.l, args.f, args.s, args.p, args.r)
steam_service.proces_message()
