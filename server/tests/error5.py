# error5.py
# ZeroDivisionError

def divide_numbers(a, b):
    return a / b

if __name__ == "__main__":
    # Division by zero
    result = divide_numbers(10, 0)
    print(f"Result: {result}")
