import csv,io
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import View
from .models import *
from .forms import *
from datetime import datetime
from .utils import consuptions

# Create your views here.

def MetersList(request):

    meters = Meter.objects.all()
    return render(request,'list_meters.html', context={'meters':meters})


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


class MeterDetail(View):

    def get(self,request,slug):
        #meter = Meter.objects.get(slug__iexact=slug)
        meter = get_object_or_404(Meter,slug__iexact=slug)
        return render(request,'meter_detail.html',context={'meter':meter})

    def post(self,request,slug):
        form = UploadCsvForm(request.POST, request.FILES)
        meter = Meter.objects.get(slug__iexact=slug)

        if form.is_valid():
            csv_form = CSVUpload(file=request.FILES['upload_file'])
            csv_form.save()
            date = datetime.now()

            paramFile=request.FILES['upload_file'].open("rb")
            decoded_file = paramFile.read().decode('utf-8')
            io_string =io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=';', quotechar='|')
            header_ = next(reader)
            header_cols = convert_header(header_)
            parsed_items = []

            for line in reader:
                parsed_row_data ={}
                i = 0
                row_item =line[0].split(',')
                for item in row_item:
                    key = header_cols[i]
                    parsed_row_data[key] = item
                    i+=1
                parsed_items.append(parsed_row_data)

            data_for_function = consuptions(parsed_items)


            return render(request,'meter_detail.html',context={'meter':meter,'date':date,'data_for_function':data_for_function})
        else:
            return render(request,'meter_detail.html',context={'meter':meter})



