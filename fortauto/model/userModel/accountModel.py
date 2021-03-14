from datetime import datetime

from mongoengine import *

class CarDetail(EmbeddedDocument):
    maker = StringField(default=None)
    model = StringField(default=None)
    vin_number = StringField(default=None)

    def to_json(self, *args, **kwargs):
        return {
            "maker": self.maker,
            "model": self.model,
            "vin_number": self.vin_number,
        }
    @queryset_manager
    def removeId(doc_cls, queryset, vin_number):
        car = queryset.filter(vin_number=vin_number).first()
        car.delete()
        return vin_number

    @queryset_manager
    def get_car(doc_cls, queryset, vin_number):
        car = queryset.filter(vin_number=vin_number).first()
        return car




class User(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = EmailField(required=True, unique=True, min_length=5)
    state = StringField(required=True)
    car_details = EmbeddedDocumentListField(CarDetail)
    phone_number = StringField(required=True)
    city = StringField(required=True)
    address = StringField(required=True)
    password = StringField(required=True)
    active = BooleanField(required=True, default=False)
    super_admin = BooleanField(required=True, default=False)
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
            "super_admin":self.super_admin,
            "created_at": str(self.created_at)
        }
