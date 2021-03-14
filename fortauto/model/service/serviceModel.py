from mongoengine import *
from datetime import datetime
from os import urandom
class ServiceList(Document):
    name = StringField(required=True, unique=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow)
    price = IntField(default=0, required=True)

    @queryset_manager
    def get_all_serviceList(doc_cls, queryset):
        return queryset.all()

    @queryset_manager
    def get_single_serviceListById(doc_cls, queryset, serviceListId):
        return queryset.filter(id=serviceListId).first()

    @queryset_manager
    def get_single_serviceListByName(doc_cls, queryset, serviceName):
        return queryset.filter(name=serviceName).first()

    def to_json(self, *args, **kwargs):
        return {
            "id":str(self.id),
            "name":self.name,
            "price":self.price,
            "created_at":str(self.created_at)
        }

class ServiceCategory(Document):
    name = StringField(required=True, unique=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow)

    @queryset_manager
    def get_all_service_category(doc_cls, queryset):
        return queryset.all()

    @queryset_manager
    def get_single_service_category_ById(doc_cls, queryset, serviceListId):
        return queryset.filter(id=serviceListId).first()

    @queryset_manager
    def get_single_service_category_ByName(doc_cls, queryset, serviceName):
        return queryset.filter(name=serviceName).first()

    def to_json(self, *args, **kwargs):
        return {
            "id":str(self.id),
            "name":self.name,
            "created_at":str(self.created_at)
        }

def get_date():
    return str(datetime.today())

class Service(Document):
    userId = StringField(required=True)
    serviceId = StringField(default=urandom(3).hex())
    car_type = StringField(required=True)
    service_type = StringField(required=True)
    additional_notes = StringField(default="no note")
    quantity = IntField(max_length=300, min_length=0, default=0)
    status = StringField(choices=("picked", "repairing", "ready", "deliver", "pending", "processing"), default="processing")
    price = IntField(default=0)
    priority = StringField(required=True)
    date = StringField(default=get_date())



    @queryset_manager
    def get_all_service(doc_cls, queryset):
        return queryset.all()

    @queryset_manager
    def get_single_serviceById(doc_cls, queryset, serviceId):
        return queryset.filter(serviceId=serviceId).first()

    @queryset_manager
    def get_single_serviceByName(doc_cls, queryset, serviceName):
        return queryset.filter(name=serviceName).first()

    def to_json(self, *args, **kwargs):
        return {
            "id":str(self.id),
            "userId":self.userId,
            "serviceId":str(self.serviceId),
            "car_type":self.car_type,
            "service_type":self.service_type,
            "quantity":self.quantity,
            "priority":self.priority,
            "price":self.price,
            "status":self.status,
            "additional_notes":self.additional_notes,
            "data":str(self.date)
        }

