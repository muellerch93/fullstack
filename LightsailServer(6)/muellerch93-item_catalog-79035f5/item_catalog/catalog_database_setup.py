import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(800), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

print(sys.path)
url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format('catalog', 'password', 'localhost', '5432', 'catalog_db')
engine = create_engine(url, client_encoding='utf8')
Base.metadata.create_all(engine)
