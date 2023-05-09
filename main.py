from typing import List

from fastapi import FastAPI, Path, Query, HTTPException

import crud
import models
import schemas

from database import engine, session

app = FastAPI()


@app.on_event("startup")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post("/ingredient/", response_model=schemas.IngredientOut)
async def ingredient(ingredient: schemas.IngredientIn) -> models.Ingredient:
    """Добавить новый ингредиент"""
    if await crud.get_ingredient_by_name(name=ingredient.name):
        raise HTTPException(status_code=400, detail="Такой ингредиент уже есть")

    return await crud.add_ingredient(ingredient)


@app.put("/ingredient/{id_ingredient: int}", response_model=schemas.IngredientOut)
async def ingredient(id_ingredient: int, ingredient: schemas.IngredientIn) -> models.Ingredient:
    """Изменить существующий ингредиент"""
    db_ingredient = await crud.get_ingredient(id_ingredient=id_ingredient)
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Такой записи нет в базе")

    return await crud.update_ingredient(db_ingredient=db_ingredient, now_ingredient=ingredient)


@app.get("/ingredient/{id: int}", response_model=schemas.IngredientOut)
async def ingredient(id: int) -> models.Ingredient:
    "Получить ингредиент"

    return await crud.get_ingredient(id_ingredient=id)


@app.delete("/ingredient/{id: int}", response_model=schemas.IngredientOut)
async def ingredient(id: int) -> models.Ingredient:
    "Удалить ингредиент"

    return await crud.delete_ingredient(id=id)


@app.post("/dish/", response_model=schemas.DishOut)
async def dish(dish: schemas.DishIn) -> models.Dish:
    """Добавить новое блюдо"""

    return await crud.add_dish(dish)


@app.put("/dish/{dish_id: int}", response_model=schemas.DishOut)
async def dish(dish_id: int, dish: schemas.DishIn) -> models.Dish:
    """Изменить информацию о блюде"""

    db_dish = await crud.get_dish(dish_id=dish_id)
    if not db_dish:
        raise HTTPException(status_code=404, detail="Такой записи нет в базе")

    return await crud.update_dish(db_dish, dish)



@app.delete("/dish/{dish_id: int}", response_model=schemas.DishOut)
async def dish(dish_id: int) -> models.Dish:
    "Удалить блюдо"

    return await crud.delete_dish(id_dish=dish_id)


@app.get("/dish/{dish_id: int}", response_model=schemas.DishOut)
async def dish(dish_id:int) -> models.Dish:
    """Получить блюдо по ID"""

    return await crud.get_dish(dish_id=dish_id)


@app.get('/dishes/', response_model=List[schemas.DishesAllOut])
async def dishes() -> List[models.Dish]:
    """Получить список всех блюд"""

    return await crud.get_all_dishes()
