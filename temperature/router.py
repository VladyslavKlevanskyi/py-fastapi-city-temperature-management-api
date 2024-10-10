from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import crud, schemas


router = APIRouter()


@router.post("/temperatures/update/", response_model=schemas.Temperature)
async def create_temperature(
        temperature: schemas.TemperatureCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.Temperature:
    return await crud.create_temperature(db=db, temperature=temperature)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
        db: AsyncSession = Depends(get_db),
        city_id: int | None = None
) -> list[schemas.Temperature]:
    # Fetch temperatures from the database, with optional city_id filtering
    temperatures = await crud.get_all_temperatures(db=db, city_id=city_id)

    # If no temperatures are found for the given city_id, raise a 404 error
    if city_id is not None and not temperatures:
        raise HTTPException(
            status_code=404,
            detail="No temperatures found for the given city ID"
        )
    return temperatures
