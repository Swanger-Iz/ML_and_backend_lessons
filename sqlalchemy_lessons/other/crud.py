# CRUD - create, read, update, delete

# from argparse import ArgumentParser

from sqlalchemy.orm import sessionmaker

from sqlalchemy_lessons.other.models import User, engine

# parser = ArgumentParser()
# parser.add_argument("--name", type=str, required=True)
# parser.add_argument("--hc", type=str, required=True)
# parser.add_argument("--p", type=str, default="Ass")
# args = parser.parse_args()

Session = sessionmaker(bind=engine)
session = Session()

#### Inserting rows
# user = User(name="John doe", age=30)
# user2 = User(name="Andrew Pip", age=25)
# user3 = User(name="Iron man", age=57)
# user4 = User(name="Richard Gear", age=25)

# session.add(user2)
# session.add_all([user3, user4])

# session.commit()

# user = Gachi(name=args.name, hair_color=args.hc, phrase=args.p)
# session.add(user)
# session.commit()

### Reading data
# users = session.query(User).all()
# for u in users:
#     print(f"Id: {u.id}, name: {u.name}, age: {u.age}")

# print("-" * 20)

# users = session.query(Gachi).all()
# for u in users:
#     print(f"Id: {u.id}, name: {u.name}, phrase: {u.phrase}")


### Filter and update
# user = session.query(User).filter_by(id=1).all() / .one_or_none() / .first()
# users = session.query(User).filter(User.age < 30, User.id == 4).all()
# print(users)
# for u in users:
#     u.name = "A different name"
#     print(f"Id: {u.id}, name: {u.name}, age: {u.age}")

# session.commit()

### Delete item
# session.add(User(name="temp user", age=18))

# for u in session.query(User).all():
#     print(f"Id: {u.id}, name: {u.name}, age: {u.age}")

# session.commit()


user = session.query(User).filter(User.id == 5).one_or_none()
session.delete(user)
session.commit()
