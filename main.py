from sqlalchemy import CHAR, create_engine, ForeignKey, SmallInteger, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(CHAR(5), unique=True)


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))


class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))


class Grades(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column(SmallInteger)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'))


def main() -> None:
    engine = create_engine('sqlite:///db.sqlite', echo=True)

    Base.metadata.create_all(engine)
    Base.metadata.bind = engine


if __name__ == '__main__':
    main()
