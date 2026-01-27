# Simple Calculator

A lightweight Python calculator that supports basic arithmetic operations: addition, subtraction, multiplication, and division.

## Files

- **calculator.py**: Core calculator module with functions for each operation
- **main.py**: Interactive command-line interface
- **test_calculator.py**: Comprehensive unit tests

## Usage

### Interactive Mode

Run the calculator interactively:

```bash
python main.py
```

Then enter calculations in the format: `number1 operation number2`

Examples:
```
10 + 5
20 - 3
7 * 8
15 / 3
```

### As a Module

Use it in your Python code:

```python
from calculator import add, subtract, multiply, divide, calculate

result = add(5, 3)           # 8
result = calculate('+', 5, 3)  # 8
result = calculate('/', 10, 2) # 5.0
```

## Operations

- `+` : Addition
- `-` : Subtraction
- `*` : Multiplication
- `/` : Division (raises ValueError if dividing by zero)

## Testing

Run all tests:

```bash
pytest test_calculator.py -v
```

## Features

- Basic arithmetic operations (add, subtract, multiply, divide)
- Division by zero error handling
- Support for both integers and floating-point numbers
- Interactive CLI with user-friendly prompts
- Comprehensive test suite
