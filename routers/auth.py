from typing import Optional
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status

from Database import engine
from datetime import timedelta, datetime
import Models
from Database import SessionLocal
from sqlalchemy.orm import Session
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)

Models.Base.metadata.create_all(bind=engine)
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "bd1ae5cc926d6e03733f6829943955e6601068d5a8187267f53e1d87f6545322"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def hash_pwd(plain_pwd: str):
    return bcrypt_context.hash(plain_pwd)


def verify_pwd(plain_pwd, hashed_pwd):
    return bcrypt_context.verify(plain_pwd, hashed_pwd)


def authenticate_user(username, pwd, db):
    user_model = db.query(Models.Users).filter(Models.Users.username == username).first()
    if user_model is None:
        return None
    if not verify_pwd(pwd, user_model.hashed_pwd):
        return None
    return user_model


def create_access_token(username: str, userid: int, expires_delta: Optional[timedelta] = None):
    encode = {"username": username, "userid": userid}
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=20)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.get("/get_current_user")
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username: str = payload.get("username")
        userid: int = payload.get("userid")
        expire = payload.get("exp")
        if username is None or userid is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "id": userid}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


class User(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    phone_number:str


@router.get("/")
async def GetAllUsers(db: Session = Depends(get_db)):
    return db.query(Models.Users).all()


@router.post("/create/users")
async def CreateNewUser(user: User, db: Session = Depends(get_db)):
    new_user = Models.Users()
    new_user.email = user.email
    new_user.username = user.username
    new_user.first_name = user.first_name
    new_user.last_name = user.last_name
    new_user.hashed_pwd = hash_pwd(user.password)
    new_user.phone_number = user.phone_number

    db.add(new_user)
    db.commit()
    return successful_response(201)


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise http_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, token_expires)
    return {"token", token}


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="User not found")


# Exceptions
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception
