class SafeDivision:
    def __enter__(self):
        return self

    def divide(self, a, b):
        return a / b

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is ZeroDivisionError:
            print("Nie można dzielić przez zero")
            return True   # tłumi wyjątek
        return False      # inne wyjątki lecą dalej


with SafeDivision() as sd:
    print(sd.divide(10, 2))   # 5.0
    print(sd.divide(5, 0))    # wypisze komunikat, wyjątek stłumiony
print("Program działa dalej")