"""
Calculator Module

This module provides basic arithmetic operations.
"""

def add(a, b):
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b

def subtract(a, b):
    """
    Subtract b from a.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Difference of a and b
    """
    return a - b

def multiply(a, b):
    """
    Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product of a and b
    """
    return a * b

def divide(a, b):
    """
    Divide a by b.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Quotient of a divided by b
        
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a, b):
    """
    Raise a to the power of b.
    
    Args:
        a: Base number
        b: Exponent
        
    Returns:
        a raised to the power of b
    """
    return a ** b

def main():
    """
    Main function to demonstrate calculator usage.
    """
    print("Calculator Demo")
    print(f"2 + 3 = {add(2, 3)}")
    print(f"5 - 2 = {subtract(5, 2)}")
    print(f"4 * 3 = {multiply(4, 3)}")
    print(f"10 / 2 = {divide(10, 2)}")
    print(f"2 ^ 3 = {power(2, 3)}")

if __name__ == "__main__":
    main()
