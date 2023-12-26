from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, or_, and_, update, delete
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from PyQt5.QtWidgets import QMessageBox

Base = declarative_base()

class Logins(Base):
    __tablename__ = 'logins'
    id = Column(Integer, primary_key= True, index= True)
    username = Column(String, unique= True, index= True)
    password = Column(String)
    key = Column(String)
    saved_data = relationship('SavedData', back_populates= 'login')

class SavedData(Base):
    __tablename__ = 'saved_data'
    id = Column(Integer, primary_key= True, index= True)
    tag = Column(String)
    username = Column(String)
    password = Column(String)
    website = Column(String)
    category = Column(String)
    note = Column(String, default='')
    login_id = Column(Integer, ForeignKey('logins.id'))
    login = relationship('Logins', back_populates= 'saved_data')

class data():
    def __init__(self) -> None:
        self.engine = create_engine('sqlite:///database.db')
        self.Session = sessionmaker(bind= self.engine)
        self.create_table()
        self.session = self.Session()

    def create_table(self):
        Base.metadata.create_all(bind=self.engine)

    def add_user(self, userInput: str, passInput: str, keyInput: str) -> None:
        try:
            self.session.add(Logins(username = userInput, password = passInput, key = keyInput))
            self.session.commit()
        except:
            QMessageBox.warning(None, 'Error', 'useername is already taken!')
    

    def add_data(self, login_id: int, tag: str, username: str, password: str, website: str, category: str, note: str = '') -> None:
        self.session.add(SavedData(
            login_id = login_id,
            tag = tag,
            username = username,
            password = password,
            website = website,
            category = category,
            note = note,
        ))
        self.session.commit()

    def get_user(self, userInput: str) -> list:
        return self.session.query(Logins).filter(Logins.username == userInput).all()
    
    def get_data(self, id: int) -> list:
        return self.session.query(SavedData).filter(SavedData.login_id == id).all()
    
    def get_everything(self, word: str, id: int) -> list:
        return self.session.query(SavedData).filter(or_(SavedData.category.like(f'%{word}%'), SavedData.tag.like(f'%{word}%'), SavedData.username.like(f'%{word}%'), SavedData.website.like(f'%{word}%')), and_(SavedData.login_id == id)).all()

    def get_record(self, login_id: int, tag: str, username: str, website: str, category: str) -> list:
        return self.session.query(SavedData).filter(and_(SavedData.login_id == login_id, SavedData.tag == tag, SavedData.username == username, SavedData.website == website, SavedData.category == category)).all()
    
    def delete_data(self, login_id: int, tag: str, username: str, website: str, category: str) -> None:
        self.session.query(SavedData).filter(and_(SavedData.login_id == login_id, SavedData.tag == tag, SavedData.username == username, SavedData.website == website, SavedData.category == category)).delete()
        self.session.commit()
        
    def delete_parent(self, category: str, id: int) -> None:
        self.session.query(SavedData).filter(and_(SavedData.category == category, SavedData.login_id == id)).delete()
        self.session.commit()

    def update_data(self, oldRecord: list, newRecord: list) -> None:
        records = self.session.query(SavedData).filter(and_(SavedData.login_id == oldRecord[0], SavedData.tag == oldRecord[1], SavedData.username == oldRecord[2], SavedData.website == oldRecord[3], SavedData.category == oldRecord[4])).all()
        for record in records:
            record.tag = newRecord[0]
            record.username = newRecord[1]
            record.password = newRecord[2]
            record.website = newRecord[3]
            record.category = newRecord[4]
            record.note = newRecord[5]
            self.session.commit()