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

def calculate_velocity(distance: float, time: float) -> float:
    if time <= 0:
        raise ValueError("Time must be greater than zero")
    return distance / time

def main():
    while True:
        print("Simple Calculator")
        print("Operations: add, subtract, multiply, divide, velocity")
        op = input("Enter operation: ").strip().lower()
        if op not in ['add', 'subtract', 'multiply', 'divide', 'velocity']:
            print("Invalid operation")
            continue
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
        except ValueError:
            print("Invalid number")
            continue
        if op == 'add':
            result = add(a, b)
        elif op == 'subtract':
            result = subtract(a, b)
        elif op == 'multiply':
            result = multiply(a, b)
        elif op == 'divide':
            result = divide(a, b)
        elif op == 'velocity':
            try:
                result = calculate_velocity(a, b)
            except ValueError as e:
                print(e)
                continue
        print(f"Result: {result}")
        again = input("Do another calculation? (y/n): ").strip().lower()
        if again != 'y':
            break

if __name__ == "__main__":
    main()