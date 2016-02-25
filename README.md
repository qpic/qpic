---
title: Solarized
description: Precision colors for machines and people
author: Ethan Schoonover
tags: test, testing, test123
colors: light yellow
created:  2011 Mar 15
modified: 2011 Apr 16

---

Solarized
=========

## Precision colors for machines and people

[![solarized dualmode](https://github.com/altercation/solarized/raw/master/img/solarized-yinyang.png)](#features)

[![qpic dualmode](https://raw.githubusercontent.com/KutinS/qpic/tom/docs/images/BasicTeleportation.png)](#features)

[![qpic dualmode](https://github.com/KutinS/qpic/raw/tom/docs/images/BasicTeleportation.png)](#features)

[![qpic dualmode](https://github.com/KutinS/qpic/raw/tom/docs/images/BasicTeleportation.png)]

[![qpic dualmode](docs/images/BasicTeleportation.png)](#features)

qpic
===============================

![qpic logo](docs/images/typeset_qpic.pdf)

## Quantum circuits made easy

![qpic logo](docs/images/qpic.pdf)


[qpic_svg](https://raw.github.com/KutinS/qpic/raw/tom/docs/images/BasicTeleportation.svg)

[qpic_svg](https://raw.github.com/KutinS/qpic/raw/tom/docs/images/BasicTeleportation.png)

[qpic_svg2](docs/images/BasicTeleportation.png)

[qpic_svg2](/docs/images/BasicTeleportation.png)



[local ref](/docs/images/BasicTeleportation.png?raw=true)

[local ref2](docs/images/BasicTeleportation.png?raw=true)

.. image:: docs/images/typeset_qpic.pdf
   :scale: 200

.. image:: https://img.shields.io/pypi/v/qpic.svg
        :target: https://pypi.python.org/pypi/qpic

.. image:: https://img.shields.io/travis/SmoothDragon/qpic.svg
        :target: https://travis-ci.org/SmoothDragon/qpic

.. image:: https://readthedocs.org/projects/qpic/badge/?version=latest
        :target: https://readthedocs.org/projects/qpic/?badge=latest
        :alt: Documentation Status

.. |qpic| image:: docs/images/typeset_qpic.pdf
   :alt: <q|pic>

.. |tikz| image:: docs/images/typeset_tikz.pdf
   :alt: TikZ
   :align: middle
   :target: http://www.texample.net/tikz/

.. |latex| image:: docs/images/typeset_latex.pdf
   :alt: LaTeX
   :target: https://www.latex-project.org/

``qpic`` converts the |qpic| description of a quantum circuit into |latex| as a |tikz| graphic.

.. image:: docs/images/qpic.pdf
   :scale: 300

* Free software: GNU GPLv3 license
* Documentation: https://qpic.readthedocs.org.

Features
--------

The |qpic| language provides a concise, readable, ``ASCII`` format for describing quantum circuits. ``qpic`` converts |qpic| files to the scientific paper standard of |latex| using |tikz| graphic commands.

* Automatic placement of circuit components.
* Human readable.
* Input |qpic| syntax can be produced by other scripts.
* Can be included in |latex| documents in |tikz| or PDF form.

Examples
--------

Basic quantum teleportation circuit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://github.com/KutinS/qpic/blob/tom/docs/images/BasicTeleportation.svg

This classic diagram derives from the following code:

::

  a W |\psi\rangle
  b c W |\beta_{00}\rangle<
  c W |\psi\rangle
  a +b
  a H
  a b M
  c X b:owire
  c Z a:owire

Decorated quantum teleportation circuit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|qpic| has additional features for commenting or highlighting parts of a circuit. 

.. image:: docs/images/QuantumTeleportation.pdf

This diagram derives from the following:

::

  PREAMBLE \providecommand{\K}[1]{\left|#1\right\rangle}
  a  W \K{\phi} [x]
  x1 W type=o # Empty wire used for positioning
  x0 W style=dashed # Dividing line
  x2 W type=o # Empty wire used for positioning
  b0 W \K{0} [y]
  b1 W \K{0} \K{\phi}

  VERTICAL 0
  b1 H    % $\K{\phi}\K{0}(\K{0}{+}\K{1})$
  +b0 b1   % $(\alpha\K{0}{+}\beta\K{1})(\K{00}{+}\K{11})$
  b0 x1 PERMUTE
  +b0 a %$\scriptstyle\alpha\K{0}(\K{00}{+}\K{11}){+}\beta\K{1}(\K{10}{+}\K{01})$
  a H     % $\sum_{x,y}\K{xy}(\alpha\K{y}{+}(-1)^x\beta\K{\bar{y}})$
  a b0 M  % $[xy](\alpha\K{y}{+}(-1)^x\beta\K{\bar{y}})$
  x1 x2 a b0 PERMUTE
  +b1 b0   % $[xy](\alpha\K{0}{+}(-1)^x\beta\K{1})$
  b1 a  % $[xy](\alpha\K{0}{+}\beta\K{1})$

  # Colored boxes
  DEFINE qq fill=green style=rounded_corners
  DEFINE cc fill=blue style=rounded_corners
  b0 b1 x1 x2 @ 0 2 qq %% $[qq]$ Quantum entanglement
  a b0 x2 x1 @ 6 6 cc %% \hspace{.5cm}$2[c\rightarrow c]$ Classical channel



Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
