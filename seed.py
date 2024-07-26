from random import randint
from re import sub

from faker import Faker

from connect import session

# Each model should be imported to use them from global definitions.
from models import Grade, Group, Student, Subject, Teacher

STUDENTS = randint(30, 50)
SUBJECTS = randint(5, 8)

fake = Faker()


def grades() -> list[tuple]:
    results = []

    for student in range(1, STUDENTS + 1):
        for _ in range(randint(0, 20)):
            results.append({'value': randint(0, 100),
                            'student_id': student,
                            'subject_id': randint(1, SUBJECTS)})

    return results


TABLES = {
    'groups': {
        'value': lambda: '{}-{}{}'.format(
            # Two-letter abbreviation of the name of the specialty.
            sub(r'[^A-Z]', '', fake.name())[:2],
            # Academic year number.
            randint(1, 5),
            # Serial number of the group of students in the educational stream.
            randint(1, 3)
        ),
        'rows': 3
    },
    'students': {
        'relations': ('groups',),
        'rows': STUDENTS
    },
    'teachers': {
        'rows': randint(3, 5)
    },
    'subjects': {
        'relations': ('teachers',),
        'value': lambda: fake.job(),
        'rows': SUBJECTS
    },
    'grades': {
        'relations': ('students', 'subjects'),
        'column': 'value',
        'rows': grades
    }
}


def fill(session, name: str) -> None:
    table = TABLES[name]

    if isinstance(table['rows'], int):
        column = table.get('column', 'name')
        relations = table.get('relations', ())

        sequence = [
            {
                column: table.get('value', fake.name)(),
                **{f'{relation[:-1]}_id': randint(1, TABLES[relation]['rows'])
                   for relation in relations}
            }
            for _ in range(table['rows'])
        ]
    else:
        sequence = table['rows']()

    cls = globals()[name[:-1].title()]

    [session.add(cls(**values)) for values in sequence]

    session.commit()


def main() -> None:
    [fill(session, name) for name in TABLES.keys()]
    session.close()


if __name__ == '__main__':
    main()
