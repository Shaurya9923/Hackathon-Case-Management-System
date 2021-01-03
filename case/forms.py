from django import forms
from .models import cases,case_hearings,case_invoices

class case_form(forms.Form):
    detail_doc = forms.FileField(label='',required=False)
    reply = forms.FileField(label='',required=False)
    rejoinder= forms.FileField(label='',required=False)

class hearing_form(forms.Form):

    detail_doc = forms.FileField(label='',required=False)

class invoice_form(forms.Form):

    invoice_doc = forms.FileField(label='',required=False)
