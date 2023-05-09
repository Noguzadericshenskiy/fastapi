from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from typing import Dict

from database import Base


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(Integer, primary_key=True)
    name_of_dish = Column(String, index=True)
    preparation_time = Column(Integer)
    number_of_views = Column(Integer)
    description = Column(String, index=True)

    ingredients = relationship("Ingredient", back_populates="dish")

    def to_json(self) -> Dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    unit = Column(String(10))
    value = Column(Integer)
    dish_id = Column(Integer, ForeignKey('dish.id'))

    dish = relationship("Dish", back_populates="ingredients")

    def to_json(self) -> Dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
