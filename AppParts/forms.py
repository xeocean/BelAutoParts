from django import forms


class OrderForm(forms.Form):
    order_name = forms.CharField(label='Имя', max_length=100)
    order_phone = forms.CharField(label='Номер телефона', max_length=20)
    part_name = forms.CharField(widget=forms.HiddenInput())
    part_code = forms.CharField(widget=forms.HiddenInput())
