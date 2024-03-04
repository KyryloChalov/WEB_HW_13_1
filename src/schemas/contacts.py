from datetime import date
from pydantic import Field, BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from static.constants import NAME_LEN, EMAIL_LEN, PHONE_LEN, NOTES_LEN
from typing import Optional


PhoneNumber.phone_format = "E164"


class ContactModel(BaseModel):
    first_name: str = Field("", max_length=NAME_LEN)
    last_name: Optional[str] = Field("", max_length=NAME_LEN)
    email: Optional[EmailStr] = Field("@", max_length=EMAIL_LEN)
    phone: Optional[PhoneNumber] = Field("+380", max_length=PHONE_LEN)
    birthday: Optional[date] = None
    notes: Optional[str] = Field("", max_length=NOTES_LEN)


class ContactResponse(ContactModel):
    id: int

    class Config:
        from_attributes = True
