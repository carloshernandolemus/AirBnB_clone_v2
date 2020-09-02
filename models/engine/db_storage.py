#!/usr/bin/python3
''' Class to stablish conection with the DB '''
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import MetaData
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel, Base


class DBStorage:
    ''' DBStorage class '''

    __engine = None
    __session = None

    def __init__(self):
        ''' get environment variables '''
        user = os.getenv('HBNB_MYSQL_USER')
        pasw = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        name = os.getenv('HBNB_ENV')

        ''' setting engine '''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, pasw, host, db),
                                      pool_pre_ping=True)
        if name == 'test':
            meta = MetaData(self.__engine)
            meta.drop_all()

    def new(self, obj):
        ''' create new row in database '''
        self.__session.add(obj)

    def save(self):
        ''' commit the changes into DB '''
        self.__session.commit()

    def delete(self, obj=None):
        ''' Delete object from DB '''
        self.__session.delete(obj)

    def all(self, cls=None):
        ''' return dictionary with every objects '''
        session = self.__session
        classes = [User, State, City, Amenity, Place, Review]
        dictionary = {}
        if cls is None:
            for cls in classes:
                query = session.query(cls).all()
                for instance in query:
                    key = '{}.{}'.format(instance.__class__.__name__,
                                         instance.id)
                    dictionary[key] = instance
        else:
            query = session.query(eval(cls)).all()
            for instance in query:
                key = '{}.{}'.format(instance.__class__.__name__,
                                     instance.id)
                dictionary[key] = instance
        return dictionary

    def reload(self):
        ''' reload info '''
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(session)
        self.__session = session
