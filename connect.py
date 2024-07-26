from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from uri import uri

engine = create_engine(uri())
Session = sessionmaker(engine)
session = Session()
