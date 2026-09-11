===============================
Inline qpic diagrams for LaTeX
===============================

This guide shows how to write qpic diagrams directly in a ``.tex`` file
with a ``qpic`` environment, so you do not have to keep a separate
``.qpic`` file and export by hand.

Shell escape
============

``qpic-latex`` runs the **qpic** program while TeX compiles the
document (``\write18`` / shell escape). Passing ``-shell-escape``
(TeX Live) or ``-enable-write18`` (MiKTeX) does not only allow qpic:
it allows **any** shell command in that ``.tex`` file and in every
package it loads.

- Compile this way **only for documents you trust**.
- The package prints a warning on every run so the log shows that the
  shell is being used.
- If shell escape is off, or only TeX Live's default restricted list is
  enabled, the package **stops with an error**.

Do **not** put ``-shell-escape`` in a home-directory ``.latexmkrc`` or a
global editor setting that applies to every paper. That would enable the
shell for documents that never needed it.

1. Prerequisites
================

Install LaTeX tools
-------------------

Ensure you have ``latexmk`` installed::

    sudo apt update
    sudo apt install texlive-full latexmk

Install qpic
------------

qpic is a command-line program. On Debian/Ubuntu, install it with
``pipx`` so it lands on your ``PATH`` without touching system Python::

    sudo apt install pipx
    pipx ensurepath
    pipx install qpic

Open a new terminal (or source your shell config), then check::

    qpic --version

If you already use a virtual environment, install there instead, and
make sure TeX can see that ``qpic`` when it runs (the venv ``bin``
directory must be on ``PATH``)::

    python3 -m venv ~/.venvs/qpic
    source ~/.venvs/qpic/bin/activate
    pip install qpic

2. The qpic-LaTeX style file
============================

To use the ``qpic`` environment, use the ``qpic-latex.sty`` shipped in
this directory (or copy it next to your ``.tex`` file, or into
``~/texmf/tex/latex/qpic/``). The file is:

.. code-block:: latex

    \NeedsTeXFormat{LaTeX2e}
    \ProvidesPackage{qpic-latex}[2026/09/11 Qpic integration for LaTeX]

    \RequirePackage{tikz}
    \usetikzlibrary{decorations.pathreplacing,decorations.pathmorphing}
    \RequirePackage{fancyvrb}
    \RequirePackage{shellesc}

    \PackageWarningNoLine{qpic-latex}{%
      This package runs the qpic program via shell escape.^^J%
      -shell-escape allows any shell command in this document,^^J%
      not only qpic. Compile this way only for sources you trust}

    \ifcase\ShellEscapeStatus
      \PackageError{qpic-latex}{%
        Shell escape is disabled\MessageBreak
        qpic-latex runs qpic via the shell while TeX runs}%
       {Compile with -shell-escape (TeX Live) or -enable-write18 (MiKTeX).^^J%
        That flag enables the shell for the entire document, so use it^^J%
        only on sources you trust.}%
    \or
    \else
      \PackageError{qpic-latex}{%
        Restricted shell escape is not enough\MessageBreak
        qpic is not on TeX Live's restricted command list}%
       {Compile this document with unrestricted -shell-escape.^^J%
        Restricted mode cannot run qpic. Only do this for sources you trust.}%
    \fi

    \newcounter{qpicglobal}

    \newenvironment{qpic}{%
      \stepcounter{qpicglobal}%
      \edef\qpicname{qpic-\arabic{qpicglobal}}%
      \VerbatimEnvironment
      \begin{VerbatimOut}{\qpicname.qpic}%
    }{%
      \end{VerbatimOut}%
      \ShellEscape{qpic \qpicname.qpic > \qpicname.tikz 2>\qpicname.err}%
      \IfFileExists{\qpicname.tikz}{%
        \input{\qpicname.tikz}%
      }{%
        \PackageError{qpic-latex}{Failed to compile \qpicname.qpic}{}%
      }%
    }

3. Compilation
==============

Option A: via terminal (this document only)
-------------------------------------------

::

    latexmk -pdf -shell-escape test.tex

The ``-shell-escape`` flag is a trust decision for ``test.tex``, not a
general TeX setting.

Option B: project-local ``.latexmkrc``
--------------------------------------

To avoid typing the flag in this folder, create ``.latexmkrc`` **in the
project directory** (the same folder as the ``.tex`` file), not in your
home directory::

    $pdflatex = 'pdflatex -shell-escape %O %S';

4. VS Code integration (LaTeX Workshop)
=======================================

Enable shell escape **for this workspace** if you trust the documents in
it. Do not turn it on in user-wide settings unless every document you
compile is trusted.

Prefer workspace ``.vscode/settings.json`` over user settings. Search
for ``latex-workshop.latex.tools`` and add ``"-shell-escape"`` as an
argument for ``latexmk``::

    "args": [
        "-shell-escape",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-pdf",
        "-outdir=%OUTDIR%",
        "%DOC%"
    ]

5. Test example
===============

.. code-block:: latex

    % This document requires -shell-escape: \usepackage{qpic-latex} runs
    % qpic via the shell. Only compile this way for documents you trust.
    \documentclass{article}
    \usepackage{amsmath}
    \usepackage{qpic-latex}

    \begin{document}
    \title{Quantum Circuit Test}
    \author{Me}
    \maketitle


    \begin{figure}[h]
        \centering
        \begin{qpic}
            SCALE 2.1
            PREAMBLE \providecommand{\ket}[1]{\left|#1\right\rangle}
            a W \ket{\psi}_{A_i} a_i
            b W \ket{\psi}_{B_i} b_i

            b C a
            a H
            a b M
        \end{qpic}
        \caption{Inline qpic diagram.}
    \end{figure}

    \end{document}

Troubleshooting
---------------

- **``qpic-latex`` error about shell escape**: You compiled without
  ``-shell-escape`` (or only restricted ``\write18`` is on). Rebuild with
  ``latexmk -pdf -shell-escape …`` for a document you trust.
- **``sh: 1: qpic: not found``**: LaTeX cannot find your ``qpic``
  binary. Try replacing ``qpic`` in the ``.sty`` file with the absolute
  path (e.g., ``/home/yourname/.local/bin/qpic``).
- **Empty diagram**: Ensure the ``fancyvrb`` package is installed and
  the compile actually used ``-shell-escape`` (check the log for the
  qpic-latex warning).
