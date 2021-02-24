from fastapi import status, APIRouter, Depends
from fastapi.background import BackgroundTasks
from fastapi.responses import Response
from mongoengine import errors

from fortauto.fortautoMixin.accountMixin import UserMixin
from fortauto.fortautoMixin.generalMixin import Fortauto
from fortauto.model.userModel.accountModel import User
from fortauto.model.userModel.userPydanticModel import (UserInput, UpdateUserInput,
                                                        GetPasswordResetLink,
                                                        PasswordResetInput, UserLoginInput)
from fortauto.settings import WEBSITE_NAME

account_router = APIRouter()


@account_router.post("/register")
async def index(user: UserInput, background: BackgroundTasks):
    if User.find_user_with_email(email=user.email):
        return Fortauto.response({"message": "Account already exist"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    if user.password.strip() == user.confirm_password.strip():
        try:
            password = UserMixin.hash_password(user.password) if UserMixin.hash_password(user.password) else None
            newUser = User(
                email=user.email.lower(),
                first_name=user.first_name.lower(),
                last_name=user.last_name.lower(),
                phone_number=user.phone_number,
                city=user.city.lower(),
                state=user.state.lower(),
                address=user.address,
                password=password
            ).save(clean=True)
            if newUser:
                background.add_task(
                    Fortauto.mailUsr, email_title=f"Account activation",
                    user_email=user.email,
                    email_message=f"Welcome to {WEBSITE_NAME}, "
                                  f"kindly click on the link below to activate your "
                                  f"account\n\n {user.website_url}/{newUser.id}/activate")
                return Fortauto.response({"message": "Account created successfully,"
                                                     " an verification link has been sent to your email"},
                                         status_code=status.HTTP_201_CREATED)
            return Fortauto.response({"message": "Error Creating account, please check your details or try"})
        except errors.NotUniqueError:
            return Fortauto.response(
                {"message": "User with email already exist"},
                status_code=status.HTTP_400_BAD_REQUEST)

        except errors.ValidationError:
            return Fortauto.response(
                {"message": "Error validating details, please check your details and try again"},
                status_code=status.HTTP_400_BAD_REQUEST)
        except Exception.__base__:
            return Fortauto.response(
                {"message": "Error Creating account, please check your details or try"},
                status_code=status.HTTP_400_BAD_REQUEST)
    return Fortauto.response({"message": "Password is does not match"}, status_code=status.HTTP_400_BAD_REQUEST)


@account_router.post("/login")
def loginUserAccount(userIn: UserLoginInput, response: Response):
    user = User.find_user_with_email(email=userIn.email)
    if user:
        if user.active:
            if UserMixin.check_password(userIn.password, user.password):
                encode_jwt_access, encode_jwt_refresh = UserMixin.JwtEncoder(
                    user=user.to_json())
                if encode_jwt_access and encode_jwt_refresh:
                    response.set_cookie(key="refresh_token",
                                        value=encode_jwt_refresh,
                                        httponly=True,
                                        max_age=172800,
                                        expires=172800,
                                        domain=WEBSITE_NAME,
                                        secure=True)
                    SuccessResponseData = {
                        "user": user.to_json(indent=4),
                        "message": "logged in successfully",
                        "access_token": encode_jwt_access,
                        "access_token_type": "Bearer",
                        "expires": "2 days"
                    }
                    return Fortauto.response(SuccessResponseData,
                                             status_code=status.HTTP_200_OK)
            ErrorResponseData = {"message": "Password does not match"}
            return Fortauto.response(ErrorResponseData,
                                     status_code=status.HTTP_401_UNAUTHORIZED)

        ErrorResponseData = {
            "message": "Email was sent to you, please verify your email"}
        return Fortauto.response(ErrorResponseData,
                                 status_code=status.HTTP_401_UNAUTHORIZED)

    ErrorResponseData = {"message": "Account does not exist"}
    return Fortauto.response(ErrorResponseData,
                             status_code=status.HTTP_401_UNAUTHORIZED)


@account_router.get("/me")
def getUserAccount(user: dict = Depends(UserMixin.authenticate_user)):
    return user


@account_router.post("/account/activate")
async def activate_user(user: UpdateUserInput):
    update_user = User.find_user_with_Id(userId=user.userId)
    if update_user["active"]:
        return Fortauto.response(
            {"message": "Account had already been activated"},
            status_code=status.HTTP_400_BAD_REQUEST)
    if update_user:
        update_user.update(active=True)
        update_user.save(clean=True)
        return Fortauto.response(
            {"message": "Account was activated successfully"},
            status_code=status.HTTP_200_OK)
    return Fortauto.response({"message": "Account does not exist"},
                             status_code=status.HTTP_400_BAD_REQUEST)


@account_router.get("/password/reset")
async def get_password_reset_link(background: BackgroundTasks, user: GetPasswordResetLink):
    current_user = User.find_user_with_email(email=user.email)
    if current_user:
        background.add_task(Fortauto.mailUsr,
                            user_email=user.email,
                            email_message=f" Good day {current_user.first_name} {current_user.last_name}, You requested for password reset, "
                                          f"please click\n\n "
                                          f"on to link below to continue \n\n {user.website_url}/{current_user.id}/password/reset",
                            email_title="Password reset link"
                            )
        return Fortauto.response(
            {"message": "password reset link has been sent your email address, click it to continue."},
            status_code=status.HTTP_200_OK)
    return Fortauto.response({"message": "Account does not exist"},
                             status_code=status.HTTP_400_BAD_REQUEST)


@account_router.post("/password/reset")
async def reset_password(user: PasswordResetInput):
    if user.password.strip() == user.confirm_password.strip():
        check_user = User.find_user_with_Id(user.userId)
        if check_user:
            password = UserMixin.hash_password(plaintext_password=user.password)
            if password:
                check_user.update(password=password)
                check_user.save(clean=True)
                print("hello wor")
                return Fortauto.response(
                    {"message": "password changed successfully"},
                    status_code=status.HTTP_200_OK)
            return Fortauto.response({"message": "Error updating password"},
                                     status_code=status.HTTP_400_BAD_REQUEST)
        return Fortauto.response({"message": "Account does not exist"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    return Fortauto.response({"message": "Password does not match"},
                             status_code=status.HTTP_400_BAD_REQUEST)
