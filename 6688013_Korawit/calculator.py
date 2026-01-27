"""
A simple calculator module that supports basic arithmetic operations:
addition, subtraction, multiplication, and division.
"""


def add(a, b):
    """Add two numbers and return the result."""
    return a + b


def subtract(a, b):
    """Subtract b from a and return the result."""
    return a - b


def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b


def divide(a, b):
    """Divide a by b and return the result."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def calculate_velocity(distance: float, time: float) -> float:
    if time <= 0:
        raise ValueError("Time must be greater than zero")
    return distance / time


def main():
    """Main function to run the calculator in interactive mode."""
    print("=" * 50)
    print("         Simple Calculator")
    print("=" * 50)
    print("\nAvailable operations:")
    print("  1. Add (+)")
    print("  2. Subtract (-)")
    print("  3. Multiply (*)")
    print("  4. Divide (/)")
    print("  5. Exit")
    print()

    while True:
        try:
            choice = input("\nEnter operation (1/2/3/4/5): ").strip()

            if choice == "5":
                print("\nThank you for using the calculator. Goodbye!")
                break

            if choice not in ["1", "2", "3", "4"]:
                print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                continue

            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == "1":
                result = add(num1, num2)
                print(f"\n{num1} + {num2} = {result}")
            elif choice == "2":
                result = subtract(num1, num2)
                print(f"\n{num1} - {num2} = {result}")
            elif choice == "3":
                result = multiply(num1, num2)
                print(f"\n{num1} * {num2} = {result}")
            elif choice == "4":
                result = divide(num1, num2)
                print(f"\n{num1} / {num2} = {result}")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Invalid input. Please enter valid numbers. Error: {e}")


if __name__ == "__main__":
    main()
