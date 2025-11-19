"""
String Utilities Module

This module contains utility functions for string manipulation.
"""

def reverse_string(s):
    """
    Reverse a string.
    
    Args:
        s: Input string
        
    Returns:
        Reversed string
    """
    return s[::-1]

def is_palindrome(s):
    """
    Check if a string is a palindrome.
    
    Args:
        s: Input string
        
    Returns:
        True if palindrome, False otherwise
    """
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def count_vowels(s):
    """
    Count the number of vowels in a string.
    
    Args:
        s: Input string
        
    Returns:
        Number of vowels
    """
    vowels = "aeiouAEIOU"
    count = 0
    for char in s:
        if char in vowels:
            count += 1
    return count

def capitalize_words(s):
    """
    Capitalize the first letter of each word.
    
    Args:
        s: Input string
        
    Returns:
        String with capitalized words
    """
    return " ".join(word.capitalize() for word in s.split())

def remove_duplicates(s):
    """
    Remove duplicate characters from string.
    
    Args:
        s: Input string
        
    Returns:
        String without duplicates
    """
    result = ""
    seen = set()
    for char in s:
        if char not in seen:
            result += char
            seen.add(char)
    return result
