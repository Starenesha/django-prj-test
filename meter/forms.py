from django import forms
from django.shortcuts import render, redirect
from .models import *
from django.core.exceptions import ValidationError


class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['meter_name','resource', 'unit']

        widgets = {
            'meter_name': forms.TextInput(attrs={'class': 'form-control'}),
            'resource': forms.Select(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'})
        }

        def clean_meter(self):
            new_slug = self.cleaned_data['slug'].lower()

            if Meter.objects.filter(slug__iexact=new_slug).count():
                raise ValidationError('Name must be unique.'.format(new_slug))
            return new_slug


class UploadCsvForm(forms.Form):
    upload_file = forms.FileField()
