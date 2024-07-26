from pprint import pprint

from sqlalchemy import desc, func

from connect import session
from models import Grade, Student


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
        .query(Student.name,
               func.round(func.avg(Grade.value), 1).label('grade'))
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc('grade'))
        .limit(5)
        .all()
    )


def main() -> None:
    pprint(select_1())


if __name__ == '__main__':
    main()
