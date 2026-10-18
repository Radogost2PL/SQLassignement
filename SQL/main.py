from SQL.AlchemyTest import create_database, engine
from SQL.ExperimentService import ExperimentService


def main() -> None:
    create_database()
    service = ExperimentService(engine)
    service.run()


if __name__ == "__main__":
    main()