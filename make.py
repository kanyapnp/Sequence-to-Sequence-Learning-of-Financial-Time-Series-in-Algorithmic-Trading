#!/usr/bin/env python
import os, sys
sys.path.insert(0, os.path.join('build', 'pymake2'))

from pymake2 import *

from pymake2.template.latex import pdflatex
from pymake2.template.util  import fswatcher

@default_target(depends=[ 'compile' ])
def all(conf):
    pass

@after_target('compile')
def bibtex(conf):
    # Set the modified time and rerun pdflatex to insert citations properly, if
    # needed.

    bbl = os.path.join(conf.bindir, conf.name + '.bbl')
    bibmtime = os.path.getmtime(os.path.join(conf.srcdir, 'bibliography.bib'))

    if os.path.isfile(bbl) and bibmtime < os.path.getmtime(bbl):
        return

    srcfile = os.path.join(conf.srcdir, conf.srcfile)

    bibsrc = os.path.join(os.path.abspath('src'), 'bibliography.bib')
    cwd = os.getcwd()
    os.chdir(conf.bindir)
    # Have to copy this file for this to work with MacTeX.
    copy(bibsrc, r'.\bibliography.bib')
    run_program('bibtex', [ conf.name ])
    delete_file('bibliography.bib')
    os.chdir(cwd)

    atime = os.path.getatime(srcfile)
    mtime = os.path.getmtime(srcfile)

    os.utime(srcfile, None)
    pdflatex.compile(conf)

    os.utime(srcfile, None)
    pdflatex.compile(conf)

    # Restore access and modified times to not break the 'watch' target.
    os.utime(srcfile, (atime, mtime))

pymake2({
    'name'    : 'thesis',
    'srcfile' : 'main.tex'
})
