from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Table, Float, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Uzytkownik(Base):
    __tablename__ = 'uzytkownik'

    id_uzytkownika = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    question = Column(String)
    answer = Column(String)
    role = Column(String)

    def __repr__(self):
        return "<uzytkownik(id_uzytkownika='%s', login='%s', password='%s', question='%s', answer='%s')>" % (
            self.id_uzytkownika, self.login, self.password, self.question, self.answer)


class Paragon(Base):
    __tablename__ = 'paragon'

    id_paragonu = Column(Integer, primary_key=True)
    id_uzytkownika = Column(Integer)
    id_firmy = Column(Integer)


class Firma(Base):
    __tablename__ = 'firma'

    id_firmy = Column(Integer, primary_key=True)
    id_kategorii = Column(Integer)
    nazwa = Column(String)


class Paragon_produkt(Base):
    __tablename__ = 'paragon_produkt'
    __table_args__ = (
        PrimaryKeyConstraint('id_paragonu', 'id_produktu'),
    )

    id_paragonu = Column(Integer, primary_key=True)
    id_produktu = Column(Integer, primary_key=True)
    ilosc = Column(Integer)


class Produkt(Base):
    __tablename__ = 'produkt'

    id_produktu = Column(Integer, primary_key=True)
    nazwa = Column(String)
    cena = Column(Float)


class Kategoria(Base):
    __tablename__ = 'kategoria'

    id_kategorii = Column(Integer, primary_key=True)
    kod_pkd = Column(String)
    nazwa_kategorii = Column(String)


engine = create_engine('postgresql://magda:gessler@localhost:5432/GdzieMojHajsDB')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
