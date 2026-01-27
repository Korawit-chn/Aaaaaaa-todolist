"""
Simple Python Calculator Program
Supports basic arithmetic operations: add, subtract, multiply, and divide.
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


def calculate_velocity(distance: float, time: float) -> float:
    """Calculate velocity given distance and time. Raises ValueError if time is not greater than zero."""
    if time <= 0:
        raise ValueError("Time must be greater than zero")
    return distance / time


def display_menu():
    """Display the calculator menu."""
    print("\n" + "=" * 40)
    print("Simple Calculator")
    print("=" * 40)
    print("[1] Add")
    print("[2] Subtract")
    print("[3] Multiply")
    print("[4] Divide")
    print("[5] Exit")
    print("=" * 40)


def main():
    """Main function to run the calculator."""
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "5":
            print("\nThank you for using the calculator. Goodbye!")
            break

        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == "1":
                result = add(num1, num2)
                print(f"\nResult: {num1} + {num2} = {result}")
            elif choice == "2":
                result = subtract(num1, num2)
                print(f"\nResult: {num1} - {num2} = {result}")
            elif choice == "3":
                result = multiply(num1, num2)
                print(f"\nResult: {num1} × {num2} = {result}")
            elif choice == "4":
                result = divide(num1, num2)
                print(f"\nResult: {num1} ÷ {num2} = {result}")

        except ValueError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()
