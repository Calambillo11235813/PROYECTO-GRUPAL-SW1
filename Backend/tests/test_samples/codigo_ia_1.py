"""
Module for calculating statistical measures.

This module provides functions to calculate various statistical measures
including mean, median, mode, and standard deviation for a given dataset.

Functions:
    calculate_mean(numbers: List[float]) -> float
    calculate_median(numbers: List[float]) -> float
    calculate_mode(numbers: List[float]) -> float
    calculate_standard_deviation(numbers: List[float]) -> float

Example:
    >>> data = [1, 2, 3, 4, 5]
    >>> calculate_mean(data)
    3.0
"""

from typing import List
import math
from collections import Counter


def calculate_mean(numbers: List[float]) -> float:
    """
    Calculate the arithmetic mean of a list of numbers.

    Args:
        numbers: A list of numerical values.

    Returns:
        The arithmetic mean as a float.

    Raises:
        ValueError: If the input list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate mean of an empty list")
    
    return sum(numbers) / len(numbers)


def calculate_median(numbers: List[float]) -> float:
    """
    Calculate the median value of a list of numbers.

    Args:
        numbers: A list of numerical values.

    Returns:
        The median value as a float.

    Raises:
        ValueError: If the input list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate median of an empty list")
    
    sorted_numbers = sorted(numbers)
    length = len(sorted_numbers)
    middle = length // 2
    
    if length % 2 == 0:
        return (sorted_numbers[middle - 1] + sorted_numbers[middle]) / 2
    else:
        return sorted_numbers[middle]


def calculate_mode(numbers: List[float]) -> float:
    """
    Calculate the mode (most frequent value) of a list of numbers.

    Args:
        numbers: A list of numerical values.

    Returns:
        The mode value as a float.

    Raises:
        ValueError: If the input list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate mode of an empty list")
    
    counter = Counter(numbers)
    mode_value = counter.most_common(1)[0][0]
    
    return mode_value


def calculate_standard_deviation(numbers: List[float]) -> float:
    """
    Calculate the standard deviation of a list of numbers.

    Args:
        numbers: A list of numerical values.

    Returns:
        The standard deviation as a float.

    Raises:
        ValueError: If the input list is empty or has only one element.
    """
    if not numbers:
        raise ValueError("Cannot calculate standard deviation of an empty list")
    
    if len(numbers) == 1:
        raise ValueError("Cannot calculate standard deviation with only one value")
    
    mean = calculate_mean(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / (len(numbers) - 1)
    
    return math.sqrt(variance)
