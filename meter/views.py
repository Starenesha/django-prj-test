import csv,io, os
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import View
from .models import *
from .forms import *
from datetime import datetime
from .utils import consumption
from django.conf import settings
from django.core.files.storage import default_storage
from app.settings import MEDIA_ROOT
# Create your views here.






def MetersList(request):

    meters = Meter.objects.all()
    return render(request,'list_meters.html', context={'meters':meters})



#def parser(path_to_file):

   # f = open(path_to_file,'rb')
   # decoded_file = f.read().decode('utf-8')
   # io_string = io.StringIO(decoded_file)
   # reader = csv.reader(io_string, delimiter=';', quotechar='|')
   # header_ = next(reader)
   # header_cols = convert_header(header_)
   # parsed_items = []

   #for row in reader:
   #     CSVUpload.objects.create(meter=row[0],date=row[1],record=row[2])
     #   parsed_row_data = {}
      #  i = 0
       # row_item = line[0].split(',')
       # for item in row_item:
       #    key = header_cols[i]
       #     parsed_row_data[key] = item
       #    i += 1
       #parsed_items.append(parsed_row_data)

  #  data_for_function = consuptions(parsed_items)

  #  return data_for_function


class MeterDetail(View):


    def get(self,request,slug):
        #meter = Meter.objects.get(slug__iexact=slug)
        meter = get_object_or_404(Meter,slug__iexact=slug)
        slug_ = meter.slug
        records = CSVUpload.objects.filter(name_place=slug_)

        result_lst=consumption(records)
        if records is not None:
            return render(request,'meter_detail.html',context={'meter':meter,'result_lst': result_lst})
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

            if result_lst is None:
                result_lst = None

            #records = CSVUpload.objects.filter(name_place=slug_)#[{},{}]
            #tmp_value=[] # list all values
            #for x in records:
            #    tmp=x.value
            #    tmp_value.append(tmp)
            #   records=x
            #tmp_date =[] # list of all date
            #records_ = CSVUpload.objects.filter(name_place=slug_)  # [{},{}]
            #for x in records_:
             #   tmp=x.date.isoformat()
             #   tmp_date.append(tmp)
             #   records_=x

            #tmp_date_ = tmp_date[1:]

            #lst_consumption =[]
            #diff = [tmp_value[n - 1] - tmp_value[n] for n in range(1, len(tmp_value))]
            #result_lst = list(zip(tmp_date, tmp_date_, diff))

            return render(request, 'meter_detail.html', context={'meter': meter, 'result_lst': result_lst})

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








