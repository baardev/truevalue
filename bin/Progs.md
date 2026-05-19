# Programming manual (`bin/`)

Executable scripts in this folder. Invocation details live in script headers or `--help`; this file describes what each program is for.

## `twister-tholon.py`

Exploratory numerical demo for a **tholonic recursion** toward pi: updates an `N` state from paired `D` and `C` terms, tracks error versus `math.pi`, and optionally plots convergence, error on a log scale, and a complex-plane trace (real part `N`, imaginary part `C - D`).

**Depends on:** Python 3, `matplotlib` (for plots when run as main).
