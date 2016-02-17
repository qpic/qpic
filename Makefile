##########################################
# <q|pic> Makefile
# Tom Draper and Sandy Kutin -- 2013
##########################################

#############################################################################
#Copyright (c) 2013, Institute for Defense Analyses, 4850 Mark Center Drive;#
#               Alexandria, VA 22311-1882; 703-845-2500                     #
#                                                                           #
#This material may be reproduced by or for the US Government pursuant to the#
#copyright license under the clauses at DFARS 252.227-7013 and 252.227-7014.#
#                                                                           #
#    Do not distribute without express written permission of the authors    #
#############################################################################

# This makefile creates PDF graphics from .qpic files and manages their inclusion
# into a master LaTeX document. Usage examples assume <q|pic> file "diagram.qpic"
# and document file "mainfile.tex". Users should modify the two "# USER CHANGE:" 
# lines as necessary.
# 
# Usage 1: Making standalone PDF graphics
# "make diagram.pdf" creates a PDF graphic that can be viewed directly.
# 
# Usage 2: Including .qpic diagrams as PDF files
# "make" executes PDFLaTeX on "mainfile.tex" assuming all .qpic files as dependencies.
#
#   Required in main document preamble:
#   \usepackage{graphicx}
#
#   Include "diagram.pdf" using:
#   \includegraphics{diagram}

# Usage 3: Including .qpic diagrams as TikZ code
# "make" executes PDFLaTeX on "mainfile.tex" assuming all .qpic files as dependencies.
# 
#   Required in main document preamble:
#   \usepackage{tikz}
#
#   Include "diagram.tikz" using:
#   \input{diagram.tikz}

# Identify <q|pic> and TeX files
QPIC       = $(wildcard *.qpic) # List all <q|pic> files in directory
TEX        = $(wildcard *.tex)  # List all TeX files in directory

# Secondary files created by <q|pic> that can safely be removed by "make clean"
QPIC_tikz  = $(QPIC:.qpic=.tikz) 
QPIC_tex   = $(QPIC:.qpic=.tex)
QPIC_pdf   = $(QPIC:.qpic=.pdf)
QPIC_files = $(QPIC_tikz) $(QPIC_tex) $(QPIC_pdf)

# All TeX files
TEX_all    = $(TEX) $(QPIC_tex)

# Secondary files created by LaTeX that can be safely removed by "make clean"
TEX_files  = texput.log $(TEX_all:.tex=.aux) $(TEX_all:.tex=.brf) $(TEX_all:.tex=.lof) $(TEX_all:.tex=.log) $(TEX_all:.tex=.nav) $(TEX_all:.tex=.out) $(TEX_all:.tex=.snm) $(TEX_all:.tex=.toc) $(TEX_all:.tex=.vrb) $(TEX_all:.tex=.pdf)

# USER CHANGE: Name of your LaTeX document (without the .tex) 
MAIN = mainfile

all:	$(MAIN).pdf

# USER CHANGE: Document dependencies on the next line 
$(MAIN).pdf:	$(TEX) $(QPIC_pdf) 
	pdflatex -interaction=nonstopmode $(MAIN).tex
#Rerun if references are not up to date
ifeq ($(grep 'LaTeX Warning: .* may have changed' $(MAIN).log),)
	pdflatex -interaction=nonstopmode $(MAIN).tex
endif

%.tikz:	%.qpic
	python qpic.py < $< >$@

%.tex:	%.tikz
	python tikz2preview $< > $@

%.pdf:	%.tex
	pdflatex -interaction=nonstopmode $<

clean:
	/bin/rm -f $(QPIC_files) $(TEX_files)

.SECONDARY:	$(QPIC_files) $(TEX_files)
.PHONY:		all clean 

