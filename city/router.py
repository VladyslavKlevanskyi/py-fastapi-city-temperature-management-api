from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import crud, schemas


router = APIRouter()


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def retrieve_city_by_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    # Call the get_city_by_id function from your CRUD module
    city = await crud.get_city_by_id(db=db, city_id=city_id)

    # If no city is found, raise a 404 error
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
        city_id: int,
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:

    # Call the CRUD function to update the city
    updated_city = await crud.update_city(db=db, city_id=city_id, city=city)

    # If no updated city is returned,
    # raise a 404 error indicating the city was not found
    if updated_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    # Return the updated city object
    return updated_city


@router.delete("/cities/{city_id}", response_description="Delete a city")
async def remove_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> dict:
    # Call the CRUD function to delete the city
    await crud.delete_city(db=db, city_id=city_id)

    # Return a success message
    return {"detail": "City deleted successfully"}


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)) -> list[schemas.City]:
    return await crud.get_all_cities(db=db)
