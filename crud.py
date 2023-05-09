from sqlalchemy.future import select
from typing import List
from sqlalchemy.orm import selectinload

import models
from database import session

from loguru import logger


@logger.catch()
async def get_dish(dish_id: int) -> models.Dish:
    async with session.begin():
        stmt = select(models.Dish).where(models.Dish.id == dish_id).options(selectinload(models.Dish.ingredients))
        result = await session.execute(stmt)

    return result.scalars().one()

@logger.catch()
async def get_all_dishes() -> List[models.Dish]:
    stmt = select(models.Dish).order_by(models.Dish.number_of_views.desc(), models.Dish.preparation_time)
    async with session.begin():
        result = await session.execute(stmt)

    return result.scalars().all()

@logger.catch()
async def get_ingredient(id_ingredient) -> models.Ingredient:
    stmt = select(models.Ingredient).where(models.Ingredient.id == id_ingredient)
    async with session.begin():
        result = await session.execute(stmt)

    return  result.scalars().one()

@logger.catch()
async def get_ingredient_by_name(name):
    stmt = select(models.Ingredient).where(models.Ingredient.name == name)
    async with session.begin():
        result = await session.execute(stmt)

    return result.fetchone()

@logger.catch()
async def add_ingredient(ingredient) -> models.Ingredient:
    new_ingredient = models.Ingredient(**ingredient.dict())
    async with session.begin():
        await session.add(new_ingredient)

    return new_ingredient

@logger.catch()
async def update_ingredient(db_ingredient, now_ingredient) -> models.Ingredient:
    db_ingredient.name = now_ingredient.name
    db_ingredient.unit = now_ingredient.unit
    db_ingredient.value = now_ingredient.value
    db_ingredient.dish_id =now_ingredient.dish_id
    await session.commit()

    return db_ingredient

@logger.catch()
async def delete_ingredient(id) -> models.Ingredient:
    async with session.begin():
        result = await session.execute(select(models.Ingredient).where(models.Ingredient.id == id))
        record = result.scalars().one()
        await session.delete(record)

    return record

@logger.catch()
async def add_dish(dish) -> models.Dish:
    async with session.begin():
        new_dish = models.Dish(**dish.dict())
        async with session.begin():
            await session.add(new_dish)

        return new_dish

@logger.catch()
async def delete_dish(id_dish) -> models.Dish:
    async with session.begin():
        result = await session.execute(select(models.Dish).where(models.Dish.id == id_dish))
        record = result.scalars().one()
        await session.delete(record)

    return record

@logger.catch()
async def update_dish(db_dish, new_dish) -> models.Dish:
    db_dish.name_of_dish = new_dish.name_of_dish
    db_dish.preparation_time = new_dish.preparation_time
    db_dish.description = new_dish.name_of_dish
    db_dish.ingredients = new_dish.ingredients
    await session.commit()

    return db_dish
