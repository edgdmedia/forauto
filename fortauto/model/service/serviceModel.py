from mongoengine import *
from datetime import datetime

class ServiceList(Document):
    name = StringField(required=True, unique=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow)

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
            "created_at":str(self.created_at)
        }


class Service(Document):
    car_type = StringField(required=True)
    service_type = StringField(required=True)
    additional_notes = MultiLineStringField(default="no note")
    quantity = IntField(max_length=300, min_length=0)
    priority = StringField(required=True)
    date = DateTimeField(default=datetime.utcnow)

    @queryset_manager
    def get_all_service(doc_cls, queryset):
        return queryset.all()

    @queryset_manager
    def get_single_serviceById(doc_cls, queryset, serviceId):
        return queryset.filter(id=serviceId).first()

    @queryset_manager
    def get_single_serviceByName(doc_cls, queryset, serviceName):
        return queryset.filter(name=serviceName).first()

    def to_json(self, *args, **kwargs):
        return {
            "id":str(self.id),
            "car_type":self.car_type,
            "service_type":self.service_type,
            "quantity":self.quantity,
            "priority":self.priority,
            "additional_notes":self.additional_notes,
            "data":str(self.date)
        }

