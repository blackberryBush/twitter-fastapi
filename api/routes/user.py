from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.exc import IntegrityError
from starlette import status

from config import SECRET_KEY, ALGORITHM
from schemas.jwt import TokenPair
from schemas.user import UserCreateSchema
from services.token import TokenService
from services.user import UserService

router = APIRouter(tags=["Users"])


# REGISTER USER
@router.post("/register", response_model=TokenPair)
async def register_user(user_data: UserCreateSchema):
    try:
        user = await UserService.create_user(user_data)
        return TokenService.create_token_pair(data={"sub": user.username})
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# LOGIN
@router.post("/login", response_model=TokenPair)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return TokenService.create_token_pair(data={"sub": user.username})


# REFRESH TOKEN
@router.post("/refresh", response_model=TokenPair)
async def refresh_tokens(refresh_token: str):
    if not TokenService.is_token_valid(refresh_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    user = await UserService.get_user(username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return TokenService.create_token_pair(data={"sub": user.username})
