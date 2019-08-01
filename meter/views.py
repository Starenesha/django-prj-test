import csv,io, os
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import View
from .models import *
from .forms import *
from datetime import datetime
from .utils import consuptions
from django.conf import settings
from django.core.files.storage import default_storage
from app.settings import MEDIA_ROOT
# Create your views here.

path_to_file = os.path.join(MEDIA_ROOT, 'filename')


def file_upload(request):
    save_path = os.path.join(settings.MEDIA_ROOT,'uploads', request.FILES['upload_file'])
    path = default_storage.save(save_path, request.FILES['upload_file'])
    return default_storage.path(path)


def MetersList(request):

    meters = Meter.objects.all()
    return render(request,'list_meters.html', context={'meters':meters})



def parser(path_to_file):

    f = open(path_to_file,'rb')
    decoded_file = f.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.reader(io_string, delimiter=';', quotechar='|')
    header_ = next(reader)
    header_cols = convert_header(header_)
    parsed_items = []

    for line in reader:
        parsed_row_data = {}
        i = 0
        row_item = line[0].split(',')
        for item in row_item:
            key = header_cols[i]
            parsed_row_data[key] = item
            i += 1
        parsed_items.append(parsed_row_data)

    data_for_function = consuptions(parsed_items)

    return data_for_function


class MeterDetail(View):


    def get(self,request,slug):
        #meter = Meter.objects.get(slug__iexact=slug)
        meter = get_object_or_404(Meter,slug__iexact=slug)
        path_to_file = os.path.join(MEDIA_ROOT, 'filename')
        if os.path.exists(path_to_file):
            result = parser(path_to_file)
            return render(request,'meter_detail.html',context={'meter':meter,'result':result})
        else:
            return render(request,'meter_detail.html',context={'meter':meter})


    def post(self,request,slug):
        form = UploadCsvForm(request.POST, request.FILES)
        meter = Meter.objects.get(slug__iexact=slug)

        if form.is_valid():
            csv_form = CSVUpload(file=request.FILES['upload_file'])

            csv_form.save()
            date = datetime.now()
            result=parser(path_to_file)


            return render(request,'meter_detail.html',context={'meter':meter,'result':result})
        else:
            return render(request,'meter_detail.html',context={'meter':meter})



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








