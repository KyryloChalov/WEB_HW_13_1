from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from sqlalchemy import or_, and_, extract, select, func
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Contact, User
from src.schemas.contacts import ContactModel
from static.colors import GRAY, RESET, CYAN, MAGENTA, WHITE, GRAY_BACK
from typing import List


async def create_contact(contact: ContactModel, user: User, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def read_contacts(db: Session = Depends(get_db), q: str = "", user = User):
    if q:
        return (
            db.query(Contact)
            .filter(
                and_(
                or_(
                    Contact.first_name.ilike(f"%{q}%"),
                    Contact.last_name.ilike(f"%{q}%"),
                    Contact.email.ilike(f"%{q}%"),
                ),
                Contact.user_id == user.id

            ))
            .all()
        )

    return db.query(Contact).filter(Contact.user_id == user.id).all()


async def find_contact(contact_id: int, user: User, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    if contact is None:
        raise HTTPException(
            status_code=404, detail=f"Contact with id: {contact_id} was not found"
        )
    return contact


async def update_contact(contact_id: int, user: User, body: ContactModel, db: Session):
    contact = (
        db.query(Contact)
        .filter(and_(Contact.user_id == user.id,  Contact.id == contact_id))
        .first()
    )

    if contact is None:
        raise HTTPException(
            status_code=404, detail=f"Contact with id: {contact_id} was not found"
        )

    if contact:
        for key, value in body.model_dump().items():
            setattr(contact, key, value)
        db.commit()
        db.refresh(contact)

    return contact


async def delete_contact(contact_id: int, user: User, db: Session = Depends(get_db)):
    db_contact = (
        db.query(Contact)
        .filter(and_(Contact.user_id == user.id, Contact.id == contact_id))
        .first()
    )
    if db_contact is None:
        raise HTTPException(
            status_code=404, detail=f"Contact with id: {contact_id} was not found"
        )
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact successfully deleted"}


def birthdays_print(result, today_, days_):

    def blank(num:int, data) -> str:
        return str(" " * (num - len(str(data))) + str(data))

    print(GRAY, end="")
    if result == []:
        print(f"     there are no contacts whose birthday is in the next {days_} days")
    else:
        print('------------------------------------------------')
        print(GRAY_BACK, ' №   id    birthday   age      fullname       ', RESET, GRAY)
        print('------------------------------------------------')
        for num, r in enumerate(result, 1):
            age = today_.year - r.birthday.year
            print(f"{blank(3, num)}. {blank(4, r.id)} {RESET}", end=' ')
            print(f"{r.birthday.strftime("%d-%m-%Y")}", end=' ')
            print(f"{MAGENTA if r.birthday.day == today_.day else CYAN}", end=' ')
            print(f"{blank(3, age)}{GRAY}", end="  ")
            print(f"{WHITE}{r.first_name } {r.last_name}{GRAY}")
        print('------------------------------------------------')


async def get_next_days_birthdays(user_: User, db: Session = Depends(get_db), days_: int = 7):

    today_ = datetime.today().date()
    # today_ = datetime(year=2023, month=12, day=27).date() # debugging

    result = []
    for num in range(days_+1):

        date_ = today_ + timedelta(num)

        contacts = db.query(Contact).filter_by(user=user_).filter(
            extract('month', Contact.birthday) == date_.month,
            extract('day', Contact.birthday) == date_.day
        ).where(Contact.birthday != None).all()

        for i in range(len(contacts)):
            result.append(contacts[i])

    birthdays_print(result, today_, days_) # debugging
    return result


async def next_week_birthdays(user_: User, db: Session = Depends(get_db), days_: int = 7):

    today_ = datetime.today().date()
    # today_ = datetime(year=2023, month=12, day=27).date() # debugging
    end_date = today_ + timedelta(days_)
    # print(f"from {today_.month}")
    # print(f"till {end_date.month}")

    statement = (
        select(Contact)
        .filter_by(user=user_)
        .filter(
            func.to_char(Contact.birthday, "MM-DD").between(today_.strftime("%m-%d"), end_date.strftime("%m-%d"))
        )
    )
    result = db.execute(statement).scalars().all()

    # result = (
    #     db.query(Contact)
    #     .filter_by(user=user)
    #     .filter(
    #         and_(
    #             func.extract("month", Contact.birthday) == today_.month,
    #             # func.extract("month", Contact.birthday).between(today_.month, end_date.month),
    #             func.extract("day", Contact.birthday).between(today_.day, end_date.day)
    #         )
    #     )
    #     .all()
    # )


    birthdays_print(result, today_, end_date) # debugging
    return result


async def get_week_birthdays(user: User, db: Session = Depends(get_db), days_: int = 7):

    today_ = datetime.today().date()
    # today_ = datetime(year=2023, month=12, day=30) # debugging
    end_date = today_ + timedelta(days=days_)

    result = (
        db.query(Contact)
        .filter(
            and_(
                or_(
                    and_(
                        extract("day", Contact.birthday) >= today_.day,
                        extract("month", Contact.birthday) == today_.month,
                    ),
                    and_(
                        extract("day", Contact.birthday) <= end_date.day,
                        extract("month", Contact.birthday) == end_date.month,
                    ),
                ),
                Contact.user_id == user.id,
            )
        )
        .all()
    )
    birthdays_print(result, today_, end_date) # debugging
    return result

# from sqlalchemy.ext.asyncio import AsyncSession

async def get_contact_by_birthday(user_: User, db: Session, days_: int = 7):

    today_ = datetime.today().date()
    end_date = today_+ timedelta(days=days_)

    result = []

    stmt = select(Contact).filter_by(user=user_).where(Contact.birthday != None)
    contacts = db.execute(stmt)
    contacts = contacts.scalars().all()
    
    for contact in contacts:
        bday_this_year = datetime(year=today_.year, month=contact.birthday.month, day=contact.birthday.day).date()

        if bday_this_year >= today_ and bday_this_year <= end_date:
            result.append(contact)

    birthdays_print(result, today_, end_date) # debugging
    return result
