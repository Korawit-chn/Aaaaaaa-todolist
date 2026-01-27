"""
Unit tests for the calculator module.
"""

import pytest
from calculator import add, subtract, multiply, divide, calculate


class TestBasicOperations:
    """Test basic arithmetic operations."""
    
    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0
        assert add(10.5, 2.5) == 13.0
    
    def test_subtract(self):
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5
        assert subtract(-1, -1) == 0
        assert subtract(10.5, 2.5) == 8.0
    
    def test_multiply(self):
        assert multiply(2, 3) == 6
        assert multiply(-2, 3) == -6
        assert multiply(0, 100) == 0
        assert multiply(2.5, 4) == 10.0
    
    def test_divide(self):
        assert divide(6, 2) == 3
        assert divide(10, 4) == 2.5
        assert divide(-8, 2) == -4
    
    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)


class TestCalculateFunction:
    """Test the calculate dispatcher function."""
    
    def test_add_operation(self):
        assert calculate('+', 5, 3) == 8
    
    def test_subtract_operation(self):
        assert calculate('-', 5, 3) == 2
    
    def test_multiply_operation(self):
        assert calculate('*', 5, 3) == 15
    
    def test_divide_operation(self):
        assert calculate('/', 6, 2) == 3
    
    def test_invalid_operation(self):
        with pytest.raises(ValueError, match="Invalid operation"):
            calculate('&', 5, 3)
    
    def test_invalid_operation_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculate('/', 5, 0)


class TestEdgeCases:
    """Test edge cases and special values."""
    
    def test_large_numbers(self):
        assert add(1000000, 2000000) == 3000000
        assert multiply(1000, 1000) == 1000000
    
    def test_negative_numbers(self):
        assert add(-5, -3) == -8
        assert subtract(-5, -3) == -2
        assert multiply(-5, -3) == 15
        assert divide(-6, -2) == 3
    
    def test_floats(self):
        assert abs(add(0.1, 0.2) - 0.3) < 1e-9  # Handle floating point precision
        assert multiply(0.5, 0.5) == 0.25
