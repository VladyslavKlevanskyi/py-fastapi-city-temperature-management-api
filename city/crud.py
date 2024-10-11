from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> schemas.City:

    # Prepare an insert query for the City model,
    # including returning the ID of the inserted record
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )

    # Execute the query
    result = await db.execute(query)

    # Commit the transaction to save changes in the database
    await db.commit()

    # Get the ID of the newly inserted city
    new_city_id = result.inserted_primary_key[0]

    # Prepare the response by retrieving the created city instance
    created_city_query = select(models.City).where(
        models.City.id == new_city_id)
    created_city_result = await db.execute(created_city_query)
    created_city = created_city_result.scalars().first()

    if created_city is None:
        raise HTTPException(status_code=500,
                            detail="City was not created correctly")

    # Return the created City object as a Pydantic model
    return schemas.City.from_orm(created_city)


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    # Create a select query to find a City record by its ID
    query = select(models.City).where(models.City.id == city_id)

    # Execute the query asynchronously
    result = await db.execute(query)

    # Retrieve the first City instance from the result set
    city = result.scalars().first()

    # Return the found City object or None if not found
    return city


async def update_city(
        db: AsyncSession,
        city_id: int,
        city: schemas.CityCreate
) -> models.City | None:

    # Prepare an update query for the City model
    query = update(models.City).where(models.City.id == city_id).values(
        name=city.name,
        additional_info=city.additional_info,
    )

    # Execute the query asynchronously
    await db.execute(query)

    # Commit the transaction to save changes in the database
    await db.commit()

    # Retrieve the updated City instance from the database
    updated_city = await get_city_by_id(db=db, city_id=city_id)

    # Return the updated City object
    return updated_city


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> None:
    # Check if the city exists before trying to delete
    existing_city = await get_city_by_id(db, city_id)

    if not existing_city:
        raise HTTPException(status_code=404, detail="City not found")

    # Prepare a delete query for the City model
    query = delete(models.City).where(models.City.id == city_id)

    # Execute the delete query asynchronously
    await db.execute(query)

    # Commit the transaction to save changes to the database
    await db.commit()


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    # Create a select query to retrieve all records from the City model
    query = select(models.City)

    # Execute the query asynchronously
    result = await db.execute(query)

    # Extract all the Temperature instances from the result set
    cities_list = result.scalars().all()

    # Return the list of Temperature objects as Pydantic models
    return [schemas.City.from_orm(city) for city in cities_list]
