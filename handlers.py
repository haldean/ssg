import jinja2

file_handlers = {}

def handler(ext):
  '''
  Use this as an annotation on a method to use that method as a file handler.

  Example:
      @handler('md')
      def process_md(path, file, outdir):
        markdown.process(os.path.join(path, file), os.path.join(outdir, file))
  '''
  def wrap(func):
    file_handlers[ext] = func
    return func
  return wrap

def wrap(tfile, **kwargs):
  '''Convenience method for using a jinja2 template with the provided content.'''
  with open(tfile) as f:
    template = jinja2.Template(f.read())
  return template.render(**kwargs)
