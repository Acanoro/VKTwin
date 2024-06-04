from sqlalchemy import CheckConstraint, Column, Integer, String, Enum, ForeignKey, BIGINT

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    id_tg = Column(BIGINT, unique=True)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))
    city = Column(String(length=100))
    gender = Column(Enum('м', 'ж', name='gender_enum'))
    age = Column(Integer, CheckConstraint('age >= 18 AND age <= 100', name='age_between_18_and_100'))

    def __str__(self):
        return f'Users: {self.last_name} {self.first_name}'


class profiles(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    vk_id = Column(BIGINT, unique=True)

    def __str__(self):
        return f'Profiles: {self.vk_id}'


class favorites(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('Users', backref='user')

    profile_id = Column(Integer, ForeignKey('profiles.id'))
    profiles = relationship('profiles', backref='favorite')

    def __str__(self):
        return f'Favorites: {self.user_id} {self.profile_id}'


class BlackList(Base):
    __tablename__ = 'black_list'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', backref='blacklisted_users')

    profile_id = Column(Integer, ForeignKey('profiles.id'))
    profile = relationship('profiles', backref='blacklisted_profiles')

    def __str__(self):
        return f'BlackList: {self.user_id} {self.profile_id}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
