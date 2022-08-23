from django.forms import ModelForm
from .models import Entry, Sku
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput


class DateInput(forms.DateInput):
    input_type = 'date'


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = '__all__'

    def __init__(self, *args, **kwrags):
        super(EntryForm, self).__init__(*args, **kwrags)


        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'form-control'})

        self.fields['order_date'].widget.attrs.update({'class':'input form-control', 'type':"date"})

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your Name', max_length=100)


class SkuForm(ModelForm):
    class Meta:
        model = Sku
        fields = '__all__'

    def __init__(self, *args, **kwrags):
        super(SkuForm, self).__init__(*args, **kwrags)
    
        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'form-control'})

class PartialCompleteForm(forms.Form):
    qty = forms.IntegerField(label="Partial Order Quantity")

