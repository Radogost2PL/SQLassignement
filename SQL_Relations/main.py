

from ExperimentServiceRelations import ExperimentServiceRelations
from SQL_Relations.RelationAlchemyTest import create_database, engine


def main() -> None:
    create_database()
    service = ExperimentServiceRelations(engine)
    service.run()


if __name__ == "__main__":
    main()