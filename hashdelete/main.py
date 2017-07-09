from argparse import ArgumentParser
from os import listdir, remove
from os.path import isfile, join
from hashlib import md5, sha1, sha512

parser = ArgumentParser(description='List or remove double files using their hashsums.')
parser.add_argument('-d', '--delete', action='store_true',
                    help='Deletes double files.')
parser.add_argument('-q', '--quiet', action="store_true",
                    help='Turns off console output.')
parser.add_argument('directory', type=str,
                    help='The directory to find files in.')
parser.add_argument('-ht', '--hashtype', type=str, default='Sha512',
                    help='The hash type to use. Options: MD5, Sha1, Sha512 (default).')

args = parser.parse_args()

path = args.directory if args.directory.endswith('/') else args.directory + '/'

if args.hashtype == 'MD5':
  hashfunc = md5
elif args.hashtype == 'Sha1':
  hashfunc = sha1
elif args.hashtype == 'Sha512':
  hashfunc = sha512

dic = {}

for f in listdir(path):
  if isfile(join(path, f)):
    hash = hashfunc(open(path+f, 'rb').read()).hexdigest()
  if hash in dic:
    if not args.quiet:
      print(path+f + " double of " + dic[hash] + "." + (" Deleting..." if args.delete else ""))
    if args.delete:
      remove(path+f)
  else:
    dic[hash] = path+f

