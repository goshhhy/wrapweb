import argparse
import git
import github
import os.path
import tempfile

from mesonwrap import gitutils
from mesonwrap import webapi
from mesonwrap import wrapcreator
from mesonwrap.tools import environment


def main(prog, args):
    parser = argparse.ArgumentParser(prog)
    parser.add_argument('name')
    parser.add_argument('version')
    parser.add_argument('--test')
    args = parser.parse_args(args)
    wrapcreator.make_wrap(name=args.name,
                          repo_url=,
                          branch=args.version)
