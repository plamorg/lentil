# error2.py
# NameError: 'x' is not defined

def show_value():
    print(x)  # 'x' was never defined

if __name__ == "__main__":
    show_value()