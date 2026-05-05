#!/usr/bin/env python3

import math
import cmath
import matplotlib.pyplot as plt


def tholonic_pi_simulation(iterations=500, h_step=2):
    """
    Tholonic π recursion.

    N starts at 1.
    Each step applies:
        N_next = N - 1/sum_d + 1/prod_c

    Then π estimate is:
        pi_estimate = 4 * N
    """

    N = 1.0
    sum_d = 3.0
    prod_c = 5.0

    history = []

    for k in range(iterations):
        D = 1.0 / sum_d
        C = 1.0 / prod_c

        N = N - D + C
        pi_estimate = 4.0 * N
        error = pi_estimate - math.pi

        # Complex interpretation:
        # real axis = negotiated N-state
        # imaginary axis = imbalance between C and D
        imbalance = C - D
        Z = complex(N, imbalance)

        history.append({
            "k": k,
            "N": N,
            "pi_estimate": pi_estimate,
            "error": error,
            "D": D,
            "C": C,
            "imbalance": imbalance,
            "Z": Z,
        })

        sum_d += h_step ** 2
        prod_c += 2 * h_step

    return history


def plot_convergence(history):
    ks = [row["k"] for row in history]
    estimates = [row["pi_estimate"] for row in history]
    errors = [abs(row["error"]) for row in history]

    plt.figure()
    plt.plot(ks, estimates, label="Tholonic π estimate")
    plt.axhline(math.pi, linestyle="--", label="math.pi")
    plt.xlabel("Iteration")
    plt.ylabel("π estimate")
    plt.title("Tholonic π Recursion Convergence")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(ks, errors)
    plt.xlabel("Iteration")
    plt.ylabel("Absolute error")
    plt.title("Error Convergence Toward π")
    plt.yscale("log")
    plt.grid(True)
    plt.show()


def plot_complex_phase(history):
    xs = [row["Z"].real for row in history]
    ys = [row["Z"].imag for row in history]

    plt.figure()
    plt.plot(xs, ys, marker=".", markersize=2)
    plt.xlabel("Real axis: N-state")
    plt.ylabel("Imaginary axis: imbalance C - D")
    plt.title("Complex Plane View of Tholonic Recursion")
    plt.grid(True)
    plt.show()


def print_summary(history):
    last = history[-1]

    print("Final result")
    print("------------")
    print(f"Iterations:     {len(history)}")
    print(f"N-state:        {last['N']}")
    print(f"π estimate:     {last['pi_estimate']}")
    print(f"math.pi:        {math.pi}")
    print(f"error:          {last['error']}")
    print(f"absolute error: {abs(last['error'])}")


if __name__ == "__main__":
    history = tholonic_pi_simulation(iterations=500, h_step=2)

    print_summary(history)
    plot_convergence(history)
    plot_complex_phase(history)
