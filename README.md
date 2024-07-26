# University

## Deployment

```bash
$ echo 'your database user password' > .secret
$ docker run --name lexhouk-hw-07 -p 5432:5432 -e "POSTGRES_PASSWORD=$(cat .secret)" -d postgres
$ alembic upgrade head
$ python seed.py
```

## Usage

```bash
$ python my_select.py
```
