from django.db import models
from apps.User.models import BaseUser,Doctor,Patient
from core.references import StatusTransactionEnum,TypeTransactionEnum,PaymentMethodEnum,DiagnosticFormEnum
import uuid

# Create your models here.
class Wallet(models.Model):
    class Meta:
        constraints=[
            models.CheckConstraint(check=models.Q(available_amount__gte=0), name='available_amount_gte_0') ,
            models.UniqueConstraint(
                name="unique_wallet_person",
                fields=["base_user"],
            )

        ]
    wallet_id=models.CharField(primary_key=True,max_length=8)
    base_user=models.ForeignKey(BaseUser,null=False,on_delete=models.CASCADE)
    available_amount=models.FloatField(default=0,null=False)

class Transaction(models.Model):
    class Meta:
        constraints=[
            models.CheckConstraint(check=models.Q(amount__gte=0), name='transaction_amount_gte_0') ,
        ]
    transaction_id=models.CharField(max_length=8,primary_key=True)
    amount=models.FloatField(default=0,null=False)
    detail=models.TextField(default='')
    date=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False) # true is the money in , otherwise money  out
    transaction_type=models.CharField(choices=TypeTransactionEnum.__tupple__(),max_length=32)
    payment_method=models.CharField(max_length=32,choices=PaymentMethodEnum.__tupple__())

    

class DiagnosticBill(models.Model):
    class Meta:
        db_table="DiagnosticBill"

    doctor=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL)
    patient=models.ForeignKey(Patient,null=True,on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    pay_time= models.DateTimeField(null=True)
    diagnostic_form=models.CharField(max_length=32,choices=DiagnosticFormEnum.__tupple__())

class DiagnosticBillDetail(models.Model):
    class Meta:
        db_table="DiagnosticBillDetail"
        constraints=[
            models.CheckConstraint(check=models.Q(distance__gte=0), name='distance_gte_0') ,
            models.CheckConstraint(check=models.Q(doctor_fee__gte=0), name='doctor_fee_gte_0') ,
            models.CheckConstraint(check=models.Q(total_fee__gte=0), name='total_fee_gte_0') ,
        ]
        
    id=models.CharField(primary_key=True,max_length=36,default = uuid.uuid4)
    bill=models.ForeignKey(DiagnosticBill,on_delete=models.CASCADE,null=False)
    distance=models.IntegerField(default=0)
    doctor_fee=models.FloatField(default=0)
    total_fee=models.FloatField(default=0)



        