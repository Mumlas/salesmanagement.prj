from django.forms import ModelForm
from .models import Shift, Sales

class EditShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = [
            'type', 'start', 'end', 'staff','pump','status', 'inventory',
        ]
    
    def __init__(self, *args, **kwargs):
        super(EditShiftForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['branch'].widget.attrs['readonly'] = True
            self.fields['pump'].widget.attrs['readonly'] = True
            self.fields['product'].widget.attrs['readonly'] = True
            self.fields['stock'].widget.attrs['readonly'] = True

class NewShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = [
            'type', 'start', 'end', 'staff','pump','status', 'inventory',
        ]
    
    def __init__(self, *args, **kwargs):
        super(NewShiftForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['staff'].widget.attrs['readonly'] = True

class ReconcileSalesForm(ModelForm):
        class Meta:
            model = Sales
            fields = [
                'shift', 'quantity_sold', 'expected_sales', 'actual_sales','margin','reconciliation', 'remark',
            ]

        def __init__(self, *args, **kwargs):
            super(ReconcileSalesForm, self).__init__(*args, **kwargs)
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                self.fields['shift'].widget.attrs['readonly'] = True
                self.fields['quantity_sold'].widget.attrs['readonly'] = True
                self.fields['expected_sales'].widget.attrs['readonly'] = True
                self.fields['actual_sales'].widget.attrs['readonly'] = True
                self.fields['margin'].widget.attrs['readonly'] = True

