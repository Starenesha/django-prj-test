from django.test import TestCase
from meter.models import *
from datetime import date
# Create your tests here.


class MetersTest(TestCase):

    def setUp(self):
        self.test_meter = Meter.objects.create(meter_name='Test',
                                                resource='W',
                                                unit='m3',
                                               slug= 'test'),
                                               unit='m3')

    def test_meter_creation(self):
        self.assertTrue(isinstance(self.test_meter, Meter))

    def test_str_meter(self):
        self.assertEqual(self.test_meter.__str__(), self.test_meter.meter_name)

    def test_meter_absolute_url(self):
        self.assertEqual(self.test_meter.get_absolute_url(),'meter_detail', kwargs={'slug':self.slug})





class CSVUpload(TestCase):

    def setUp(self):
        self.test_meter = Meter.objects.create(meter_name='Test',resource='W',unit='m3',slug= gen_slug(self.meter_name),unit='m3')

        self.test_record1 = CSVUpload.objects.create(meter=self.test_meter,
                                                        date=date(2019,6,8),
                                                        value=1)
        self.test_record_second = CSVUpload.objects.create(meter=self.test_meter,
                                                         date=date(2019, 6, 10),
                                                         value=2)


   def test_creation(self):

        self.assertTrue(isinstance(self.test_first_record, CSVUpload))
        self.assertTrue(isinstance(self.test_second_record, CSVUpload))


