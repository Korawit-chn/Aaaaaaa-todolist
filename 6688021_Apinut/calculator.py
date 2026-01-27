"""
Simple Calculator
A basic calculator that supports add, subtract, multiply, and divide operations.
"""


class Calculator:
    """A simple calculator class for basic arithmetic operations."""

    def calculate_velocity(distance: float, time: float) -> float:
    if time <= 0:
        raise ValueError("Time must be greater than zero")
    return distance / time

    def add(self, a, b):
        """Add two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            The sum of a and b
        """
        return a + b

    def subtract(self, a, b):
        """Subtract two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            The difference of a and b
        """
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            The product of a and b
        """
        return a * b

    def divide(self, a, b):
        """Divide two numbers.
        
        Args:
            a: First number (dividend)
            b: Second number (divisor)
            
        Returns:
            The quotient of a divided by b
            
        Raises:
            ValueError: If attempting to divide by zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


def main():
    """Main function to run the calculator in interactive mode."""
    calc = Calculator()
    
    print("=" * 50)
    print("Simple Calculator")
    print("=" * 50)
    print("\nAvailable operations:")
    print("1. Add (add)")
    print("2. Subtract (subtract)")
    print("3. Multiply (multiply)")
    print("4. Divide (divide)")
    print("5. Exit (exit or quit)")
    print()
    
    while True:
        try:
            operation = input("Enter operation (add/subtract/multiply/divide) or 'exit': ").strip().lower()
            
            if operation in ['exit', 'quit']:
                print("Thank you for using the calculator!")
                break
            
            if operation not in ['add', 'subtract', 'multiply', 'divide']:
                print("Invalid operation. Please try again.\n")
                continue
            
            # Get input numbers
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            # Perform operation
            if operation == 'add':
                result = calc.add(num1, num2)
                print(f"\n{num1} + {num2} = {result}\n")
            elif operation == 'subtract':
                result = calc.subtract(num1, num2)
                print(f"\n{num1} - {num2} = {result}\n")
            elif operation == 'multiply':
                result = calc.multiply(num1, num2)
                print(f"\n{num1} * {num2} = {result}\n")
            elif operation == 'divide':
                result = calc.divide(num1, num2)
                print(f"\n{num1} / {num2} = {result}\n")
                
        except ValueError as e:
            print(f"Error: {e}\n")
        except ValueError:
            print("Invalid input. Please enter valid numbers.\n")


if __name__ == "__main__":
    main()
