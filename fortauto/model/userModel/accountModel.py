from datetime import datetime

from mongoengine import *


class User(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True, unique=True, min_length=5)
    state = StringField(required=True)
    phone_number = StringField(required=True)
    city = StringField(required=True)
    address = StringField(required=True)
    password = StringField(required=True)
    active = BooleanField(required=True, default=False)
    admin = BooleanField(required=True, default=False)
    created_at = DateField(required=True, default=datetime.utcnow)

    @queryset_manager
    def find_user_with_email(doc_cls, queryset: object, email: str) -> object:
        """
        :param email:
        :type queryset: object
        """
        return queryset.filter(email=email).first()

    @queryset_manager
    def find_user_with_Id(doc_cls, queryset: object, userId: str) -> object:
        """
        :param email:
        :type queryset: object
        """
        return queryset.filter(id=userId).first()

    def to_json(self, *args, **kwargs):
        """"
        This method is use to return a json of user details.
          """
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "active": self.active,
            "admin": self.admin,
            "created_at": str(self.created_at)
        }
