# Inline QPic Diagrams for LaTeX

This is a
 guide
 on how to setup
 the environment to be able to 
  write **qpic** diagrams directly inside your LaTeX source files. This eliminates the need to manually manage separate `.qpic` files and external exports.

## Shell escape

`qpic-latex` runs the **qpic** program while TeX compiles the document (`\write18` / shell escape). Passing `-shell-escape` (TeX Live) or `-enable-write18` (MiKTeX) does not only allow qpic: it allows **any** shell command in that `.tex` file and in every package it loads.

- Compile this way **only for documents you trust**.
- The package prints a warning on every run so the log shows that the shell is being used.
- If shell escape is off, or only TeX Live's default restricted list is enabled, the package **stops with an error**.

Do **not** put `-shell-escape` in a home-directory `.latexmkrc` or a global editor setting that applies to every paper. That would enable the shell for documents that never needed it.

---

## 1. Prerequisites

### Install LaTeX Tools
Ensure you have `latexmk` installed:
```bash
sudo apt update
sudo apt install texlive-full latexmk
```

### Install QPic
Install the qpic tool via Python. On Ubuntu 24.04+, use the `--break-system-packages` flag to install it to your user directory:
```bash
sudo apt install python3-pip python3-venv
pip install --user qpic --break-system-packages
```

### Verify PATH
The binary lives in `~/.local/bin`. Ensure this is in your PATH:
```bash
qpic --version
```
If the command is not found, add it to your `.bashrc`:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 2. The QPic-LaTeX Style File

To use the `\begin{qpic}` environment, use the `qpic-latex.sty` shipped in this directory (or copy it next to your `.tex` file, or into `~/texmf/tex/latex/qpic/`). The file is:

```latex
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
```

---

## 3. Compilation

### Option A: Via Terminal (this document only)

```bash
latexmk -pdf -shell-escape test.tex
```

The `-shell-escape` flag is a trust decision for `test.tex`, not a general TeX setting.

### Option B: Project-local `.latexmkrc`

To avoid typing the flag in this folder, create `.latexmkrc` **in the project directory** (the same folder as the `.tex` file), not in your home directory:

```perl
$pdflatex = 'pdflatex -shell-escape %O %S';
```

---

## 4. VS Code Integration (LaTeX Workshop)

Enable shell escape **for this workspace** if you trust the documents in it. Do not turn it on in user-wide settings unless every document you compile is trusted.

### Enable Shell Escape in VS Code
To allow VS Code to build the diagrams, edit your `settings.json`:
1. Search for `latex-workshop.latex.tools`.
2. Add `"-shell-escape"` as an argument for `latexmk`:
```json
"args": [
    "-shell-escape",
    "-synctex=1",
    "-interaction=nonstopmode",
    "-file-line-error",
    "-pdf",
    "-outdir=%OUTDIR%",
    "%DOC%"
]
```

Prefer workspace `.vscode/settings.json` over user settings.

---

## 5. Test Example

```latex
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
```

---

### Troubleshooting
* **`qpic-latex` error about shell escape**: You compiled without `-shell-escape` (or only restricted `\write18` is on). Rebuild with `latexmk -pdf -shell-escape …` for a document you trust.
* **`sh: 1: qpic: not found`**: LaTeX cannot find your `qpic` binary. Try replacing `qpic` in the `.sty` file with the absolute path (e.g., `/home/yourname/.local/bin/qpic`).
* **Empty diagram**: Ensure the `fancyvrb` package is installed and the compile actually used `-shell-escape` (check the log for the qpic-latex warning).
