from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Contact, User
from src.seed.users import seed_users
from typing import List
import random
from faker import Faker

fake_data: Faker = Faker(locale="uk_UA")

PHONES_CODES = [
    "067",
    "097",
    "096",
    "098",
    "068",
    "050",
    "066",
    "095",
    "099",
    "063",
    "093",
    "073",
]


def create_contacts(count: int) -> List[dict]:
    contacts = []
    for _ in range(count):
        notes = ""
        if bool(random.getrandbits(1)):
            notes = fake_data.paragraph(nb_sentences=1)
        contacts.append(
            {
                "first_name": fake_data.first_name(),
                "last_name": fake_data.last_name(),
                "email": fake_data.free_email(),
                "birthday": fake_data.date_of_birth(minimum_age=5, maximum_age=99),
                "phone": f"+38{random.choice(PHONES_CODES)}{fake_data.msisdn()[6:]}",
                "notes": notes,
            }
        )
    return contacts


def upload_contacts(db: Session, contacts: List[dict]) -> None:
    users = db.query(User).all()
    if len(users) < 1:
        # якщо нема жодного user'а, робимо 3 стандартні контакти
        seed_users(3)
        users = db.query(User).all()

    for contact_data in contacts:
        contact = Contact(**contact_data, user=random.choice(users))
        db.add(contact)
    db.commit()


def seed_contacts(count_contacts: int=10):
    contacts = create_contacts(count_contacts)
    upload_contacts(db=next(get_db()), contacts=contacts)


def main():
    seed_contacts()

if __name__ == "__main__":
    main()
