from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)


Base.metadata.create_all(engine)
print(User.__table__)

me = User(name="Julien", fullname="Julien BOULLY", nickname="BOULLY")

SessionBuilder = sessionmaker(bind=engine)
session = SessionBuilder()

session.add(me)
session.commit()
