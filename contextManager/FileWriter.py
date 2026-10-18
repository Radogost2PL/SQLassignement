class FileWriter:
    def __init__(self, path):
        self.path = path
        self.file = None

    def __enter__(self):
        self.file = open(self.path, "w", encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()          # zamkniicie pliku zawsze
        if exc_type is not None:
            print(f"Błąd podczas zapisu: {exc_value}")
        return False                   # wyjątek nie jest tłumiony


# # Test zapisu
# with FileWriter("../test.txt") as f:
#     f.write("Witaj, świecie!\n")
#
# # Test z wyjtkiem (program zostanie przerwany, try, żeby zobaczyć efekt)
# try:
#     with FileWriter("../test.txt") as f:
#         f.write("Dane\n")
#         raise ValueError("coś poszło nie tak")
# except ValueError as e:
#     print("Wyjątek został przepuszczony dalej:", e)