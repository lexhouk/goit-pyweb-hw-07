from pprint import pprint
from re import search

from argparse import ArgumentParser

from connect import session
from seed import TABLES
from models import Grade, Group, Student, Subject, Teacher


def create_action() -> None:
    ...


def list_action(model: str) -> list:
    match model:
        case 'Grade':
            query = (
                session
                .query(Grade.id, Student.name, Subject.name, Grade.value)
                .select_from(Grade)
                .join(Subject)
                .join(Student)
                .order_by(Student.name)
                .order_by(Subject.name)
            )

        case 'Group':
            query = session.query(Group.id, Group.name).order_by(Group.name)

        case 'Student':
            query = (
                session
                .query(Student.id, Student.name, Group.name)
                .join(Group)
                .order_by(Student.name)
            )

        case 'Subject':
            query = (
                session
                .query(Subject.id, Subject.name, Teacher.name)
                .join(Teacher)
                .order_by(Subject.name)
            )

        case 'Teacher':
            query = session.query(Teacher.id, Teacher.name) \
                .order_by(Teacher.name)

    return query.all()


def update_action() -> None:
    ...


def remove_action() -> None:
    ...


def main() -> None:
    parser = ArgumentParser('CRUD')

    parser.add_argument('-a',
                        '--action',
                        choices=[data.group(1) for name in globals()
                                 if (data := search(r'^(.+)_action$', name))],
                        required=True)

    parser.add_argument('-m',
                        '--model',
                        choices=[name[:-1].title() for name in TABLES.keys()],
                        required=True)

    parser.add_argument('-n', '--name')
    parser.add_argument('-i', '--id', type=int)

    arguments = vars(parser.parse_args())

    pprint(globals()[arguments['action'] + '_action'](arguments['model']))

    session.close()


if __name__ == '__main__':
    main()
