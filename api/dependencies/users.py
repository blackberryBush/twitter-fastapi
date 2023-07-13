from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from config import SECRET_KEY, ALGORITHM
from services.token import TokenService
from services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


async def validate_user(token: str = Depends(oauth2_scheme)):
    if not TokenService.is_token_valid(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    user = await UserService.get_user(username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user.id
