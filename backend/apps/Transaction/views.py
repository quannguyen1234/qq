from rest_framework.viewsets import ModelViewSet
from .serializers import DiagnosticBillSerializer
from .models import DiagnosticBill,DiagnosticBillDetail,Transaction
from apps.User.models import BaseUser,Admin
from core.references import StatusTransactionEnum,TypeTransactionEnum,PaymentMethodEnum,DiagnosticFormEnum
from .models import Wallet
from channels.db import database_sync_to_async
from core.references import FEE_DISTANCE

@database_sync_to_async
def check_amount(fee,base_user):
    wallet=Wallet.objects.get(base_user=base_user)

    if wallet.available_amount>=fee:
        return True
    return False

class HoldMoney:
    def __init__(self,base_user) -> None:
        self.base_user=base_user

    def run(self,fee):
        pass

class PatientHoldMoney(HoldMoney):
    def __init__(self, base_user) -> None:
        super().__init__(base_user)
    

    def run(self,fee):
        
        patients_wallet=Wallet.objects.get(
            base_user=self.base_user
        )

        admin_wallet=Wallet.objects.get(
            base_user=Admin.objects.get(admin_id='1').base_user
        )

        patients_wallet.transfer_money(fee,admin_wallet)

class TransferMoney:
    def __init__(self,base_user) -> None:
        self.base_user=base_user

    def transfer(self,fee,to_base_user):
        from_wallet=Wallet.objects.get(
            base_user=self.base_user
        )
        to_wallet=Wallet.objects.get(
            base_user=to_base_user
        )
        from_wallet.transfer_money(fee,to_wallet)

    
class Fee:
    def __init__(self,doctor) -> None:
        self.doctor=doctor

    def get_fee(self):
        pass

class FeeBooking(Fee):

    def __init__(self, doctor,distance) -> None:
        super().__init__(doctor)
        self.distance=distance

    def get_fee(self):
    
        return self.doctor.diagnostic_fee + self.distance*FEE_DISTANCE


    


class DiagnosticBillAPI(ModelViewSet):
    serializer_class=DiagnosticBillSerializer
    queryset=DiagnosticBill.objects.all()
    permission_classes=[]

    
    