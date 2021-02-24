from smtplib import SMTP_SSL

from fastapi.responses import JSONResponse

from fortauto.settings import API_URL
from fortauto.settings import EMAIL, PASSWORD


class Fortauto(object):
    @staticmethod
    def route_prefix(url_prefixName):
        return f"{API_URL}/{url_prefixName}"

    @staticmethod
    def run_once(f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)

        wrapper.has_run = False
        return wrapper

    @staticmethod
    def response(message: dict, status_code: int):
        return JSONResponse(content=message, status_code=status_code)

    @staticmethod
    def mailUsr(email_message: str, user_email: str, email_title: str):
        try:
            with SMTP_SSL(host="smtp.gmail.com", port=465) as mail:
                mail.login(EMAIL, PASSWORD)
                message = f"subject:{email_title}\n\n{email_message}"
                mail.sendmail(from_addr=EMAIL, to_addrs=user_email, msg=message)
                return "email sent successfully"
        except Exception as e:
            return f"error sending email {e}"
