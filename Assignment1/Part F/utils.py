"""
This module contains utility functions for temperature conversion,
prime number checking, factorial calculation, and Fibonacci sequence generation.
"""

from typing import List

# Constants
FAHRENHEIT_FREEZING_POINT = 32
FAHRENHEIT_CELSIUS_RATIO = 5 / 9

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Convert temperature from Fahrenheit to Celsius.
    
    Args:
        fahrenheit (float): Temperature in Fahrenheit.
    
    Returns:
        float: Temperature in Celsius.

    Raises:
        ValueError: If the input is not a number.
        OverflowError: If the input is too large to be converted.
    """
    try:
        return (float(fahrenheit) - FAHRENHEIT_FREEZING_POINT) * FAHRENHEIT_CELSIUS_RATIO
    except ValueError:
        raise ValueError("Input must be a number")
    except OverflowError:
        raise OverflowError("Input is too large to be converted")

def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convert temperature from Celsius to Fahrenheit.
    
    Args:
        celsius (float): Temperature in Celsius.
    
    Returns:
        float: Temperature in Fahrenheit.

    Raises:
        ValueError: If the input is not a number.
        OverflowError: If the input is too large to be converted.
    """
    try:
        return (float(celsius) / FAHRENHEIT_CELSIUS_RATIO) + FAHRENHEIT_FREEZING_POINT
    except ValueError:
        raise ValueError("Input must be a number")
    except OverflowError:
        raise OverflowError("Input is too large to be converted")

def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    
    Args:
        n (int): The number to check.
    
    Returns:
        bool: True if the number is prime, False otherwise.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    sqrt_n = int(n**0.5) + 1
    for i in range(3, sqrt_n, 2):
        if n % i == 0:
            return False
    return True

def factorial(n: int) -> int:
    """
    Calculate the factorial of a non-negative integer.

    Args:
        n (int): The non-negative integer to calculate the factorial for.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("Factorial must be a non-negative integer.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def fibonacci(n: int) -> List[int]:
    """
    Generate the Fibonacci sequence up to the nth term.

    The Fibonacci sequence is a series of numbers where each number is the sum
    of the two preceding ones. It starts from 0 and 1, and each subsequent
    number is the sum of the previous two.

    Args:
        n (int): The number of terms to generate in the sequence.

    Returns:
        list: A list containing the Fibonacci sequence up to the nth term.
             - For n = 0, returns an empty list []
             - For n = 1, returns [0]
             - For n = 2, returns [0, 1]
             - For n > 2, returns the first n terms of the Fibonacci sequence

    Raises:
        ValueError: If n is negative.

    Examples:
        >>> fibonacci(0)
        []
        >>> fibonacci(1)
        [0]
        >>> fibonacci(2)
        [0, 1]
        >>> fibonacci(5)
        [0, 1, 1, 2, 3]
        >>> fibonacci(10)
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib