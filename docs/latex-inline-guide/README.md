# Inline QPic Diagrams for LaTeX

This is a
 guide
 on how to setup
 the environment to be able to 
  write **qpic** diagrams directly inside your LaTeX source files. This eliminates the need to manually manage separate `.qpic` files and external exports.

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

To use the `\begin{qpic}` environment, create a file named `qpic-latex.sty`. You can place this in your project folder or in your local `texmf` directory (`~/texmf/tex/latex/qpic/`).

```latex
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{qpic-latex}[2026/08/24 Qpic integration for LaTeX]

\RequirePackage{tikz}
\RequirePackage{fancyvrb} 

\newcounter{qpicglobal}

\newenvironment{qpic}{%
  \stepcounter{qpicglobal}%
  \edef\qpicname{qpic-\arabic{qpicglobal}}%
  \VerbatimEnvironment
  \begin{VerbatimOut}{\qpicname.qpic}%
}{%
  \end{VerbatimOut}%
  \immediate\write18{qpic -f tikz \qpicname.qpic > \qpicname.tikz 2>\qpicname.err}%
  \IfFileExists{\qpicname.tikz}{%
    \input{\qpicname.tikz}%
  }{%
    \PackageError{qpic-latex}{Failed to compile \qpicname.qpic}{}%
  }%
}
```

---

## 3. Compilation

Because this setup uses `\write18` to call Python, you **must** enable `shell-escape`.

### Option A: Via Terminal (Manual)
Run this command to compile your document:
```bash
latexmk -pdf -shell-escape test.tex
```

### Option B: Via `.latexmkrc` (Automatic)
To avoid typing the flag every time, create a file named `.latexmkrc` in your home directory or project root:
```perl
$pdflatex = 'pdflatex -shell-escape %O %S';
```

---

## 4. VS Code Integration (LaTeX Workshop)


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

---

## 5. Test Example

```latex
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
* **`sh: 1: qpic: not found`**: LaTeX cannot find your `qpic` binary. Try replacing `qpic` in the `.sty` file with the absolute path (e.g., `/home/yourname/.local/bin/qpic`).
* **Empty diagram**: Ensure the `fancyvrb` package is installed and `shell-escape` is actually enabled in your build command.