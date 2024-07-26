def uri() -> str:
    with open('.secret', encoding='utf-8') as file:
        return f'postgresql://postgres:{file.read()}@localhost:5432/postgres'
