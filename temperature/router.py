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
        db: AsyncSession = Depends(get_db)
) -> list[schemas.Temperature]:
    temperatures = await crud.get_all_temperatures(db=db)
    return temperatures
