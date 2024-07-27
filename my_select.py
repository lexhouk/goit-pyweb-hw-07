from pprint import pprint
from re import search

from sqlalchemy import and_, desc, func

from connect import session
from models import Grade, Group, Student, Subject, Teacher


def grade(label: bool = False):
    column = func.round(func.avg(Grade.value), 1)

    if label:
        column = column.label('grade')

    return column


def select_1():
    '''
    SELECT s.name, ROUND(AVG(g.value), 1) as grade
    FROM grades g
    JOIN students s ON g.student_id = s.id
    GROUP BY g.student_id
    ORDER BY grade DESC
    LIMIT 5;
    '''
    return (
        session
        .query(Student.name, grade(True))
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc('grade'))
        .limit(5)
    )


def select_2(subject: int = 1):
    '''
    SELECT d.name, s.name, ROUND(AVG(g.value), 1) as grade
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN subjects d ON g.subject_id = d.id
    WHERE d.id = 1
    ORDER BY grade DESC
    LIMIT 1;
    '''
    return (
        session
        .query(Subject.name, Student.name, grade(True))
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .filter(Subject.id == subject)
        .group_by(Subject.id)
        .group_by(Student.id)
        .order_by(desc('grade'))
        .limit(1)
    )


def select_3(subject: int = 1):
    '''
    SELECT d.name, g.name, ROUND(AVG(m.value), 1)
    FROM groups g
    JOIN students s ON g.id = s.group_id
    JOIN grades m ON s.id = m.student_id
    JOIN subjects d ON d.id = m.subject_id
    WHERE d.id = 1
    GROUP BY g.id;
    '''
    return (
        session
        .query(Subject.name, Group.name, grade())
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .join(Subject)
        .filter(Subject.id == subject)
        .group_by(Subject.id)
        .group_by(Group.id)
    )


def select_4():
    '''
    SELECT ROUND(AVG(value), 1)
    FROM grades;
    '''
    return session.query(grade())


def select_5(teacher: int = 5):
    '''
    SELECT t.name, s.name
    FROM teachers t
    JOIN subjects s ON s.teacher_id = t.id
    WHERE t.id = 5;
    '''
    return (
        session
        .query(Teacher.name, Subject.name)
        .select_from(Teacher)
        .join(Subject)
        .filter(Teacher.id == teacher)
    )


def select_6(group: int = 1):
    '''
    SELECT g.name, s.name
    FROM groups g
    JOIN students s ON s.group_id = g.id
    WHERE g.id = 1
    ORDER BY s.name;
    '''
    return (
        session
        .query(Group.name, Student.name)
        .select_from(Group)
        .join(Student)
        .filter(Group.id == group)
        .order_by(Student.name)
    )


def select_7(subject: int = 1, group: int = 1):
    '''
    SELECT d.name, g.name, s.name, m.value
    FROM groups g
    JOIN students s ON s.group_id = g.id
    JOIN grades m ON m.student_id = s.id
    JOIN subjects d ON d.id = m.subject_id
    WHERE d.id = 1 AND g.id = 1
    ORDER BY s.name;
    '''
    return (
        session
        .query(Subject.name, Group.name, Student.name, Grade.value)
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .join(Subject)
        .filter(and_(Subject.id == subject, Group.id == group))
        .order_by(Student.name)
    )


def select_8(teacher: int = 5):
    '''
    SELECT t.name, s.name, ROUND(AVG(g.value), 1)
    FROM teachers t
    JOIN subjects s ON s.teacher_id = t.id
    JOIN grades g ON g.subject_id = s.id
    WHERE t.id = 5
    GROUP BY s.id
    ORDER BY s.name;
    '''
    return (
        session
        .query(Teacher.name, Subject.name, grade())
        .select_from(Teacher)
        .join(Subject)
        .join(Grade)
        .filter(Teacher.id == teacher)
        .group_by(Teacher.id)
        .group_by(Subject.id)
        .order_by(Subject.name)
    )


def select_9(student: int = 1):
    '''
    SELECT s.name, d.name
    FROM students s
    JOIN grades g ON g.student_id = s.id
    JOIN subjects d ON d.id = g.subject_id
    WHERE s.id = 1
    GROUP BY d.id
    ORDER BY d.name;
    '''
    return (
        session
        .query(Student.name, Subject.name)
        .select_from(Student)
        .join(Grade)
        .join(Subject)
        .filter(Student.id == student)
        .group_by(Student.id)
        .group_by(Subject.id)
        .order_by(Subject.name)
    )


def select_10(teacher: int = 5, student: int = 2):
    '''
    SELECT t.name, s.name, d.name
    FROM teachers t
    JOIN subjects d ON d.teacher_id = t.id
    JOIN grades g ON g.subject_id = d.id
    JOIN students s ON s.id = g.student_id
    WHERE t.id = 5 AND s.id = 2
    GROUP BY d.id
    ORDER BY d.name;
    '''
    return (
        session
        .query(Teacher.name, Student.name, Subject.name)
        .select_from(Teacher)
        .join(Subject)
        .join(Grade)
        .join(Student)
        .filter(and_(Teacher.id == teacher, Student.id == student))
        .group_by(Teacher.id)
        .group_by(Student.id)
        .group_by(Subject.id)
        .order_by(Subject.name)
    )


def main() -> None:
    ids = [int(result.group(1))
           for name in globals().keys()
           if (result := search(r'^select_(\d+)$', name))]

    for id in sorted(ids):
        print(f' Task #{id} '.center(80, '-'))
        pprint(globals()[f'select_{id}']().all())


if __name__ == '__main__':
    main()
