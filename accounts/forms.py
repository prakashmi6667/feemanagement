from django import forms
from .models import WalletTransaction

class WalletTransactionForm(forms.ModelForm):

    class Meta:
        model = WalletTransaction
        fields = "__all__"
        exclude = ('franchise', 'transaction_type', 'status', 'signature', 'order_id', 'payment_id')

    def __init__(self, *args, **kw):
        super(WalletTransactionForm, self).__init__(*args, **kw)
        # self.fields['course'].required = True
