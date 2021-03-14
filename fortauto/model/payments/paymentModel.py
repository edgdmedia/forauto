from mongoengine import *
from datetime import datetime
class Payment(Document):
    userId = ObjectIdField(required=True)
    services = ListField(DictField(), required=True)
    payment_status = StringField(choices=("success", "pending", "canceled", "failed"))
    payment_RefNo = StringField(unique=True)
    method = StringField(required=True)
    total_amount = IntField(required=True, decimal_places=2)
    created_at = DateTimeField(default=datetime.utcnow)

    def to_json(self, *args, **kwargs):
        return {
            "id":str(self.id),
            "userId":str(self.userId),
            "services":self.services,
            "payment_RefNo":self.payment_RefNo,
            "payment_status":self.payment_status,
            "method":self.method,
            "total_amount":self.total_amount,
            "created_at":str(self.created_at)
        }

    @queryset_manager
    def get_user_payment(doc_cls, queryset, userId:str):
        return queryset.filter(userId=userId).all()

    @queryset_manager
    def get_single_payment(doc_cls, queryset, payment_RefNo:int):
        return queryset.filter(payment_RefNo=payment_RefNo).first()




class Deposit(Document):
    userId = ObjectIdField(required=True, unique=True)
    total_amount = IntField(required=True, decimal_places=2)
    created_at = DateTimeField(default=datetime.utcnow)

    def to_json(self, *args, **kwargs):
        return {
            "id": str(self.id),
            "userId": str(self.userId),
            "total_amount": self.total_amount,
            "created_at": str(self.created_at)
        }

    @queryset_manager
    def get_user_account(doc_cls, queryset, userId: str):
        return queryset.filter(userId=userId).first()

    @queryset_manager
    def get_single_amount(doc_cls, queryset, userId: str):
        user = queryset.filter(userId=userId).first()
        if user:
            return user.total_amount
        return None