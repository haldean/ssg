#!/usr/bin/env python

'''
ssg: stupid site generator.

Given a directory structure, copies all files in the directory to a different
directory with optional extension-based transformations while copying. By
default, it transforms Markdown files and nothing else. To add support for other
file types, modify config.py.
'''

from sh import cp, mkdir, rm

import argparse
import os
import sys

# import config, which populates the file_handlers map in the handlers module
import config
from handlers import file_handlers

_debug = True

def handle_unknown(path, file, outdir):
  if '' in file_handlers:
    if file_handlers[''](path, file, outdir, args):
      return
  cp(os.path.join(path, file), outdir)

def handle_file(path, file, outdir):
  print outdir
  ext_start = file.rfind('.')
  if ext_start < 0:
    debug('found no extension on file %s' % file)
    handle_unknown(path, file, outdir)
    return
  ext = file[ext_start+1:]
  if ext in file_handlers:
    debug('found known extension', ext)
    if not file_handlers[ext](path, file, outdir, args):
      debug('handler for %s returned false, copying' % ext)
      handle_unknown(path, file, outdir)
  else:
    debug('found unknown extension %s on file %s' % (ext, file))
    handle_unknown(path, file, outdir)

def gen_site(indir, outdir):
  if not os.path.exists(indir):
    print 'Input tree "%s" does not exist, exiting.' % indir
    return

  if not os.path.exists(outdir):
    mkdir(outdir, p=True)

  for dirpath, dirname, files in os.walk(indir):
    relpath = os.path.relpath(dirpath, start=indir)
    outpath = os.path.join(outdir, relpath)
    if relpath and not os.path.exists(outpath):
      mkdir(outpath, p=True)
    for file in files:
      handle_file(dirpath, file, outpath)

def debug(*strs):
  if _debug:
    print(' '.join(strs))

def usage():
  print sys.argv[0] + ' [input tree] [output tree]'
  exit()

def parse_args():
  parser = argparse.ArgumentParser(description='stupid site generator')
  parser.add_argument('input_tree', type=str, help='input directory')
  parser.add_argument(
      'output_tree', type=str,
      help='output directory (existing files will be overwritten)')
  if 'populate_args' in config.__dict__:
    config.populate_args(parser)
  return parser.parse_args()

if __name__ == '__main__':
  args = parse_args()
  gen_site(args.input_tree, args.output_tree)
