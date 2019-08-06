import csv,io, os
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import View
from .models import *
from .forms import *
from datetime import datetime
from .utils import consumption
# Create your views here.


def MetersList(request):

    meters = Meter.objects.all()
    return render(request,'list_meters.html', context={'meters':meters})


class MeterDetail(View):


    def get(self,request,slug):

        meter = get_object_or_404(Meter,slug__iexact=slug)
        slug_ = meter.slug
        records = CSVUpload.objects.filter(name_place=slug_)
        Date = CSVUpload.objects.filter(name_place=slug_).last()
        if Date is not None:
            last_date = Date.date
        else:
            last_date = None

        result_lst=consumption(records)
        if records is not None:

            return render(request,'meter_detail.html',context={'meter':meter,'result_lst': result_lst, 'last_date':last_date})
        else:
            return render(request, 'meter_detail.html', context={'meter': meter})


    def post(self,request,slug):
        form = UploadCsvForm(request.POST, request.FILES)
        meter = Meter.objects.get(slug__iexact=slug)
        slug_ = meter.slug
        if form.is_valid():
            CSVUpload.objects.filter(name_place=slug_).delete()
            data = csv.DictReader(request.FILES['upload_file'].read().decode('utf-8').splitlines())
            for row in data:
                p = CSVUpload.objects.create(date=row['DATE'], value=row['VALUE'], name_place=slug_)
                p.save()

            records_ = CSVUpload.objects.filter(name_place=slug_)
            result_lst=consumption(records_)
            Date = CSVUpload.objects.filter(name_place=slug_).last()
            last_date = Date.date

            if result_lst is None:
                result_lst = None
                last_date = None

            return render(request, 'meter_detail.html', context={'meter': meter, 'result_lst': result_lst,'last_date':last_date})

        else:
            return render(request, 'meter_detail.html', context={'meter': meter})


def meter_delete_data(request, slug):
    meter = get_object_or_404(Meter,slug__iexact=slug)
    slug_ = meter.slug
    if request.method == "POST":

        CSVUpload.objects.filter(name_place=slug_).delete()
        return redirect(meter.get_absolute_url())


class CreateMeter(View):

    def get(self,request):
        form = MeterForm()
        return render(request, 'create_meter.html', context={'form':form})

    def post(self,request):
        bound_form = MeterForm(request.POST)

        if bound_form.is_valid():
            new_meter = bound_form.save()
            return redirect(new_meter)
        else:
            return render(request, 'create_meter.html', context={'form':bound_form})


class MeterDelete(View):

    def get(self,request,slug):
        meter =Meter.objects.get(slug__iexact=slug)
        return render(request, 'meter_delete.html', context={'meter':meter})

    def post(self,request,slug):
        meter = Meter.objects.get(slug__iexact=slug)
        meter.delete()
        return redirect('list_meters')








