import random
from datetime import datetime

from sqlalchemy import delete, select, update
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from SQL.AlchemyTest import Experiment, DataPoint


class ExperimentService:
    def __init__(self, engine: Engine):
        self.engine = engine

    def add_data(self) -> tuple[list[int], list[int]]:
        """tworzy i Dodaje do DB 2 eksperymenty i 10 punktów danych."""
        with Session(self.engine) as session:
            experiments = [
                Experiment(
                    title=f"Eksperyment {number}",
                    created_at=datetime.now(),
                    type=random.randint(1, 3),
                    finished=False,
                )
                for number in range(0, 2)
            ]

            data_points = [
                DataPoint(
                    real_value=round(random.uniform(0, 100), 2),
                    target_value=round(random.uniform(0, 100), 2),
                )
                for _ in range(10)
            ]

            session.add_all(experiments)
            session.add_all(data_points)

            # Wysyła INSERT-y do bazy, aby uzyskać nadane identyfikatory.
            session.flush()

            experiment_ids = [item.id for item in experiments]
            data_point_ids = [item.id for item in data_points]

            session.commit()

        print("Dodano 2 eksperymenty i 10 punktów danych.")
        return experiment_ids, data_point_ids

    def show_added_data(
        self,
        experiment_ids: list[int],
        data_point_ids: list[int],
    ) -> None:
        """Pobiera z bazy i wyświetla tylko przed chwilą dodane dane."""
        with Session(self.engine) as session:
            experiments = session.scalars(
                select(Experiment)
                .where(Experiment.id.in_(experiment_ids))
                .order_by(Experiment.id)
            ).all()

            data_points = session.scalars(
                select(DataPoint)
                .where(DataPoint.id.in_(data_point_ids))
                .order_by(DataPoint.id)
            ).all()

            print("\n--- Dodane eksperymenty ---")

            for experiment in experiments:
                print(
                    f"id={experiment.id}, "
                    f"title={experiment.title!r}, "
                    f"created_at={experiment.created_at}, "
                    f"type={experiment.type}, "
                    f"finished={experiment.finished}"
                )

            print("\n--- Dodane punkty danych ---")

            for point in data_points:
                print(
                    f"id={point.id}, "
                    f"real_value={point.real_value}, "
                    f"target_value={point.target_value}"
                )

    def finish_all_experiments(self) -> None:
        """Ustawia finished=True we wszystkichj eksperymentach."""
        with Session(self.engine) as session:
            session.execute(
                update(Experiment).values(finished=True)
            )
            session.commit()

        print("\nUstawiono finished=True dla wszystkich eksperymentów.")

    def delete_all_data(self) -> None:
        """Usuwa wszystkie rekordy z obu tabel."""
        with Session(self.engine) as session:
            session.execute(delete(DataPoint))
            session.execute(delete(Experiment))
            session.commit()

        print("\nUsunięto wszystkie rekordy z obu tabel.")

    def run(self) -> None:
        experiment_ids, data_point_ids = self.add_data()
        self.show_added_data(experiment_ids, data_point_ids)
        self.finish_all_experiments()
        self.delete_all_data()