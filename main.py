from pprint import pprint
from re import search

from argparse import ArgumentParser

from connect import session
from seed import TABLES
from models import Grade, Group, Student, Subject, Teacher


def create_action(**options: dict) -> None:
    model: str = options['model']
    relations = TABLES[model.lower() + 's'].get('relations', ())

    if len(relations) > 1:
        raise ValueError('Unsupported model.')

    name = options['name']
    cls = globals()[model]

    if session.query(cls).filter(eval(f'{model}.name') == name).one_or_none():
        raise ValueError('The name is already used.')

    fields = {'name': name}

    if relations:
        id = options['id']
        relation = relations[0][:-1]
        sub_model = relation.title()
        sub_cls = globals()[sub_model]
        column = eval(f'{sub_model}.id')

        if not session.query(sub_cls).filter(column == id).one_or_none():
            raise ValueError(f'The {relation} is absent.')

        fields[relation + '_id'] = options['id']

    try:
        session.add(cls(**fields))
        session.commit()
    except Exception as error:
        raise error
    else:
        print(f'A new {model.lower()} has been added successfully.')


def list_action(**options: dict) -> None:
    match options['model']:
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

    pprint(query.all())


def update_action(**options: dict) -> None:
    name = options['name']
    id = options['id']
    model: str = options['model']
    cls = globals()[model]
    model = model.lower()
    column = cls.__dict__['id']

    if not session.query(cls).filter(column == id).one_or_none():
        raise ValueError(f'The {model} is absent.')

    entity = session.query(cls).filter(column == id).one()
    setattr(entity, TABLES[model + 's'].get('column', 'name'), name)

    try:
        session.add(entity)
        session.commit()
    except Exception as error:
        raise error
    else:
        print(f'A {model} has been updated successfully.')


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

    arguments = {key: value
                 for key, value in vars(parser.parse_args()).items()
                 if value is not None}

    try:
        globals()[arguments['action'] + '_action'](**arguments)
    except KeyError as error:
        print(f'The {str(error)[1:-1]} is mandatory.')
    except ValueError as error:
        print(error)
    else:
        session.close()


if __name__ == '__main__':
    main()
