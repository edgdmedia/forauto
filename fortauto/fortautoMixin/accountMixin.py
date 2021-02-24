from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from fortauto.model.userModel.accountModel import User
from fortauto.settings import (SECRET_KEY, REFRESH_TOKEN_EXPIRE_TIME, ACCESS_TOKEN_EXPIRE_TIME, REFRESH_KEY)
from fortauto.settings import WEBSITE_NAME, API_URL

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta


class UserMixin(object):
    Oauth_schema = OAuth2PasswordBearer(tokenUrl=f"{WEBSITE_NAME}{API_URL}/user/login")

    @staticmethod
    def hash_password(plaintext_password: str) -> bytes:
        password = pwd_context.hash(plaintext_password)
        if password:
            return password
        return None

    @staticmethod
    def JwtEncoder(user: dict):
        access_token_time = datetime.utcnow() + timedelta(days=int(ACCESS_TOKEN_EXPIRE_TIME))
        refresh_token_time = datetime.utcnow() + timedelta(days=int(REFRESH_TOKEN_EXPIRE_TIME))
        data_access_token = {"user": user, "exp": access_token_time}
        data_refresh_token = {"user": user, "exp": refresh_token_time}
        try:
            encode_jwt_refresh = jwt.encode(
                claims=data_refresh_token, key=REFRESH_KEY)
            encode_jwt_access = jwt.encode(
                claims=data_access_token, key=SECRET_KEY)
            return encode_jwt_access, encode_jwt_refresh
        except JWTError as e:
            raise HTTPException(detail={
                "error": "Error jwt error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def authenticate_user(token: str = Depends(Oauth_schema)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token=token, key=SECRET_KEY)
            user: dict = payload.get("user")
            if user is None:
                raise credentials_exception
            currentUser = User.find_user_with_email(user["email"])
            if currentUser is None:
                raise credentials_exception
            return currentUser.to_json()
        except JWTError:
            raise credentials_exception

    @staticmethod
    def check_password(plaintext_password, hashed_password):
        password = pwd_context.verify(plaintext_password, hashed_password)
        if password:
            return True
        return False
