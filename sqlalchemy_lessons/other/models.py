from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

# general template "<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>"
# examples

# postgresql
# "postgres+psycopg2://<username>:<password>@<host>:<port>/<database>"

# mysql
# "mysql://<username>:<password>@<host>:<port>/<database>"

# oracle
# "oracle://<username>:<password>@<host>:<port>/<database>"

# sqlite
# "sqlite://:memory:"

# "sqlite://<path>"
# "sqlite:///path/to/database.db"    /// - relative path | //// - absolute path


db_url = "sqlite:///database.db"

engine = create_engine(db_url)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class Gachi(Base):
    __tablename__ = "gachi_actors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hair_color = Column(String)
    phrase = Column(String)


Base.metadata.create_all(engine)  # go and create a db and tables which associated with it
