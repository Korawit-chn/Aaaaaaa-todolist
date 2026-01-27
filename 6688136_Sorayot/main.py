"""
Interactive command-line interface for the simple calculator.
"""

from calculator import calculate


def main():
    """Run the interactive calculator."""
    print("=" * 50)
    print("Simple Calculator")
    print("=" * 50)
    print("\nOperations available:")
    print("  +  : Add")
    print("  -  : Subtract")
    print("  *  : Multiply")
    print("  /  : Divide")
    print("\nType 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("Enter operation (or 'quit'): ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            
            # Parse input: "number1 operation number2"
            parts = user_input.split()
            
            if len(parts) != 3:
                print("Invalid format. Use: 'number1 operation number2'")
                print("Example: 5 + 3\n")
                continue
            
            try:
                num1 = float(parts[0])
                operation = parts[1]
                num2 = float(parts[2])
            except ValueError:
                print("Error: Please enter valid numbers\n")
                continue
            
            result = calculate(operation, num1, num2)
            print(f"Result: {num1} {operation} {num2} = {result}\n")
        
        except ValueError as e:
            print(f"Error: {e}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}\n")


if __name__ == "__main__":
    main()
