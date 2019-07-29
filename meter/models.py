import csv, io
from datetime import datetime
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify


# Create your models here.


def gen_slug(s):
    new_slug = slugify(s,allow_unicode=True)
    return new_slug

class Meter(models.Model):
    meter_name = models.CharField(max_length=50, db_index=True )
    unit = models.CharField(max_length=10, db_index=True )
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    resource_list =(("E", "Electricity"),("W","Water"),("G","Gas"))
    resource = models.CharField(max_length=2,choices=resource_list)


    def __str__(self):
        return "{}".format(self.meter_name)

    def get_absolute_url(self):
        return reverse('meter_detail', kwargs={'slug':self.slug})

    def save(self,*args,**kwargs):
        if not self.id:
            self.slug = gen_slug(self.meter_name)
        super(Meter,self).save(*args,**kwargs)




class CSVUpload(models.Model):

    file = models.FileField(upload_to='uploads/%Y/%m/%d')
    created_date = models.DateTimeField(default=datetime.now)




def convert_header(csvHeader):
    header_ = csvHeader[0]
    cols = [x.replace('','_').lower() for x in header_.split(",")]
    return cols