from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, URL, Integer, String, DateTime, Boolean, false, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Plik bazy w tym samym pakiecie
DATABASE_PATH = Path(__file__).resolve().parent / "experiments.db"

engine = create_engine(
    URL.create("sqlite", database=str(DATABASE_PATH)),
    echo=True,
)


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    __tablename__ = "Experiment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    type: Mapped[int] = mapped_column(Integer, nullable=False)
    finished: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=false(),
    )


class DataPoint(Base):
    __tablename__ = "DataPoint"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)


def create_database() -> None:
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_database()
    print(f"Baza danych jest gotowa: {DATABASE_PATH}")