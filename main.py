import argparse
import platform
import os
from vm_setup import *

BASE_DIR = "tools/"

parser = argparse.ArgumentParser(
                    prog='VM setup',
                    description='Automated vm setup',
                    )
parser.add_argument('-d', '--dir', help="Directory where to store files, Default tools/")
args = parser.parse_args()

if args.dir != None:
    BASE_DIR = args.dir

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

os.chdir(BASE_DIR)
os_ = platform.system()

if os_ == "Linux":
    setup_linux()
else:
    setup_windows()