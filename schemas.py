from pydantic import BaseModel, Field

from typing import List

class BaseIngredient(BaseModel):
    name: str = Field(
        title='Название ингредиента',
        description='Название ингредиента')
    unit: str = Field(
        title='Единица измерения',
        description='Единица измерения')
    value: int = Field(
        title='Значение в граммах',
        description='Значение в граммах')
    dish_id: int = Field(
        title='ID блюда',
        description='ID блюда')


class IngredientIn(BaseIngredient):
    ...


class IngredientOut(BaseIngredient):
    id: int = Field(title='ID ингредиента')

    class Config:
        orm_mode = True


class BaseDish(BaseModel):
    name_of_dish: str = Field(title='Название блюда', description='Название блюда')
    preparation_time: int = Field(
        title='Время приготовления',
        description='Время приготовления в минутах',
        )
    number_of_views: int = Field(
        title='Количество просмотров',
        description='Количество просмотров')
    description: str = Field(
        title='Описание',
        description='Описание')


class DishIn(BaseDish):
    ingredients: List[IngredientOut] = Field(title='Список ингредиентов', description='Список ингредиентов')


class DishOut(BaseDish):
    id: int = Field(title='ID блюда', description='ID блюда')
    ingredients: List[IngredientOut] = Field(title='Список ингредиентов', description='Список ингредиентов')

    class Config:
        orm_mode = True


class DishesAllOut(BaseModel):
    id: int = Field(title='ID блюда', description='ID блюда')
    name_of_dish: str = Field(title='Название блюда', description='Название блюда')
    preparation_time: int = Field(
        title='Время приготовления',
        description='Время приготовления в минутах',
        )
    number_of_views: int = Field(
        title='Количество просмотров',
        description='Количество просмотров')

    class Config:
        orm_mode = True
