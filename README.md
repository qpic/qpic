# ⟨q|pic⟩

## Quantum circuits made easy

[![qpic dualmode](https://github.com/KutinS/qpic/raw/tom/docs/images/qpic.png)](#features)

**qpic** converts the ⟨q|pic⟩ description of a quantum circuit into LaTeX as a TikZ graphic.

* Free software: GNU GPLv3 license
* Documentation: https://qpic.readthedocs.org.
<p align="center">
    <a href="https://img.shields.io/pypi/v/qpic.svg">
        <img src="https://img.shields.io/pypi/v/qpic.svg"
             alt="build status">
    </a>
    <a href="https://travis-ci.org/SmoothDragon/qpic">
        <img src="https://img.shields.io/travis/SmoothDragon/qpic.svg"
             alt="build status">
    </a>
    <a href="https://readthedocs.org/projects/qpic/?badge=latest">
        <img src="https://readthedocs.org/projects/qpic/badge/?version=latest"
             alt="documentation status">
    </a>
</p>

<!---
.. image:: https://img.shields.io/pypi/v/qpic.svg
        :target: https://pypi.python.org/pypi/qpic

.. image:: https://img.shields.io/travis/SmoothDragon/qpic.svg
        :target: https://travis-ci.org/SmoothDragon/qpic

.. image:: https://readthedocs.org/projects/qpic/badge/?version=latest
        :target: https://readthedocs.org/projects/qpic/?badge=latest
        :alt: Documentation Status
--->

## Features

The ⟨q|pic⟩ language provides a concise, readable, ASCII format for describing quantum circuits. **qpic** converts ⟨q|pic⟩ files to the scientific paper standard of LaTeX using TikZ graphic commands.

* Automatic placement of circuit components.
* Human readable.
* Input ⟨q|pic⟩ syntax can be produced by other scripts.
* Can be included in LaTeX documents in TikZ or PDF form.

## Examples

### Basic quantum teleportation circuit

[![qpic dualmode](https://github.com/KutinS/qpic/raw/tom/docs/images/BasicTeleportation.png)](#features)

This classic diagram derives from the following code:

```
a W |\psi\rangle
b c W |\beta_{00}\rangle<
c W |\psi\rangle
a +b
a H
a b M
c X b:owire
c Z a:owire
```

### Decorated quantum teleportation circuit

⟨q|pic⟩ has additional features for commenting or highlighting parts of a circuit. 

[![qpic dualmode](https://github.com/KutinS/qpic/raw/tom/docs/images/QuantumTeleportation.png)](#features)

This diagram derives from the following:

```
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
```

For an explanation of `qpic` commands and more examples, see the official documentation.

## Credits

This package was created with Cookiecutter and the `audreyr/cookiecutter-pypackage` project template.
