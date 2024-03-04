from libgravatar import Gravatar
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import User
from src.schemas.users import UserModel
from src.services.auth import auth_service
from typing import List


def create_users(count: int, db: Session):

    # users_ = {"Kyrylo": "kyrylo.chalov@gmail.com",
    #     "meta": "kirill_chalov@meta.ua",
    #     "ks797": "ks7977166@gmail.com"}

    # for key, value in users_.items():
    #     body = UserModel(
    #         username=key,
    #         email=value,
    #         password="123456",
    #     )
    #     body.password = auth_service.get_password_hash(body.password)
    #     print(f"{body.username}, {body.email}")
    #     avatar = None
    #     try:
    #         g = Gravatar(body.email)
    #         avatar = g.get_image()
    #     except Exception as e:
    #         print(e)
    #     new_user = User(**body.model_dump(), avatar=avatar, confirmed=True)
    #     db.add(new_user)
    #     db.commit()
    #     db.refresh(new_user)

    number_user = len(db.query(User).all()) + 1

    for num in range(number_user, (number_user + count)):
        body = UserModel(
            username=f"user_{str(num)}",
            email=f"user_{str(num)}@gmail.com",
            password="123456",
        )
        body.password = auth_service.get_password_hash(body.password)

        avatar = None
        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except Exception as e:
            print(e)
        new_user = User(**body.model_dump(), avatar=avatar, confirmed=True)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)


def seed_users(count_users: int=3):
    create_users(count_users, db=next(get_db()))

def main():
    seed_users()

if __name__ == "__main__":
    main()
