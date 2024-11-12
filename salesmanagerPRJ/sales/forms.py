from django.forms import ModelForm
from .models import Shift

class EditShiftForm(ModelForm):
    class Meta:
        model = Shift
        fields = [
            'type', 'start', 'end','branch', 'staff','pump','product','stock','is_active'
        ]
    
    def __init__(self, *args, **kwargs):
        super(EditShiftForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['branch'].widget.attrs['readonly'] = True
            self.fields['pump'].widget.attrs['readonly'] = True
            self.fields['product'].widget.attrs['readonly'] = True
            self.fields['stock'].widget.attrs['readonly'] = True

class PostSalesForm(ModelForm):
        class Meta:
            model = Shift
            fields = [
                'type', 'start', 'end','branch', 'staff','pump','product','stock','is_active',
            ]

        def __init__(self, *args, **kwargs):
            super(EditShiftForm, self).__init__(*args, **kwargs)
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                self.fields['branch'].widget.attrs['readonly'] = True
                self.fields['pump'].widget.attrs['readonly'] = True
                self.fields['product'].widget.attrs['readonly'] = True
                self.fields['stock'].widget.attrs['readonly'] = True
                self.fields['type'].widget.attrs['readonly'] = True
                self.fields['start'].widget.attrs['readonly'] = True
                self.fields['end'].widget.attrs['readonly'] = True
                self.fields['is_active'].widget.attrs['readonly'] = True