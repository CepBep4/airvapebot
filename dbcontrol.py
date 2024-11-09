from sqlalchemy import create_engine, Column, Integer, Text, Boolean, JSON, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loggs import write_log
from traceback import print_exc

DATABASE_URL = "mysql://gen_user:%7DXpM%5CkD0%2C9AMbG@213.171.3.234:3306/default_db"#f"sqlite:///db.sqlite3"

# Создание объекта Engine
engine = create_engine(DATABASE_URL)

# Создание базового класса для моделей
Base = declarative_base()

#Пользователи
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(256), nullable=False, unique=True)
    chat_id = Column(Integer, nullable=True, unique=True)
    balance = Column(Integer, nullable=True)
    case_info = Column(JSON, nullable=True)
    
    def get_val(self):
        return {
            'id':self.id,
            'username':self.username,
            'chat_id':self.chat_id,
            'balance':self.balance, 
            'case_info':self.case_info
        }
        
    def get_params(self):
        return {
            'id':User.id,
            'username':User.username,
            'chat_id':User.chat_id,
            'balance':User.balance, 
        }

#Кейсы
class Case(Base):
    __tablename__ = "case"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(256), nullable=True, unique=True)
    content = Column(JSON, nullable=True)
    chance = Column(JSON, nullable=True)
    photo = Column(String(256), nullable=True, unique=False)
    
    def get_val(self):
        return {
            'id':self.id,
            'name':self.name,
            'content':self.content,
            'chance':self.chance, 
            'photo':self.photo
        }

#История
class History(Base):
    __tablename__ = "history"
    id = Column(Integer, autoincrement=True, primary_key=True)
    case_id = Column(Integer, nullable=True)
    number_raffle = Column(Integer, nullable=True)
    prize = Column(String(256), nullable=True)
    
    def get_val(self):
        return {
            'id':self.id,
            'case_id':self.case_id,
            'number_raffle':self.number_raffle,
            'prize':self.prize, 
        }

#Промокоды
class Promo(Base):
    __tablename__ = "promo"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(256), nullable=True)
    count = Column(Integer, nullable=True)
    name_prize = Column(String(256), nullable=True)
    chance = Column(Integer, nullable=True)
    
    def get_val(self):
        return {
            'id':self.id,
            'name':self.name,
            'count':self.count,
            'name_prize':self.name_prize,
            'chance':self.chance,
        }

control_class = {
    'promo': Promo,
    'user': User,
    'case': Case,
    'history': History
}

def base_get(table: str, key, value) -> any:
    try:
        Session = sessionmaker()
        session = Session(bind = engine)
        table = control_class[table]
        
        #Поиск строки
        data = session.query(table).filter(table.get_val(table)[key] == value).first().get_val()
        
        session.close()
        return data
    
    except Exception as error:
        return write_log(str(error))
    
def base_get_all(table):
    try:
        Session = sessionmaker()
        session = Session(bind = engine)
        table = control_class[table]
        
        #Выдача базы
        data = [x.get_val() for x in session.query(table).all()]
        
        session.close()
        return data
    
    except Exception as error:
        print_exc()
        return write_log(str(error))
    
def base_edit(table, key, value, data) -> any:
    try:
        Session = sessionmaker()
        session = Session(bind = engine)
        table = control_class[table]
        
        #Поиск строки
        curr = session.query(table).filter(table.get_val(table)[key] == value).first()

        for key in list(data):
            setattr(curr, key, data[key])
            
        session.commit()
        session.close()
        return True
    
    except Exception as error:
        return write_log(str(error))
    
def base_add(table,js):
    try:
        del js['id']
        Session = sessionmaker()
        session = Session(bind = engine)
        table = control_class[table]

        #Выдача базы
        new = table(**js)
        # new = table(username = 'String(256)', balance = 100, chat_id = 100)
        session.add(new)
        
        session.commit()
        session.close()
        return {'success': True}
    
    except Exception as error:
        print_exc()
        return write_log(str(error))

Base.metadata.create_all(engine)
