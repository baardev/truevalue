#!/usr/bin/env python3

from functools import partial


def x_pi_over_4(max_iter: int, seeds: tuple, istep: int = 2) -> float:
    N, D, C = seeds
    d_step = istep**2
    c_step = istep * 2
    for _ in range(max_iter):
        N = N - (1.0 / D) + (1.0 / C)
        D += d_step
        C += c_step
    return N


def x_phi(max_iter: int, seeds: tuple) -> float:
    N, D, C = seeds
    for _ in range(max_iter):
        N = 1.0 + (1.0 / N)
    return N


def x_e(max_iter: int, seeds: tuple) -> float:
    N, D, C = seeds
    N = D / C
    C = D
    for count in range(1, max_iter):
        C *= count
        N += D / C
    return N


def x_sqrt2(max_iter: int, seeds: tuple) -> float:
    N, D, C = seeds
    for _ in range(max_iter):
        N = (N + (D / N)) / C
    return N


def x_ln2(max_iter: int, seeds: tuple) -> float:
    N, D, C = seeds
    for count in range(max_iter):
        term = D / (count + C)
        N = N + term if count % 2 == 0 else N - term
    return N


_CALCULATORS = {
    "pi/4": partial(x_pi_over_4, seeds=(1.0, 3.0, 5.0)),
    "phi":  partial(x_phi,       seeds=(1.0, 1.0, 2.0)),
    "e":    partial(x_e,         seeds=(0.0, 1.0, 1.0)),
    "sqrt2":partial(x_sqrt2,     seeds=(1.0, 2.0, 2.0)),
    "ln2":  partial(x_ln2,       seeds=(0.0, 1.0, 1.0)),
}


def compute_tholonic_constant(constant_type="pi/4", max_iter=100000):
    calculator = _CALCULATORS.get(constant_type)
    if calculator is None:
        raise ValueError(f"Unknown constant_type: {constant_type}")
    return calculator(max_iter)


if __name__ == "__main__":
    constant_types = ["pi/4", "phi", "e", "sqrt2", "ln2"]
    for constant_type in constant_types:
        result = compute_tholonic_constant(constant_type)
        print(f"{constant_type} = {result}")
