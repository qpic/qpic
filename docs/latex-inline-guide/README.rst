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

Copy ``qpic-latex.sty`` from this directory next to your ``.tex`` file
(or into ``~/texmf/tex/latex/qpic/``). Then::

    \usepackage{qpic-latex}

    \begin{qpic}
        ...
    \end{qpic}

While TeX runs, the environment writes ``qpic-N.qpic`` and compiles it
with::

    qpic qpic-N.qpic > qpic-N.tikz 2>qpic-N.err

See ``qpic-latex.sty`` for the full package (shell-escape checks, TikZ
libraries, and error handling).

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

Generated files
---------------

Each ``qpic`` environment leaves three files next to the ``.tex``
source, named ``qpic-N.qpic``, ``qpic-N.tikz``, and ``qpic-N.err``
(``N`` counts environments in the document). They are rebuildable: safe
to delete, and safe to ignore in git, for example::

    qpic-*.qpic
    qpic-*.tikz
    qpic-*.err

Keep ``qpic-N.err`` only if you need to inspect a failed ``qpic`` run.

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
    \author{Hughes Q. Pick}
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
- **Extra ``qpic-N.*`` files**: Expected; see *Generated files* above.
  Delete them or add them to ``.gitignore``. They are not the document.
