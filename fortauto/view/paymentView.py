from fortauto.model.payments.paymentModel import Payment, Deposit
from fortauto.model.payments.paymentPydanticModel import UserPayment, UserDeposit, UpdatePayment, UpdateDeposit
from fastapi import APIRouter, Depends, status
from fortauto.fortautoMixin.accountMixin import UserMixin
from fortauto.fortautoMixin.generalMixin import Fortauto
from mongoengine import errors

payment_router = APIRouter()
user_deposit  = APIRouter()
@payment_router.post("/")
async def create_payment(paymentDetails:UserPayment, user:dict = Depends(UserMixin.authenticate_user)):
    try:
        if paymentDetails.method.lower() == "direct":
            user_credit_account = Deposit.get_user_account(userId=user["id"])
            if user_credit_account:
                if user_credit_account >= paymentDetails.total_amount:
                    current_balance = (user_credit_account.total_amount - paymentDetails.total_amount)
                    user_credit_account.update(total_amount=current_balance, method=paymentDetails.method.lower())
                    user_credit_account.save(clean=True)
                    return Fortauto.response({"message": "new payment saved"}, status_code=status.HTTP_201_CREATED)
                return Fortauto.response({"message": "User does not sufficient balance"},
                                         status_code=status.HTTP_400_BAD_REQUEST)
            return Fortauto.response({"message":"user does not have a credit account"},
                                     status_code=status.HTTP_400_BAD_REQUEST)
        data = {**paymentDetails.dict(), "userId": user["id"]}
        payment = Payment(**data).save(clean=True)
        if payment:
            # MAKE REQUEST TO VERIFY PAYMENT
            return Fortauto.response({"message": "new payment saved"}, status_code=status.HTTP_201_CREATED)
        return Fortauto.response({"message": "error saving new payment"}, status_code=status.HTTP_400_BAD_REQUEST)
    except errors.ValidationError:
        return Fortauto.response({"message": "error saving new payment, please try again!"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    except errors.NotUniqueError:
        return Fortauto.response({"message": "payment with this reference number added already"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    except Exception.__base__:
        return Fortauto.response({"message": "error saving payment"},
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@payment_router.put("/")
async def update_payment( payment_details:UpdatePayment, user: dict = Depends(UserMixin.authenticate_user)):
    if user["admin"] or user["super_admin"]:
        try:
            payment = Payment.get_single_payment(payment_RefNo=payment_details.payment_RefNo)
            if payment:
               if payment_details.total_amount:
                   payment.update(payment_status=payment_details.payment_status, total_amount=payment_details.total_amount)
               payment.update(payment_status=payment_details.payment_status)
               payment.save(clean=True)
               payment = Payment.get_single_payment(payment_RefNo=payment_details.payment_RefNo)
               return Fortauto.response({"payments": payment.to_json(), "message":"payment updated successfully"},
                                         status_code=status.HTTP_200_OK)
            return Fortauto.response({"message": "payment not found"},
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except errors.DoesNotExist:
            return Fortauto.response({"message": "payment does not exist"}, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception.__base__:
            return Fortauto.response({"message": "error updating payment"},
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Fortauto.response({"message": "error validating admin"},
                             status_code=status.HTTP_401_UNAUTHORIZED)

@payment_router.get("/")
async def get_payments(user:dict = Depends(UserMixin.authenticate_user)):
    try:
        payment = Payment.get_user_payment(userId=user["id"])
        if payment:
            return Fortauto.response({"payments": [payment.to_json() for payment in payment]},
                                     status_code=status.HTTP_200_OK)
        return Fortauto.response({"message": "user does not have any payment"}, status_code=status.HTTP_400_BAD_REQUEST)
    except errors.DoesNotExist:
        return Fortauto.response({"message": "payment does not exist"}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception.__base__:
        return Fortauto.response({"message": "error getting user payments"},
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@payment_router.get("/{payment_RefNo}")
async def get_single_payment( payment_RefNo:str, user: dict = Depends(UserMixin.authenticate_user)):
    try:
        payment = Payment.get_single_payment(payment_RefNo=payment_RefNo, userId=user["id"])
        if payment:
            return Fortauto.response({"payments": payment.to_json()},
                                     status_code=status.HTTP_200_OK)
        return Fortauto.response({"message": "payment not found"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    except errors.DoesNotExist:
        return Fortauto.response({"message": "payment does not exist"}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception.__base__:
        return Fortauto.response({"message": "error getting user payment"},
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@payment_router.delete("/{payment_RefNo}")
async def delete_payment(payment_RefNo: str, user: dict = Depends(UserMixin.authenticate_user)):
    if user["super_admin"]:
        try:
            payment = Payment.get_single_payment(payment_RefNo=payment_RefNo)
            if payment:
                payment.delete()
                return Fortauto.response({"message": "payment deleted successfully", "payment":payment_RefNo},
                                         status_code=status.HTTP_200_OK)
            return Fortauto.response({"message": "payment not found"},
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except errors.DoesNotExist:
            return Fortauto.response({"message": "payment does not exist"}, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception.__base__:
            return Fortauto.response({"message": "error deleting payment"},
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Fortauto.response({"message": "error validating admin"},
                             status_code=status.HTTP_401_UNAUTHORIZED)


############################# user deposit start here ################################

@user_deposit.post("/")
async def create__deposit(deposit_details:UserDeposit, user:dict = Depends(UserMixin.authenticate_user)):
    try:
        ## MAKE A REQUEST TO VERIFY PAYMENT with payment_ref
        user_account = Deposit.get_user_account(userId=user["id"])
        if user_account:
            current_balance = (user_account.total_amount + deposit_details.total_amount)
            user_account.update(total_amount=current_balance)
            user_account.save(clean=True)
            return Fortauto.response({"message": f"You account credited with ₦{deposit_details.total_amount}"},
                                     status_code=status.HTTP_201_CREATED)
        deposit = Deposit(total_amount=deposit_details.total_amount, userId=user["id"]).save(clean=True)
        if deposit:
            return Fortauto.response({"message":f"You account credited with ₦{deposit_details.total_amount}"},
                                     status_code=status.HTTP_201_CREATED)
        return Fortauto.response({"message":"error making deposit"},
                                     status_code=status.HTTP_400_BAD_REQUEST)
    except errors.ValidationError:
        return Fortauto.response({"message": "error validating payment details"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    except Exception.__base__:
        return Fortauto.response({"message": "error making depositing"},
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@user_deposit.put("/")
async def update_user_deposit_account(deposit_details:UpdateDeposit, user:dict = Depends(UserMixin.authenticate_user)):
    if user["super_admin"]:
        try:
            user_account = Deposit.get_user_account(userId=deposit_details.userId)
            if user_account:
                if deposit_details.method.lower() == "credit" and deposit_details.total_amount > 0 :
                    current_balance = (user_account.total_amount + deposit_details.total_amount)
                    user_account.update(total_amount=current_balance)
                    user_account.save(clean=True)
                    return Fortauto.response({"message": f"Your account was credited with ₦{deposit_details.total_amount}"},
                                             status_code=status.HTTP_200_OK)
                elif deposit_details.method.lower() == "debit"  and deposit_details.total_amount > 0:
                    if user_account.total_amount < deposit_details.total_amount:
                        balance = (deposit_details.total_amount - user_account.total_amount)
                        return Fortauto.response({"message":f"user does not have sufficient amount, required ₦{balance} to complete transaction"},
                                                 status_code=status.HTTP_400_BAD_REQUEST)
                    current_balance = (user_account.total_amount - deposit_details.total_amount)
                    user_account.update(total_amount=current_balance)
                    user_account.save(clean=True)
                    return Fortauto.response(
                        {"message": f"Your account was debited with ₦{deposit_details.total_amount}"},
                        status_code=status.HTTP_200_OK)
                if deposit_details.method.lower() != "debit" and deposit_details.method != "credit":
                    return Fortauto.response(
                        {"message": "deposit method not recognized"},
                        status_code=status.HTTP_400_BAD_REQUEST)
                elif deposit_details.total_amount <= 0:
                    return Fortauto.response({"message": "you can only deposit amount greater than ₦100 "},
                                             status_code=status.HTTP_400_BAD_REQUEST)
        except errors.ValidationError:
            return Fortauto.response({"message": "error validating payment details"},
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except Exception.__base__:
            return Fortauto.response({"message": "error updating user credit account"},
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Fortauto.response(
                        {"message": f"Error validating admin"},
                        status_code=status.HTTP_401_UNAUTHORIZED)

@user_deposit.get("/")
async def get_user_depositd_balance(user:dict = Depends(UserMixin.authenticate_user)):
    try:
        user_account = Deposit.get_user_account(userId=user["id"])
        if user_account:
            return Fortauto.response({"message": user_account.to_json()},
                                     status_code=status.HTTP_201_CREATED)
        return Fortauto.response({"message":"User does not have any credit account"},
                                     status_code=status.HTTP_400_BAD_REQUEST)
    except Exception.__base__:
        return Fortauto.response({"message": "error getting user credit account"},
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)




@user_deposit.delete("/{userId}")
async def remove_user_deposit_account(user:dict = Depends(UserMixin.authenticate_user)):
    if user["super_admin"]:
        try:
            user_account = Deposit.get_user_account(userId=user["id"])
            if user_account:
                user_account.delete()
                return Fortauto.response({"message": "user credit account was removed"},
                                         status_code=status.HTTP_200_OK)
            return Fortauto.response({"message": "User does not have any credit account"},
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except Exception.__base__:
            return Fortauto.response({"message": "error removing user credit account"},
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Fortauto.response({"message": "error validating admin"},
                             status_code=status.HTTP_401_UNAUTHORIZED)














