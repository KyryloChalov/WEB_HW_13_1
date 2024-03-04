from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas.contacts import ContactModel, ContactResponse
from src.services.auth import auth_service
from typing import List

router = APIRouter(prefix="/contacts", tags=["contacts"])


# @router.post("/", response_model=ContactResponse)
@router.post(
    "/",
    response_model=ContactResponse,
    description="No more than 2 requests per minute",
    dependencies=[Depends(RateLimiter(times=2, seconds=60))],
)
async def create_contact(
    contact: ContactModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_contacts.create_contact(contact, current_user, db)


# всі контакти без зайвих питань - чи воно треба?
# @router.get("/", response_model=List[ContactResponse])
# async def read_all_contacts(db: Session = Depends(get_db)):
#     contacts = await repository_contacts.read_contacts(db)
#     return contacts


# пошук рядка find_string в полях first_name, last_name, email
# якшо рядок пошуку порожній - виводяться всі контакти
@router.get(
    "/",
    response_model=List[ContactResponse],
    description="No more than 5 requests per minute",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def read_contacts(
    db: Session = Depends(get_db),
    find_string: str = "",
    current_user: User = Depends(auth_service.get_current_user),
):
    contacts = await repository_contacts.read_contacts(db, find_string, current_user)
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
    description="No more than 5 requests per minute",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def find_contact_id(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.find_contact(contact_id, current_user, db)
    return contact


@router.put(
    "/{contact_id}",
    response_model=ContactResponse,
    description="No more than 5 requests per minute",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def update_contact(
    contact_id: int,
    contact: ContactModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.update_contact(
        contact_id, current_user, contact, db
    )
    return contact


@router.delete(
    "/{contact_id}",
    description="No more than 5 requests per minute",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def delete_contact(
    contact_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    contact = await repository_contacts.delete_contact(contact_id, current_user, db)
    return contact


@router.get(
    "/birthdays/",
    response_model=List[ContactResponse],
    description="No more than 5 requests per minute",
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def get_next_days_birthdays(
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
    days: int = 7,
):
    contacts = await repository_contacts.get_next_days_birthdays(current_user, db, days)
    return contacts


# @router.get(
#     "/birthdays_4/",
#     response_model=List[ContactResponse],
#     description="No more than 5 requests per minute",
#     dependencies=[Depends(RateLimiter(times=5, seconds=60))],
# )
# async def get_contact_by_birthday(
#     current_user: User = Depends(auth_service.get_current_user),
#     db: Session = Depends(get_db),
#     days: int = 7,
# ):
#     contacts = await repository_contacts.get_contact_by_birthday(current_user, db, days)
#     return contacts
