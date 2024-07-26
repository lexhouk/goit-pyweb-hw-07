from sqlalchemy import CHAR, ForeignKey, SmallInteger, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, \
    MappedColumn

Base = declarative_base()


class Column:
    @staticmethod
    def primary() -> MappedColumn:
        return mapped_column(primary_key=True)

    @staticmethod
    def foreign(name: str) -> MappedColumn:
        return mapped_column(ForeignKey(name + 's.id',
                                        ondelete='CASCADE',
                                        onupdate='CASCADE'))

    @staticmethod
    def data(size: int = 100, fixed: bool = False) -> MappedColumn:
        return mapped_column(CHAR(size) if fixed else String(size),
                             nullable=False,
                             unique=True)


class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = Column.primary()
    name: Mapped[str] = Column.data(5, True)


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = Column.primary()
    name: Mapped[str] = Column.data()
    group_id: Mapped[int] = Column.foreign('group')


class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = Column.primary()
    name: Mapped[str] = Column.data()


class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = Column.primary()
    name: Mapped[str] = Column.data()
    teacher_id: Mapped[int] = Column.foreign('teacher')


class Grades(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = Column.primary()
    value: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    student_id: Mapped[int] = Column.foreign('student')
    subject_id: Mapped[int] = Column.foreign('subject')
