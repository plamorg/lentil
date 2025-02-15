# no_error3.py
# A script that greets a user with their name

def greet_user(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    user_name = "Alice"
    message = greet_user(user_name)
    print(message)
