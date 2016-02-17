##########################################
# qpic Graphic Makefile
# Tom Draper and Sandy Kutin -- 2013
##########################################
# Targets
# $@ = file to be made
# $? = changed dependents
# $< = file that caused action
# $* = prefix shared by target and dependent files

# "make all" will create two graphics files containing all *.qpic files in the directory
# IncludeTeX.pdf: File created by inputing the *.tikz (TeX) files from each *.qpic file.
# IncludePDF.pdf: File created by including the *.pdf files from each *.qpic file.
# 
# This makefile can be modified to build LaTeX documents that include qpic files in either framework.

PYTHON = python # Set Python version - test direct versions using "make python2" or "make python3"

DIR  = Graphics # Name of directory. Used by "make tar".

# Because we have two versions of TeX
PDFLATEX_FOR_PREVIEW = /usr/bin/pdflatex

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

AUTO = IncludeTeX.tex IncludePDF.tex $(TEX_junk) $(TEX_tmp) $(QPIC_tikz)

AUTO_pdf = $(TEX_all:.tex=.pdf) 

all:	IncludeTeX.pdf IncludePDF.pdf

%.qpic:	%.py
	$(PYTHON) $< >$@

# If <q|pic> fails, remove output file
%.tikz:	%.qpic
	$(PYTHON) qpic.py $< >$@ || (rm $@ ; false)

%.tex:	%.tikz
	./tikz2preview $< > $@

%.pdf:	%.tex
	$(PDFLATEX_FOR_PREVIEW) -interaction=nonstopmode $<

# Special case where base TeX file is created by a program
IncludePDF.tex: IncludePDF.tex.py $(QPIC) $(TIKZ)
	$(PYTHON) $< > $@ 

IncludePDF.pdf:	IncludePDF.tex $(TEX) $(TEX_pdf) 
	pdflatex -interaction=nonstopmode $<
#Rerun if references are not up to date
ifeq ($(grep 'LaTeX Warning: .* may have changed' %.log),)
	pdflatex -interaction=nonstopmode $<
endif

IncludeTeX.tex: IncludeTeX.tex.py $(QPIC) $(TIKZ)
	$(PYTHON) $< > $@ 

IncludeTeX.pdf:	IncludeTeX.tex $(TEX) $(TEX_pdf) 
	pdflatex -interaction=nonstopmode $<
#Rerun if references are not up to date
ifeq ($(grep 'LaTeX Warning: .* may have changed' %.log),)
	pdflatex -interaction=nonstopmode $<
endif

clean:
	/bin/rm -f $(AUTO)

distclean:
	/bin/rm -f $(AUTO) $(AUTO_pdf) *~

tar:	$(BASE).pdf
	tar  --exclude='*.tgz' -czvhf $(DIR).tgz ../$(DIR)/*

# Identify all autogenerate files and put them in .git/info/exclude
git:
	echo $(AUTO) $(AUTO_pdf) | xargs -n 1 echo > ../.git/info/exclude
	find . -type l -exec basename {} \; >> ../.git/info/exclude

# Execute entire build process using Python3
python3:PYTHON=python3
python3:	| distclean all
	$(PYTHON) -V

# Execute entire build process using Python2
python2:PYTHON=python2
python2:	| distclean all
	$(PYTHON) -V

.SECONDARY:	$(QPIC:.qpic=.tikz) $(QPIC:.qpic=.tex) $(TIKZ:.tikz=.tex)
.PHONY:		all clean distclean tar git python2 python3

