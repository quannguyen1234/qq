from django.db import models
from apps.User.models import BaseUser,Doctor,Patient
from core.references import StatusTransactionEnum,TypeTransactionEnum,PaymentMethodEnum,DiagnosticFormEnum
import uuid
from core.references import FEE_DISTANCE

import random
def generate_character(length:int):
    s=''
    for i in range(length):
        s+=str(random.randint(0,9))
    return s

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

    def transfer_money(self,fee,to_wallet):
        if self.available_amount<=fee:
            raise ValueError("dont enough Money")
        
        self.available_amount-=fee
        to_wallet.available_amount+=fee
        to_wallet.save()
        self.save()


        #transaction for own 
        Transaction.objects.create(
            transaction_id=Transaction.generate_id(),
            base_user=self.base_user,
            amount=fee,
            detail=' ',
            status=StatusTransactionEnum.MONEY_OUT.value,
            transaction_type=TypeTransactionEnum.TRANSFER_MONEY.value,
            payment_method=PaymentMethodEnum.BANKING.value
        )

        #transaction for destination 
        Transaction.objects.create(
            transaction_id=Transaction.generate_id(),
            base_user=to_wallet.base_user,
            amount=fee,
            detail=' ',
            status=StatusTransactionEnum.MONEY_IN.value,
            transaction_type=TypeTransactionEnum.RECIEVE_MONEY.value,
            payment_method=PaymentMethodEnum.BANKING.value
        )
        
        def __str__(self):
            return f"Wallet ID: {self.wallet_id} -{self.base_user.user_type}"

class Transaction(models.Model):
    class Meta:
        constraints=[
            models.CheckConstraint(check=models.Q(amount__gte=0), name='transaction_amount_gte_0') ,
        ]
    transaction_id=models.CharField(max_length=8,primary_key=True)
    base_user=models.ForeignKey(BaseUser,on_delete=models.SET_NULL,null=True)
    amount=models.FloatField(default=0,null=False)
    detail=models.TextField(default='')
    date=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False) # true is the money in , otherwise money  out
    transaction_type=models.CharField(choices=TypeTransactionEnum.__tupple__(),max_length=32)
    payment_method=models.CharField(max_length=32,choices=PaymentMethodEnum.__tupple__())

    @classmethod
    def check_id(cls,transaction_id):
        if cls.objects.filter(transaction_id=transaction_id).exists():
            return True
        return False
    
    @classmethod
    def generate_id(cls):
        while True:
            id=generate_character(8)
            if not Transaction.check_id(id):    
                return id

    

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
          
        ]
        
    id=models.CharField(primary_key=True,max_length=36,default = uuid.uuid4)
    bill=models.OneToOneField(DiagnosticBill,on_delete=models.CASCADE,null=False,related_name='detail')
    distance=models.IntegerField(default=0)
    doctor_fee=models.FloatField(default=0)
    
    @property
    def total_fee(self):
        return FEE_DISTANCE*self.distance+self.doctor_fee



        