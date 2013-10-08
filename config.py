'''
Configuration for ssg. file_handlers takes a map of file extension to method
used to process that extension. The processor method should take four arguments:
path, file, outdir and args. Path is the directory that the input file is in,
file is the name of the file, outdir is the output directory where the processed
file should be placed, args are the parsed command line arguments. Processor
methods must return true if the file was handled appropriately, or false if it
was not handled.

If there is not a handler for a file extension, or if the handler returns false
for a file type, the file will just be copied from the input to the output tree.
To override the default behavior for all unknown file types, register a handler
for the empty extension.

To add command line arguments to ssg, add a populate_args method that takes an
argparse.ArgumentParser and adds the needed arguments to it.
'''

from handlers import handler, wrap
import markdown
import os

def populate_args(parser):
  parser.add_argument('--md_template', type=str,
      help='path of jinja template to use when rendering markdown')

@handler('md')
def md(path, file, outdir, args):
  with open(os.path.join(path, file)) as f:
    html = markdown.markdown(f.read())
  outfile = os.path.join(outdir, file.rsplit('.', 1)[0] + '.html')
  if args.md_template:
    html = wrap(args.md_template, content=html)
  with open(outfile, 'w') as f:
    f.write(html)
  return True
