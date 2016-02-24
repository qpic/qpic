#!/usr/bin/env python

from __future__ import print_function

import glob

prelude=r'''\documentclass{article}
\usepackage{tikz}
\usetikzlibrary{decorations.pathreplacing,decorations.pathmorphing}
\definecolor{bg}{rgb}{1,1,1}
\usepackage{hyperref}
\usepackage{fancyvrb}
\usepackage{amssymb}
\begin{document}
%\listoffigures
'''

postscript=r'''
\end{document}'''

print(prelude)
count = 0
L = glob.glob('*.qpic')+glob.glob('*.tikz')
S = sorted(list(set([file[:-5] for file in L])))
for filename in S:
    print('\n'+r'\SaveVerb{name}'+'|%s|'%filename)    
    print(r'\begin{figure}[ht]')
    #print(r'\begin{verbatim}'+'\n%s\n'%file+r'\end{verbatim}')
    print(r'\caption{\protect\UseVerb{name}}')
    print(r'\input'+'{%s.tikz}'%filename)
    #print(r'\makebox[\textwidth]{\includegraphics[width=\textwidth,height=\textheight,keepaspectratio]'+'{%s}}'%filename)
    print(r'\end{figure}')
    count += 1
    if count > 8:
        print(r'\clearpage')
        count = 0
print(postscript)

# TODO: Only scale image *down* to page size maximums
# TODO: List of figures using actual filenames. \protect\UseVerb fails to pass "name" parameter.
