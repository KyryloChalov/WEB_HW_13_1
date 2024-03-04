from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from src.database.db import get_db, reset_db

router = APIRouter(prefix="/database", tags=["database"])

@router.delete("/reset_base")
async def reset_database():
    reset_db()
    return {"message": "Congratulations! You have a new fresh database"}


@router.get("/healthchecker") # треба розібратися як воно працює (НЕ працює)
async def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=502, detail="Database is not configured correctly"
            )
        return {"message": "Congratulations! Database is really healthy"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=502, detail="Error connecting to the database")
