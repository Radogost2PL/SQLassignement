from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, URL, Integer, DateTime, Boolean, String, Float, ForeignKey, event, false, Table, \
    Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DATABASE_PATH = Path(__file__).resolve().parent / "experiments.db"

engine = create_engine(
    URL.create("sqlite", database=str(DATABASE_PATH)),
    echo=False,
)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Base(DeclarativeBase):
    pass

subject_experiment = Table(
    "subject_experiment",
    Base.metadata,
    Column("subject_id", ForeignKey("Subject.id"), primary_key=True),
    Column("experiment_id", ForeignKey("Experiment.id"), primary_key=True),
)

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


    data_points: Mapped[list["DataPoint"]] = relationship(
        back_populates="experiment",
        cascade="all, delete-orphan",
    )

    subjects: Mapped[list["Subject"]] = relationship(
        secondary=subject_experiment,
        back_populates="experiments",
    )

class DataPoint(Base):
    __tablename__ = "DataPoint"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    experiment_id: Mapped[int] = mapped_column(
        ForeignKey("Experiment.id"),
        nullable=False,
    )

    experiment: Mapped["Experiment"] = relationship(
        back_populates="data_points"
    )


class Subject(Base):
    __tablename__ = "Subject"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gdpr_accepted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=false(),
    )

    experiments: Mapped[list["Experiment"]] = relationship(
        secondary=subject_experiment,
        back_populates="subjects",
    )