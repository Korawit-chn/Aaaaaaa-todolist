def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

def main():
    print("Simple Calculator")
    print("Operations: +, -, *, /")
    print("Type 'quit' to exit")

    while True:
        try:
            expression = input("Enter expression (e.g., 2 + 3): ").strip()
            if expression.lower() == 'quit':
                break

            parts = expression.split()
            if len(parts) != 3:
                print("Invalid format. Use: number operator number")
                continue

            num1 = float(parts[0])
            op = parts[1]
            num2 = float(parts[2])

            if op == '+':
                result = add(num1, num2)
            elif op == '-':
                result = subtract(num1, num2)
            elif op == '*':
                result = multiply(num1, num2)
            elif op == '/':
                result = divide(num1, num2)
            else:
                print("Invalid operator. Use +, -, *, /")
                continue

            print(f"Result: {result}")

        except ValueError:
            print("Invalid input. Please enter numbers.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
