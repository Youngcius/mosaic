import numpy as np


def is_power_of_two(num):
    """Check whether a number is power of 2 or not."""
    return (num & (num - 1) == 0) and num != 0


def infidelity(u: np.ndarray, v: np.ndarray) -> float:
    """Infidelity between two matrices"""
    if u.shape != v.shape:
        raise ValueError('u and v must have the same shape.')
    d = u.shape[0]
    return 1 - np.abs(np.trace(u.conj().T @ v)) / d


def spectral_distance(u: np.ndarray, v: np.ndarray) -> float:
    """Spectral distance between two matrices"""
    if u.shape != v.shape:
        raise ValueError('u and v must have the same shape.')
    return np.linalg.norm(u - v, ord=2)
