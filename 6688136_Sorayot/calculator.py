"""
Simple calculator module that performs basic arithmetic operations.
"""


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract two numbers."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide two numbers. Raises ValueError if dividing by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate(operation, a, b):
    """
    Perform a calculation based on the operation string.
    
    Args:
        operation: A string representing the operation ('+', '-', '*', '/')
        a: First operand
        b: Second operand
    
    Returns:
        The result of the operation
    
    Raises:
        ValueError: If operation is invalid or division by zero
    """
    if operation == '+':
        return add(a, b)
    elif operation == '-':
        return subtract(a, b)
    elif operation == '*':
        return multiply(a, b)
    elif operation == '/':
        return divide(a, b)
    else:
        raise ValueError(f"Invalid operation: {operation}. Use '+', '-', '*', or '/'")
