from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import Models
from Database import SessionLocal
from routers.auth import get_current_user, hash_pwd, verify_pwd

router = APIRouter(
    prefix="/Users",
    tags=["Users"],
    responses={401: {"user": "Not authorized"}}
)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


@router.get("/get_all_users")
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(Models.Users).all()


@router.get("/get_user_by_path/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Models.Users).filter(Models.Users.id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail="User not Found")
    return {"User": user}


@router.get("/get_user_by_query/")
async def get_user_by_parameter_ud(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Models.Users).filter(Models.Users.id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail="User not Found")
    return {"User": user}


@router.put("/update_my_pwd")
async def update_pwd(curr_pwd: str, new_pwd: str, db: Session = Depends(get_db),
                     user: dict = Depends(get_current_user)):
    if user is None:
        raise get_user_exception()
    curr_user: Models.Users = db.query(Models.Users).filter(Models.Users.id == user.get("id")).first()
    print(curr_pwd)
    print(curr_user.hashed_pwd)
    print(verify_pwd("997480",curr_user.hashed_pwd))
    if verify_pwd(curr_pwd, curr_user.hashed_pwd):
        curr_user.hashed_pwd = hash_pwd(new_pwd)
        db.add(curr_user)
        db.commit()
    else:
        return {400: {"Error": "Password not Matched"}}