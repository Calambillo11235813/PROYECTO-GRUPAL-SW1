"""
List Operations Module

This module provides common list manipulation functions.
"""

def find_max(numbers):
    """
    Find the maximum value in a list.
    
    Args:
        numbers: List of numbers
        
    Returns:
        Maximum value
        
    Raises:
        ValueError: If list is empty
    """
    if not numbers:
        raise ValueError("List cannot be empty")
    
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

def find_min(numbers):
    """
    Find the minimum value in a list.
    
    Args:
        numbers: List of numbers
        
    Returns:
        Minimum value
        
    Raises:
        ValueError: If list is empty
    """
    if not numbers:
        raise ValueError("List cannot be empty")
    
    min_val = numbers[0]
    for num in numbers:
        if num < min_val:
            min_val = num
    return min_val

def calculate_average(numbers):
    """
    Calculate the average of numbers in a list.
    
    Args:
        numbers: List of numbers
        
    Returns:
        Average value
        
    Raises:
        ValueError: If list is empty
    """
    if not numbers:
        raise ValueError("List cannot be empty")
    
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

def remove_duplicates_from_list(items):
    """
    Remove duplicate items from a list.
    
    Args:
        items: Input list
        
    Returns:
        List without duplicates
    """
    result = []
    seen = set()
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result

def merge_sorted_lists(list1, list2):
    """
    Merge two sorted lists into one sorted list.
    
    Args:
        list1: First sorted list
        list2: Second sorted list
        
    Returns:
        Merged sorted list
    """
    result = []
    i = 0
    j = 0
    
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    
    while i < len(list1):
        result.append(list1[i])
        i += 1
    
    while j < len(list2):
        result.append(list2[j])
        j += 1
    
    return result
