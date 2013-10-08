ssg: stupid site generator
===

I've been looking for a static site generator that fits my needs to no avail. I
want:
- Something that doesn't mess with directory strutures
- Something that requires me to spend approximately zero time configuring anything
- Something that takes &lt;30 seconds to install
- Something that can generate a blog-like list of all available pages

So far, ssg does the first three, and I'm working on the fourth.

Usage
--

Using ssg is stupid simple. Just run:

    python ssg.py input_directory output_directory

If you're generating Markdown and you want to wrap all of your Markdown files in
a template, add the `--md_template` argument with a path to a Jinja template.

Design
--

The concept of ssg is that compiling a static site should be equivalent to
copying a bunch of files from one place to another, and transforming some of
them in the process. ssg does this by doing a deep copy of the input directory
to the output directory, and when it sees a file extension for which there is a
plugin, it calls that plugin instead of doing a straight copy. There's a
markdown plugin that comes in the box, and I'm happy to take pull requests to
add other plugins as well.
