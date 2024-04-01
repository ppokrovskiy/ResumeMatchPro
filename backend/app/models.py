from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# class BaseModel(Base):
#     pass


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    cities = relationship("City", back_populates="country")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    country = relationship("Country", back_populates="cities")
