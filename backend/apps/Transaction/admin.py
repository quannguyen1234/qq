from django.contrib import admin
from .models import Transaction,Wallet,DiagnosticBill,DiagnosticBillDetail
# Register your models here.


admin.site.register(Transaction)
admin.site.register(Wallet)
admin.site.register(DiagnosticBill)
admin.site.register(DiagnosticBillDetail)
