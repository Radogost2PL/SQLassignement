import random
from datetime import datetime

from sqlalchemy import delete, select, func
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from SQL_Relations.RelationAlchemyTest import Experiment, DataPoint


class ExperimentServiceRelations:
    def __init__(self, engine: Engine):
        self.engine = engine

    def add_data(self) -> list[int]:
        """Dodaje 2 eksperymenty, każdy z 10 punktami danych (razem 20)."""
        with Session(self.engine) as session:
            experiments = []

            for number in range(1, 3):
                experiment = Experiment(
                    title=f"Eksperyment {number}",
                    created_at=datetime.now(),
                    type=random.randint(1, 3),
                    finished=False,
                )

                for _ in range(10):
                    experiment.data_points.append(
                        DataPoint(
                            real_value=round(random.uniform(0, 100), 2),
                            target_value=round(random.uniform(0, 100), 2),
                        )
                    )

                experiments.append(experiment)

            session.add_all(experiments)
            session.flush()

            experiment_ids = [item.id for item in experiments]
            session.commit()

        print("Dodano 2 eksperymenty i 20 punktów danych (po 10 na eksperyment).")
        return experiment_ids

    def show_added_data(self, experiment_ids: list[int]) -> None:
        with Session(self.engine) as session:
            experiments = session.scalars(
                select(Experiment)
                .where(Experiment.id.in_(experiment_ids))
                .order_by(Experiment.id)
            ).all()

            for experiment in experiments:
                print(
                    f"\nEksperyment id={experiment.id}, "
                    f"title={experiment.title!r}, "
                    f"type={experiment.type}, "
                    f"finished={experiment.finished}, "
                    f"liczba punktów={len(experiment.data_points)}"
                )

                for point in experiment.data_points:
                    print(
                        f"   DataPoint id={point.id}, "
                        f"experiment_id={point.experiment_id}, "
                        f"real={point.real_value}, "
                        f"target={point.target_value}"
                    )

    def finish_all_experiments(self) -> None:
        with Session(self.engine) as session:
            experiments = session.scalars(select(Experiment)).all()

            for experiment in experiments:
                experiment.finished = True

            session.commit()

        print("\nUstawiono finished=True dla wszystkich eksperymentów.")

    def show_aggregates(self) -> None:
        """Agregacja danych ćwiczenie 5. Wyświetla sumę i średnia punktów danych dla każdego ekspermentu."""
        print("\n--- START - Agregacje dla eksperymentów ---")
        with Session(self.engine) as session:
            statement = (
                select(
                    Experiment.id,
                    Experiment.title,
                    func.count(DataPoint.id).label("points_count"),
                    func.sum(DataPoint.real_value).label("real_sum"),
                    func.avg(DataPoint.real_value).label("real_avg"),
                    func.sum(DataPoint.target_value).label("target_sum"),
                    func.avg(DataPoint.target_value).label("target_avg"),
                )
                .join(DataPoint, DataPoint.experiment_id == Experiment.id)
                .group_by(Experiment.id, Experiment.title)
                .order_by(Experiment.id)
            )

            rows = session.execute(statement).all()

        print("\n--- Agregacje dla eksperymentów ---")

        for row in rows:
            print(
                f"Eksperyment id={row.id}, title={row.title!r}, "
                f"liczba punktów={row.points_count}\n"
                f"   real_value:   suma={row.real_sum:.2f}, "
                f"średnia={row.real_avg:.2f}\n"
                f"   target_value: suma={row.target_sum:.2f}, "
                f"średnia={row.target_avg:.2f}"
            )

        print("--- KONIEC - Agregacje dla eksperymentów ---\n")

    def delete_all_data(self) -> None:
        """Najpierw usuwa rekordy podrzędne, potem eksperymenty."""
        with Session(self.engine) as session:
            session.execute(delete(DataPoint))
            session.execute(delete(Experiment))
            session.commit()

        print("\nUsunięto wszystkie rekordy z obu tabel.")

    def run(self) -> None:
        experiment_ids = self.add_data()
        self.show_added_data(experiment_ids)
        self.finish_all_experiments()
        self.show_aggregates()
        self.delete_all_data()