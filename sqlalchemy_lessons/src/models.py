import datetime
import enum
from typing import Annotated, Optional

from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Кастомный тип данных
intpk = Annotated[int, mapped_column(primary_key=True)]
created_at_ct = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at_ct = Annotated[
    datetime.datetime,
    mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.timezone.utc),
]
str_256 = Annotated[str, 256]


# КЛАССЫ
class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}

    def __repr__(self):
        cols = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"<{self.__class__.__name__} {','.join(cols)}>"


class WorkLoad(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str]

    resumes: Mapped[list["ResumeOrm"]] = relationship()


class ResumeOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[Optional[int]]
    workload: Mapped[WorkLoad]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    # server_default - данные на уровне СУБД | default - данные на уровне приложения python
    created_at: Mapped[created_at_ct]
    updated_at: Mapped[updated_at_ct]

    worker: Mapped["WorkersOrm"] = relationship()


# Тут будет храниться информация о всех созданных таблицах на стороне приложения
metadata_obj = MetaData()
workers_table = Table("workers", metadata_obj, Column("id", Integer, primary_key=True), Column("username", String(20)))
