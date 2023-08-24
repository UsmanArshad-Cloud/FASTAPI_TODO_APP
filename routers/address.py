from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

import Models
from Database import SessionLocal
from routers.auth import get_current_user, hash_pwd, verify_pwd, get_user_exception

router = APIRouter(
    prefix="/Address",
    tags=["Address"],
    responses={401: {"user": "Not authorized"}}
)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str


@router.post("/")
async def Create_Address(address: Address,
                         user: dict = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    address_model = Models.Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.country = address.country
    address_model.state = address.state
    address_model.postalcode = address.postalcode

    db.add(address_model)
    db.flush()

    print(db.query(Models.Address).all())

    user_model = db.query(Models.Users).filter(Models.Users.id == user.get("id")).first()
    user_model.address_id = address_model.id
    db.add(user_model)
    db.commit()
