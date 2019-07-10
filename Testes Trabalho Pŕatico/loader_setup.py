__author__ = "Emanuel Juliano Morais Silva"
__email__ = "emanueljulianoms@gmail.com"

import argparse
import json
import os

parser = argparse.ArgumentParser(description="""This script creates the folder structure
                                                for the other Reddit scripts.""")

parser.add_argument("--apikeydst", dest="keydst", type=str, default="./data/youtube/api_key.json",
                    help="YouTube v3 API key path.")

parser.add_argument("--cm", dest="cm", type=str, default="./data/reddit/cm/",
                    help="Folder to store the comments.")

parser.add_argument("--subm", dest="subm", type=str, default="./data/reddit/subm/",
                    help="Folder to store the submissions.")

args = parser.parse_args()

os.makedirs(args.cm, exist_ok=True)
os.makedirs(args.subm, exist_ok=True)
