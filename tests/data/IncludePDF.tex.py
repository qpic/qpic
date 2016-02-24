#!/usr/bin/env python

from __future__ import print_function

import glob

prelude=r'''\documentclass{article}
\usepackage{graphicx} % Used to import .pdf files.
\usepackage{fancyvrb}
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
    print(r'\caption{\protect\UseVerb{name}}')
    print(r'\makebox[\textwidth]{\includegraphics[width=\textwidth,height=\textheight,keepaspectratio]'+'{{%s}.pdf}}'%filename)
    print(r'\end{figure}')
    count += 1
    if count > 8:
        print(r'\clearpage')
        count = 0
print(postscript)

# TODO: Only scale image *down* to page size maximums
# TODO: List of figures using actual filenames. \protect\UseVerb fails to pass "name" parameter.

