from contextManager.MyLogger import MyLogger
from contextManager.FileWriter import FileWriter
from contextManager.SafeDivision import SafeDivision


def main():
    # Zadanie 1 — Logger
    print("--- Logger ---")

    with MyLogger():
        print("Wykonuję kod w sekcji logowania")

    # Zadanie 2 — poprawny zapis
    print("\n--- FileWriter: zapis ---")

    with FileWriter("test.txt") as plik:
        plik.write("Przykładowy tekst\n")

    # Zadanie 3 — zapis z wyjątkiem
    print("\n--- FileWriter: wyjątek ---")

    try:
        with FileWriter("test_blad.txt") as plik:
            plik.write("Tekst przed wystąpieniem błędu\n")
            raise ValueError("Przykładowy błąd zapisu")
    except ValueError as blad:
        print(f"Wyjątek dotarł poza blok with: {blad}")

    # Zadanie 4 — SafeDivision
    print("\n--- SafeDivision ---")

    with SafeDivision() as dzielenie:
        print(dzielenie.divide(10, 2))
        print(dzielenie.divide(10, 0))

    print("Program działa dalej")


if __name__ == "__main__":
    main()
