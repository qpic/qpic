##########################################
# qpic Graphic Makefile
# Tom Draper and Sandy Kutin -- 2013
##########################################
# Targets
# $@ = file to be made
# $? = changed dependents
# $< = file that caused action
# $* = prefix shared by target and dependent files

# This makefile allows easy inclusion of qpic graphics into a LaTeX document.
# Suppose you are working with the file: mypic.qpic
# "make mypic.pdf" creates a PDF graphic that can be viewed directly.
# mypic.pdf can also be included into a LaTeX document.
#
# Required in main document:
# \usepackage{graphicx}
#
# Include diagram using:
# \begin{figure}
# \caption{My qpic Diagram}
# \includegraphics{mypic}
# \end{figure}

# Alternatively,
# "make mypic.tikz" creates TikZ (LaTeX) code that can be imported into the main document.
# 
# Required in main document preamble:
# \usepackage{tikz}
#
# Include diagram using:
# \begin{figure}
# \caption{My qpic Diagram}
# \input{mypic.tikz}
# \end{figure}

# Because we have two versions of TeX
PDFLATEX_FOR_PREVIEW = /usr/bin/pdflatex

# Change this to the name of your LaTeX document (without the .tex) 
MAIN = qpic_doc

# SEPARATE FILETYPES INTO GROUPS
TEX       = $(wildcard *.tex) # List all TeX files in directory
QPIC      = $(wildcard *.qpic) # List all QPIC files in directory
TIKZ      = $(wildcard *.tikz) # List all TIKZ files in directory
MISC      = $(wildcard *.sty) $(wildcard *.cls) $(wildcard *.png)

# IDENTIFY ALL SECONDARY TeX FILES THAT CAN BE SAFELY DELETED
TEX_tmp   = $(QPIC:.qpic=.tex) $(TIKZ:.tikz=.tex) # Files that make TeX files
TEX_all   = $(TEX) $(TEX_tmp) # All potential TeX files
# Complete list of intermediate TeX files that can be removed by "make clean"
TEX_junk  = $(TEX_all:.tex=.aux) $(TEX_all:.tex=.brf) $(TEX_all:.tex=.lof) $(TEX_all:.tex=.log) $(TEX_all:.tex=.nav) $(TEX_all:.tex=.out) $(TEX_all:.tex=.snm) $(TEX_all:.tex=.toc) $(TEX_all:.tex=.vrb) 

# PDF FILES AUTOMATICALLY CREATED FOR INSERTION INTO MAIN DOCUMENT
TEX_pdf   = $(TEX_tmp:.tex=.pdf) $(CODE:code.tex=code.pdf)

# TikZ FILES CREATED BY <q|pic>
QPIC_tikz = $(QPIC:.qpic=.tikz) # Create TikZ target names for all QPIC files

AUTO = $(TEX_junk) $(TEX_tmp) $(QPIC_tikz)

AUTO_pdf = $(TEX_all:.tex=.pdf) 

all:	$(MAIN).pdf

%.qpic:	%.py
	python $< >$@

%.tikz:	%.qpic
	qpic $< >$@ # qpic < $< >$@

%.tex:  %.tikz
	tikz2preview $< > $@

%.pdf:	%.tex
	$(PDFLATEX_FOR_PREVIEW) -interaction=nonstopmode $<

$(MAIN).pdf:	$(MAIN).tex $(TEX) $(QPIC_tikz) $(TEX_pdf)
	pdflatex -interaction=nonstopmode $<
#Rerun if references are not up to date
ifeq ($(grep 'LaTeX Warning: .* may have changed' %.log),)
	pdflatex -interaction=nonstopmode $<
endif

clean:
	/bin/rm -f $(AUTO)

distclean:
	/bin/rm -f $(AUTO) $(AUTO_pdf) *~

# Identify all autogenerate files and put them in .git/info/exclude
git:
	git init # Does nothing if repo already exists
	echo $(AUTO) $(AUTO_pdf) | xargs -n 1 echo > .git/info/exclude
	find . -type l -exec basename {} \; >> .git/info/exclude

.SECONDARY:	$(QPIC:.qpic=.tikz) $(QPIC:.qpic=.tex) $(TIKZ:.tikz=.tex)
.PHONY:		all clean distclean tar git test

