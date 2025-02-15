# error7.py
# TypeError: Can't concatenate int to str directly

def combine_text_and_number(text, number):
    return text + number  # This will cause a TypeError when number is int

if __name__ == "__main__":
    result = combine_text_and_number("The answer is: ", 42)
    print(result)
