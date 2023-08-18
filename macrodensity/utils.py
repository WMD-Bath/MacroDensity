"""General utility functions."""

from functools import reduce

import numpy as np


def matrix_2_abc(Lattice: np.ndarray) -> (float, float, float, float, float, float):
    """
    Extract lattice parameters and vectors from a 3x3 matrix representing a lattice.

    Parameters:
        Lattice (np.ndarray): 3x3 matrix representing the lattice.

    Returns:
        tuple: A tuple containing the lattice parameters a, b, c and lattice vectors a_vec, b_vec, c_vec.

    Example:
        >>> Lattice = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
        >>> a, b, c, a_vec, b_vec, c_vec = matrix_2_abc(Lattice)
        >>> print("Lattice parameters:", a, b, c)
        >>> print("Lattice vectors:")
        >>> print(a_vec)
        >>> print(b_vec)
        >>> print(c_vec)
    """
    a = np.sqrt(Lattice[0,0]**2+Lattice[0,1]**2+Lattice[0,2]**2)
    b = np.sqrt(Lattice[1,0]**2+Lattice[1,1]**2+Lattice[1,2]**2)
    c = np.sqrt(Lattice[2,0]**2+Lattice[2,1]**2+Lattice[2,2]**2)

    a_vec = Lattice[0,:]
    b_vec = Lattice[1,:]
    c_vec = Lattice[2,:]

    return a,b,c,a_vec,b_vec,c_vec


def vector_2_abscissa(vector:list, magnitude: float, dx: float, dy: float, dz: float) -> np.ndarray:
    """
    Convert a 3D vector to an array of abscissa values.

    Parameters:
        vector (list): 3D vector represented as (x, y, z).

        magnitude (float): Magnitude of the vector.

        dx (float): Spacing along the x-axis.

        dy (float): Spacing along the y-axis.

        dz (float): Spacing along the z-axis.

    Returns:
        np.ndarray: 1D array containing abscissa values based on the vector and spacing.

    Example:
        >>> vector = (1, 2, 3)
        >>> magnitude = 5.0
        >>> dx, dy, dz = 0.1, 0.2, 0.3
        >>> abscissa_array = vector_2_abscissa(vector, magnitude, dx, dy, dz)
        >>> print("Abscissa Array:")
        >>> print(abscissa_array)
        
    """
    vec_mag = np.linalg.norm([vector[0] * dx, vector[1] * dy, vector[2] * dz])
    abscissa = [i * vec_mag for i in range(magnitude)]

    return np.asarray(abscissa)


def GCD(a: int,b: int) -> int:
    """
    Compute the Greatest Common Divisor (GCD) of two integers a and b.

    Parameters:
        a (int): First integer.
        
        b (int): Second integer.

    Returns:
        int: The Greatest Common Divisor of a and b.
    
    Example:
        >>> a = 36
        >>> b = 48
        >>> gcd = GCD(a, b)
        >>> print("GCD of", a, "and", b, "is:", gcd)
    """
    a = abs(a)
    b = abs(b)
    while a:
        a, b = (b % a), a
    return b


def GCD_List(list: list) -> int:
    """
    Compute the Greatest Common Divisor (GCD) of a list of integers.

    Parameters:
        list (list): List of integers.

    Returns:
        int: The Greatest Common Divisor of the elements in the list.
    
    Example:
        >>> numbers = [24, 36, 60]
        >>> gcd = GCD_List(numbers)
        >>> print("GCD of", numbers, "is:", gcd)
    """
    return reduce(GCD, list)