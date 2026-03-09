import datetime
import enum
from typing import Annotated, Optional

from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    text,
)
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

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relathionships не используются в repr(), т.к. могут привести к неожиданным подгрузкам"""

        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {','.join(cols)}>"


class WorkLoad(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str]

    resumes: Mapped[list["ResumeOrm"]] = relationship(back_populates="worker")  # backref="worker" устаревший параметр

    resumes_parttime: Mapped[list["ResumeOrm"]] = relationship(
        back_populates="worker",
        primaryjoin="and_(WorkersOrm.id == ResumeOrm.worker_id, ResumeOrm.workload =='parttime')",
        order_by="ResumeOrm.id.desc()",
        lazy="selectin",
    )


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

    worker: Mapped["WorkersOrm"] = relationship(back_populates="resumes")

    repr_cols_num = 4
    repr_cols = ("created_at",)

    __table_args__ = (
        # Primary keys можно создать также тут, но рекомендуется возле поля
        Index(
            "title_index",
            "title",
        ),
        CheckConstraint("compensation > 0", name="check_compensation_positive"),
    )


# Тут будет храниться информация о всех созданных таблицах на стороне приложения
metadata_obj = MetaData()
workers_table = Table("workers", metadata_obj, Column("id", Integer, primary_key=True), Column("username", String(20)))
