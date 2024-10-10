from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models, schemas
from city import models as city_models


async def create_temperature(
        db: AsyncSession,
        temperature: schemas.TemperatureCreate
) -> schemas.Temperature:
    # Check if the city with the given city_id exists
    city_query = select(city_models.City).where(
        city_models.City.id == temperature.city_id)
    city_result = await db.execute(city_query)
    city = city_result.scalars().first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    # Prepare an insert query for the Temperature model,
    # including returning the ID of the inserted record
    query = insert(models.Temperature).values(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature,
    )

    # Execute the query
    result = await db.execute(query)

    # Commit the transaction to save changes in the database
    await db.commit()

    # Retrieve the created Temperature instance
    # using the ID of the newly inserted record
    created_temperature_id = result.inserted_primary_key[0]

    # Prepare a select query to retrieve the created temperature instance
    select_query = select(models.Temperature).where(
        models.Temperature.id == created_temperature_id)
    created_temperature_result = await db.execute(select_query)
    created_temperature = created_temperature_result.scalars().first()

    # Return the created Temperature object as a Pydantic model
    return schemas.Temperature.from_orm(created_temperature)


async def get_all_temperatures(db: AsyncSession) -> list[schemas.Temperature]:
    # Create a select query to retrieve all records from the Temperature model
    query = select(models.Temperature)

    # Execute the query asynchronously
    result = await db.execute(query)

    # Extract all the Temperature instances from the result set
    temperatures_list = result.scalars().all()

    # Return the list of Temperature objects as Pydantic models
    return [schemas.Temperature.from_orm(temp) for temp in temperatures_list]
